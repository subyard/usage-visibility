#!/usr/bin/env python3
"""Build a small, sanitized snapshot from two explicitly selected Codex logs."""

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex


PARENT_FILE = "2026/10/05/rollout-2026-10-05T14-05-23-01a10c62-2cf9-73f1-bb64-168f19cb794d.jsonl"
OBSERVER_FILE = "2026/10/05/rollout-2026-10-05T20-02-10-01a10da8-d27f-7cd1-af60-92091d6bc1b8.jsonl"
START = "2026-10-05T00:00:00.000Z"
END = "2026-10-07T00:00:00.000Z"
TEST_PACKAGE = "./internal/adapters/reconcileruntime"
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
                fields[token] = literal(tokens[j + 2])
            if token in ('{', '[', '('):
                depth += 1
            elif token in ('}', ']', ')'):
                depth -= 1
            j += 1
        yield tokens[i + 2], fields


def package_test(command):
    """Recognize a direct go test invocation, including after cd or env."""
    if not isinstance(command, str):
        return False
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=';&|')
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return False
    for i, token in enumerate(tokens):
        if token != 'go' or tokens[i + 1:i + 2] != ['test']:
            continue
        # A quoted mention in rg/sed/echo is not an invocation.
        before = max((j for j in range(i) if tokens[j] in (';', '&&', '||', '|')), default=-1)
        prefix = tokens[before + 1:i]
        if prefix and prefix[0] != 'env' and not all(re.fullmatch(r'\w+=.*', p) for p in prefix):
            continue
        after = next((j for j in range(i + 2, len(tokens)) if tokens[j] in (';', '&&', '||', '|')), len(tokens))
        if TEST_PACKAGE in tokens[i + 2:after]:
            return True
    return False


def summarize(events, filename):
    meta = events[0][1]['payload']
    if meta.get('cwd') != '/srv/workspaces/Subyard-2/src':
        raise ValueError('Selected log is not a Subyard-2 session')
    usage = Counter()
    wait_usage = Counter()
    calls = Counter()
    models = set()
    seen = set()
    pending = []
    tests = []
    wait_records = []
    usage_records = []
    tool_times = {}
    waits = []
    ignored_poll_inputs = 0
    for line, event in events:
        timestamp = event.get('timestamp', '')
        payload = event.get('payload', {})
        kind = payload.get('type')
        in_window = START <= timestamp < END
        if event.get('type') == 'turn_context' and in_window:
            models.add(payload['model'])
        if event.get('type') == 'response_item' and kind in ('function_call', 'custom_tool_call'):
            name = payload.get('name', '')
            pending.append(name)
            if in_window:
                calls[name] += 1
                if name == 'wait_agent':
                    tool_times[payload['call_id']] = (timestamp, line)
                if name == 'exec' and kind == 'custom_tool_call':
                    for tool, fields in tool_calls(payload.get('input', '')):
                        if tool == 'write_stdin':
                            if fields.get('chars', '') == '':
                                calls['process_poll'] += 1
                            else:
                                ignored_poll_inputs += 1
                        if tool == 'exec_command' and package_test(fields.get('cmd')):
                            tests.append({'timestamp': timestamp, 'line': line})
        if event.get('type') == 'token_usage_record':
            response_id = payload['response_id']
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
                    if pending and set(pending) <= {'wait_agent', 'sleep'}:
                        wait_usage.update(values)
                        wait_records.append({'timestamp': timestamp, 'line': line, 'usage': values})
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
        'agent_path': meta.get('agent_path'), 'usage': dict(usage), 'wait_usage': dict(wait_usage),
        'wait_calls': calls['wait_agent'], 'sleep_calls': calls['sleep'],
        'poll_calls': calls['process_poll'], 'non_poll_stdin_calls': ignored_poll_inputs,
        'message_calls': calls['send_message'], 'responses': len(usage_records),
        'test_runs': len(tests), 'test_label': f'go test {TEST_PACKAGE}',
        'test_method': 'Four go test commands for the internal/adapters/reconcileruntime package '
                       'on October 6 at 07:28, 10:05, 10:06 and 10:55 UTC. The -run selectors differed; '
                       'these are checks of one package, not four reruns of the same test.',
        'test_events': tests,
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


def collect(root):
    parent = summarize(read_events(root / PARENT_FILE), PARENT_FILE)
    observer = summarize(read_events(root / OBSERVER_FILE), OBSERVER_FILE)
    if observer['parent_id'] != parent['id'] or observer['agent_path'] != '/root/full_tests_luna':
        raise ValueError('Expected a child test observer session')
    begin, end = observer['_first'], observer['_last']
    overlap_usage = Counter()
    overlap_wait = Counter()
    for row in parent['_usage_records']:
        if begin <= row['timestamp'] <= end:
            overlap_usage.update(row['usage'])
    for row in parent['_wait_records']:
        if begin <= row['timestamp'] <= end:
            overlap_wait.update(row['usage'])
    overlap_waits = [row for row in parent['_waits'] if begin <= row['timestamp'] <= end]
    elapsed = (datetime.fromisoformat(end.replace('Z', '+00:00'))
               - datetime.fromisoformat(begin.replace('Z', '+00:00'))).total_seconds()
    snapshot = {
        'period': {'start_inclusive': START, 'end_exclusive': END, 'timezone': 'UTC'},
        'captured_at': datetime.now(timezone.utc).isoformat(),
        'method': 'Deduplicate token_usage_record by response_id; count input + output. '
                  'Associate tool calls preceding each usage record. Wait-only tool responses '
                  'have exclusively wait_agent/sleep calls. Embedded execution parsed as JS '
                  'tokens; only literal cmd fields of tools.exec_command considered for tests.',
        'parent': parent, 'observer': observer,
        'observer_interval': {'start': begin, 'end': end, 'elapsed_seconds': elapsed,
                              'parent_usage': dict(overlap_usage), 'parent_wait_usage': dict(overlap_wait),
                              'wait_calls': len(overlap_waits),
                              'wait_seconds': round(sum(row['seconds'] for row in overlap_waits), 3)},
        'limitations': [
            'One pair of sessions, not a sample of all Yard work.',
            'wait_agent does not identify a child; waits can be for other agents.',
            'Wait-associated inference can contain reasoning; waiting itself does not generate model tokens.',
            'Wait duration includes wait_agent calls only; wait-associated token totals also include sleep.',
            'Cached input is a subset of input; reasoning output is a subset of output.',
            'Embedded write_stdin count means literal empty-input call sites recorded in exec bodies; '
            'dynamic executions/loops are not reconstructed.',
            'Repeated package checks have different -run selectors; necessity is not established.',
            'CPU time, dollar cost, task success and avoidable spend are not measured.',
        ],
    }
    for session in (parent, observer):
        session['source_window'] = {'first': session.pop('_first'), 'last': session.pop('_last')}
        for key in list(session):
            if key.startswith('_'):
                session.pop(key)
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sessions-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('presentation1-intro'))
    args = parser.parse_args()
    snapshot = collect(args.sessions_root)
    serialized = json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n'
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'evidence.json').write_text(serialized, encoding='utf-8')
    (args.output / 'evidence.js').write_text('window.USAGE_EVIDENCE = ' + serialized.rstrip() + ';\n', encoding='utf-8')
    print(json.dumps({'parent_tokens': snapshot['parent']['usage']['total_tokens'],
                      'wait_tokens': snapshot['parent']['wait_usage']['total_tokens'],
                      'polls': snapshot['observer']['poll_calls'],
                      'test_runs': snapshot['observer']['test_runs']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
