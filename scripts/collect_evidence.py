#!/usr/bin/env python3
"""Collect a local session audit and export aggregate-only presentation data."""

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import warnings


START = "2026-10-05T00:00:00.000Z"
END = "2026-10-07T00:00:00.000Z"
AS_OF = "2026-10-06T23:27:43.000Z"
TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
JS_TOKENS = re.compile(
    r'\s+|//[^\n]*|/\*[\s\S]*?\*/|"(?:\\[\s\S]|[^"\\])*"'
    r"|'(?:\\[\s\S]|[^'\\])*'|`(?:\\[\s\S]|[^`\\])*`|[A-Za-z_$][\w$]*|\d+|.",
    re.DOTALL,
)


def literal(value):
    if value.startswith('`'):
        return value[1:-1] if '${' not in value else None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
            return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def tool_calls(code):
    """Extract direct tools calls and top-level literal fields; never run code."""
    tokens = [m.group() for m in JS_TOKENS.finditer(code)
              if not m.group().isspace() and not m.group().startswith(('//', '/*'))]
    for i in range(len(tokens) - 5):
        if tokens[i:i + 2] != ['tools', '.'] or tokens[i + 3:i + 5] != ['(', '{']:
            continue
        fields = {}
        depth = 1
        j = i + 5
        while j < len(tokens) and depth:
            token = tokens[j]
            if depth == 1 and j + 2 < len(tokens) and tokens[j + 1] == ':':
                key = literal(token) if token.startswith(('"', "'")) else token
                fields[key] = literal(tokens[j + 2])
            if token in ('{', '[', '('):
                depth += 1
            elif token in ('}', ']', ')'):
                depth -= 1
            j += 1
        yield tokens[i + 2], fields


def is_subyard_workspace(cwd):
    parts = Path(cwd).parts
    return (len(parts) == 5 and parts[:3] == ('/', 'srv', 'workspaces')
            and parts[3].lower().startswith('subyard') and parts[4] == 'src')


def summarize(events, filename, seen=None):
    meta = events[0][1]['payload']
    if not is_subyard_workspace(meta.get('cwd', '')):
        raise ValueError('Selected log is not a Subyard workspace session')
    usage = Counter()
    wait_usage = Counter()
    observation_usage = Counter()
    usage_by_action = {}
    response_counts = Counter()
    calls = Counter()
    models = set()
    seen = set() if seen is None else seen
    pending = []
    wait_records = []
    usage_records = []
    tool_times = {}
    waits = []
    ignored_poll_inputs = 0
    for line, event in events:
        timestamp = event.get('timestamp', '')
        payload = event.get('payload', {})
        kind = payload.get('type')
        in_window = START <= timestamp < END and timestamp <= AS_OF
        if event.get('type') == 'turn_context' and in_window:
            models.add(payload['model'])
        if event.get('type') == 'response_item' and kind in ('function_call', 'custom_tool_call'):
            name = payload.get('name', '')
            action = name
            if in_window:
                calls[name] += 1
                if name == 'wait_agent':
                    tool_times[payload['call_id']] = (timestamp, line)
                if name == 'exec' and kind == 'custom_tool_call':
                    code = payload.get('input', '')
                    nested = list(tool_calls(code))
                    direct_poll = (len(nested) == 1 and nested[0][0] == 'write_stdin'
                                   and nested[0][1].get('chars', '') == ''
                                   and isinstance(nested[0][1].get('session_id'), int)
                                   and not re.search(r'\b(for|while|function)\b|=>', code))
                    if direct_poll:
                        action = 'process_poll'
                    for tool, fields in nested:
                        if tool == 'write_stdin':
                            if fields.get('chars', '') == '':
                                calls['process_poll'] += 1
                            else:
                                ignored_poll_inputs += 1
            pending.append(action)
        if event.get('type') == 'token_usage_record':
            response_id = (payload.get('thread_id'), payload['response_id'])
            if payload.get('thread_id') != meta['id']:
                raise ValueError('Unexpected cross-thread usage record')
            if response_id not in seen:
                seen.add(response_id)
                values = {key: payload['usage'].get(key, 0) for key in TOKEN_KEYS}
                if values['total_tokens'] != values['input_tokens'] + values['output_tokens']:
                    raise ValueError('Unexpected token accounting')
                if in_window:
                    usage.update(values)
                    usage_records.append({'timestamp': timestamp, 'line': line, 'usage': values})
                    actions = set(pending)
                    action = next(iter(actions)) if len(actions) == 1 else ('mixed' if actions else 'message')
                    usage_by_action.setdefault(action, Counter()).update(values)
                    response_counts[action] += 1
                    if actions and actions <= {'wait_agent', 'sleep', 'wait'}:
                        wait_usage.update(values)
                        wait_records.append({'timestamp': timestamp, 'line': line, 'usage': values})
                    if actions and actions <= {'wait_agent', 'sleep', 'wait', 'process_poll', 'send_message'}:
                        observation_usage.update(values)
            pending = []
        if kind == 'function_call_output' and payload.get('call_id') in tool_times:
            begin, call_line = tool_times.pop(payload['call_id'])
            if in_window:
                seconds = (datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                           - datetime.fromisoformat(begin.replace('Z', '+00:00'))).total_seconds()
                waits.append({'timestamp': begin, 'line': call_line, 'end_line': line, 'seconds': seconds})
    source = meta.get('source', {})
    parent_id = source.get('subagent', {}).get('thread_spawn', {}).get('parent_thread_id') if isinstance(source, dict) else None
    return {
        'id': meta['id'], 'source_file': filename, 'models': sorted(models), 'parent_id': parent_id,
        'workspace': Path(meta['cwd']).parent.name,
        'agent_path': meta.get('agent_path'), 'usage': dict(usage), 'wait_usage': dict(wait_usage),
        'observation_usage': dict(observation_usage),
        'usage_by_action': {name: dict(values) for name, values in sorted(usage_by_action.items())},
        'response_counts': dict(response_counts),
        'wait_calls': calls['wait_agent'], 'sleep_calls': calls['sleep'],
        'tool_wait_calls': calls['wait'],
        'poll_calls': calls['process_poll'], 'non_poll_stdin_calls': ignored_poll_inputs,
        'message_calls': calls['send_message'], 'responses': len(usage_records),
        '_waits': waits, '_usage_records': usage_records, '_wait_records': wait_records,
        '_first': events[0][1]['timestamp'], '_last': events[-1][1]['timestamp'],
    }


def read_events(path):
    events = []
    with path.open(encoding='utf-8') as source:
        for line, text in enumerate(source, 1):
            try:
                events.append((line, json.loads(text)))
            except json.JSONDecodeError as error:
                raise ValueError(f'Invalid record at line {line}') from error
    if not events or events[0][1].get('type') != 'session_meta':
        raise ValueError('Missing session metadata')
    return events


def totals(sessions, field):
    result = Counter()
    for session in sessions:
        result.update(session[field])
    return dict(result)


def collect(root):
    sessions = []
    parents = {}
    seen = set()
    for path in sorted(root.rglob('*.jsonl')):
        with path.open(encoding='utf-8') as source:
            meta = json.loads(next(source))['payload']
        if not is_subyard_workspace(meta.get('cwd', '')):
            continue
        source = meta.get('source', {})
        parents[meta['id']] = (source.get('subagent', {}).get('thread_spawn', {}).get('parent_thread_id')
                               if isinstance(source, dict) else None)
        session = summarize(read_events(path), str(path.relative_to(root)), seen)
        if not session['usage'].get('total_tokens'):
            continue
        session['source_window'] = {'first': session.pop('_first'), 'last': session.pop('_last')}
        for key in list(session):
            if key.startswith('_'):
                session.pop(key)
        sessions.append(session)
    families = {}
    for session in sessions:
        ancestor = session['id']
        visited = set()
        while parents.get(ancestor):
            if ancestor in visited:
                raise ValueError('Cycle in session ancestry')
            visited.add(ancestor)
            ancestor = parents[ancestor]
        families.setdefault(ancestor, []).append(session)
    if not families:
        raise ValueError('No usage records in the selected interval')
    family_root, family_sessions = max(
        families.items(), key=lambda item: sum(s['usage']['total_tokens'] for s in item[1]))
    parent = next((s for s in family_sessions if s['id'] == family_root), None)
    observer = max(family_sessions, key=lambda s: s['wait_usage'].get('total_tokens', 0))
    snapshot = {
        'period': {'start_inclusive': START, 'end_exclusive': END, 'as_of_inclusive': AS_OF, 'timezone': 'UTC'},
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'method': 'Deduplicate token_usage_record by response_id; count input + output. '
                  'Associate tool calls preceding each usage record. Wait responses exclusively '
                  'invoke wait_agent, sleep or wait. Observation also includes direct empty-input '
                  'process polls and send_message. Inspect only matching Subyard workspace logs.',
        'cohort': {'session_count': len(sessions),
                   'response_count': sum(s['responses'] for s in sessions),
                   'usage': totals(sessions, 'usage'), 'wait_usage': totals(sessions, 'wait_usage')},
        'family': {'root_id': family_root, 'session_count': len(family_sessions),
                   'response_count': sum(s['responses'] for s in family_sessions),
                   'usage': totals(family_sessions, 'usage'),
                   'wait_usage': totals(family_sessions, 'wait_usage'),
                   'session_ids': [s['id'] for s in family_sessions]},
        'parent': parent, 'observer': observer,
        'sessions': [{key: session[key] for key in
                      ('id', 'parent_id', 'source_file', 'workspace', 'models',
                       'responses', 'usage', 'wait_usage')} for session in sessions],
        'limitations': [
            'The cohort includes locally available matching Codex logs, not all providers or all Yard work.',
            'The snapshot cutoff is frozen so active sessions do not change the reported figures.',
            'A family includes the lead and selected descendants; other-workspace descendants are outside this scan.',
            'wait_agent does not identify a child; waits can be for other agents.',
            'Wait-associated inference can contain reasoning; waiting itself does not generate model tokens.',
            'wait continues a yielded tool execution; it is distinct from wait_agent and sleep.',
            'Observation-associated responses may contain useful analysis; totals are not proven waste or savings.',
            'Cached input is a subset of input; reasoning output is a subset of output.',
            'Process-poll usage requires a single direct write_stdin call with empty input and a literal session ID, '
            'without loops or callbacks; dynamic tool execution is not reconstructed.',
            'CPU time, dollar cost, task success and avoidable spend are not measured.',
        ],
    }
    return snapshot


def public_snapshot(snapshot):
    """Copy only approved period fields and numeric aggregate metrics."""
    def usage(values):
        return {key: values.get(key, 0) for key in TOKEN_KEYS}

    public = {'period': {key: snapshot['period'][key] for key in
                         ('start_inclusive', 'end_exclusive', 'as_of_inclusive', 'timezone')}}
    for scope in ('cohort', 'family'):
        public[scope] = {key: snapshot[scope][key] for key in ('session_count', 'response_count')}
        for field in ('usage', 'wait_usage'):
            public[scope][field] = usage(snapshot[scope][field])
    observer = snapshot['observer']
    actions = ('wait', 'process_poll', 'send_message')
    public['observer'] = {
        'usage': usage(observer['usage']),
        'observation_usage': usage(observer['observation_usage']),
        'usage_by_action': {action: usage(observer['usage_by_action'].get(action, {}))
                            for action in actions},
        'response_counts': {action: observer['response_counts'].get(action, 0) for action in actions},
    }
    return public


def write_snapshot(snapshot, audit_output, output):
    """Keep detailed evidence outside the directory served as the presentation."""
    audit_output = audit_output.resolve()
    output = output.resolve()
    if audit_output == output or output in audit_output.parents:
        raise ValueError('Local audit output must be outside the presentation directory')
    audit_output.mkdir(parents=True, exist_ok=True)
    (audit_output / 'evidence.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
    serialized = json.dumps(public_snapshot(snapshot), indent=2) + '\n'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'data.json').write_text(serialized, encoding='utf-8')
    (output / 'data.js').write_text('window.USAGE_EVIDENCE = ' + serialized.rstrip() + ';\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sessions-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('presentation1-intro'))
    parser.add_argument('--audit-output', type=Path, default=Path('.local/usage-evidence'))
    args = parser.parse_args()
    snapshot = collect(args.sessions_root)
    write_snapshot(snapshot, args.audit_output, args.output)
    print(json.dumps({'cohort_tokens': snapshot['cohort']['usage']['total_tokens'],
                      'cohort_wait_tokens': snapshot['cohort']['wait_usage']['total_tokens'],
                      'family_tokens': snapshot['family']['usage']['total_tokens'],
                      'observer_observation_tokens': snapshot['observer']['observation_usage']['total_tokens']}))


if __name__ == '__main__':
    main()
