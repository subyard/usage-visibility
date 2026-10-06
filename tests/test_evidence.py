import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect_evidence import is_subyard_workspace, public_snapshot, summarize, tool_calls, write_snapshot


class EvidenceTests(unittest.TestCase):
    def test_usage_is_deduplicated_without_adding_cached_or_reasoning_tokens(self):
        timestamp = '2026-10-05T20:00:00.000Z'
        meta = {'type': 'session_meta', 'timestamp': timestamp,
                'payload': {'id': 'parent', 'cwd': '/srv/workspaces/Subyard-2/src'}}
        usage = {'type': 'token_usage_record', 'timestamp': timestamp,
                 'payload': {'thread_id': 'parent', 'response_id': 'response-1',
                             'usage': {'input_tokens': 100, 'cached_input_tokens': 90,
                                       'output_tokens': 10, 'reasoning_output_tokens': 5,
                                       'total_tokens': 110}}}
        call = {'type': 'response_item', 'timestamp': timestamp,
                'payload': {'type': 'function_call', 'name': 'wait_agent', 'call_id': 'wait-1'}}
        result = summarize(list(enumerate([meta, call, usage, usage], 1)), 'fixture')
        self.assertEqual(result['usage']['total_tokens'], 110)
        self.assertEqual(result['wait_usage']['total_tokens'], 110)
        self.assertEqual(result['responses'], 1)

    def test_mixed_work_and_wait_response_is_not_attributed_to_wait_only(self):
        timestamp = '2026-10-05T20:00:00.000Z'
        events = [
            {'type': 'session_meta', 'timestamp': timestamp,
             'payload': {'id': 'parent', 'cwd': '/srv/workspaces/Subyard-2/src'}},
            {'type': 'response_item', 'timestamp': timestamp,
             'payload': {'type': 'function_call', 'name': 'wait_agent', 'call_id': 'wait-1'}},
            {'type': 'response_item', 'timestamp': timestamp,
             'payload': {'type': 'custom_tool_call', 'name': 'exec', 'input': ''}},
            {'type': 'token_usage_record', 'timestamp': timestamp,
             'payload': {'thread_id': 'parent', 'response_id': 'response-1',
                         'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}},
        ]
        result = summarize(list(enumerate(events, 1)), 'fixture')
        self.assertEqual(result['usage']['total_tokens'], 110)
        self.assertEqual(result['wait_usage'].get('total_tokens', 0), 0)

    def test_js_mentions_are_not_tool_calls(self):
        code = '''
          // tools.write_stdin({session_id: 1});
          const note = "tools.write_stdin({session_id: 2})";
          await tools.exec_command({cmd: "go test ./example", yield_time_ms: 1000});
          await tools.write_stdin({session_id: 3, chars: ""});
        '''
        calls = list(tool_calls(code))
        self.assertEqual([name for name, _ in calls], ['exec_command', 'write_stdin'])
        self.assertEqual(calls[1][1]['session_id'], 3)
        self.assertEqual(calls[1][1]['chars'], '')
        quoted = list(tool_calls('await tools.write_stdin({"session_id": 3, "chars": ""});'))
        self.assertEqual(quoted[0][1], {'session_id': 3, 'chars': ''})

    def test_workspace_filter_excludes_private_and_unrelated_sessions(self):
        self.assertTrue(is_subyard_workspace('/srv/workspaces/Subyard-4/src'))
        self.assertTrue(is_subyard_workspace('/srv/workspaces/subyard-3/src'))
        self.assertFalse(is_subyard_workspace('/srv/workspaces/Subyard-4/src/private'))
        self.assertFalse(is_subyard_workspace('/srv/workspaces/usage-visibility/src'))

    def test_tool_continuation_uses_the_same_deduplication_and_cutoff(self):
        timestamp = '2026-10-06T23:27:42.000Z'
        events = [
            {'type': 'session_meta', 'timestamp': timestamp,
             'payload': {'id': 'parent', 'cwd': '/srv/workspaces/Subyard-2/src'}},
            {'type': 'response_item', 'timestamp': timestamp,
             'payload': {'type': 'function_call', 'name': 'wait', 'call_id': 'wait-1'}},
            {'type': 'token_usage_record', 'timestamp': timestamp,
             'payload': {'thread_id': 'parent', 'response_id': 'response-1',
                         'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}},
            {'type': 'token_usage_record', 'timestamp': '2026-10-06T23:27:44.000Z',
             'payload': {'thread_id': 'parent', 'response_id': 'response-2',
                         'usage': {'input_tokens': 100, 'output_tokens': 10, 'total_tokens': 110}}},
        ]
        seen = set()
        first = summarize(list(enumerate(events, 1)), 'fixture-a', seen)
        second = summarize(list(enumerate(events, 1)), 'fixture-b', seen)
        self.assertEqual(first['usage']['total_tokens'], 110)
        self.assertEqual(first['wait_usage']['total_tokens'], 110)
        self.assertEqual(second['usage'].get('total_tokens', 0), 0)

    def test_wrong_thread_is_rejected(self):
        events = [(1, {'type': 'session_meta', 'payload': {'id': 'parent', 'cwd': '/srv/workspaces/Subyard-2/src'}}),
                  (2, {'type': 'token_usage_record', 'payload': {'thread_id': 'child', 'response_id': 'r'}})]
        with self.assertRaises(ValueError):
            summarize(events, 'fixture')

    def test_snapshot_and_offline_data_agree(self):
        root = Path(__file__).resolve().parents[1] / 'presentation1-intro'
        data = json.loads((root / 'data.json').read_text())
        javascript = (root / 'data.js').read_text()
        self.assertEqual(data, json.loads(javascript.removeprefix('window.USAGE_EVIDENCE = ').rstrip().removesuffix(';')))
        self.assertEqual(data['cohort']['usage']['total_tokens'], 2874272332)
        self.assertEqual(data['cohort']['wait_usage']['total_tokens'], 665592290)
        self.assertEqual(data['cohort']['session_count'], 179)
        self.assertEqual(data['family']['session_count'], 20)
        self.assertEqual(data['family']['usage']['total_tokens'], 1096196283)
        observer = data['observer']
        observation = sum(observer['usage_by_action'][key]['total_tokens']
                          for key in ('wait', 'process_poll', 'send_message'))
        self.assertEqual(observation, observer['observation_usage']['total_tokens'])
        self.assertEqual(observation, 226877594)
        self.assertEqual(observer['response_counts']['process_poll'], 162)

    def test_public_export_excludes_private_metadata_and_unknown_fields(self):
        root = Path(__file__).resolve().parents[1] / 'presentation1-intro'
        data = json.loads((root / 'data.json').read_text())
        snapshot = json.loads(json.dumps(data))
        snapshot['period']['local_path'] = 'PRIVATE_CANARY'
        snapshot['family']['root_id'] = 'PRIVATE_CANARY'
        snapshot['family']['session_ids'] = ['PRIVATE_CANARY']
        snapshot['sessions'] = [{'source_file': 'PRIVATE_CANARY'}]
        snapshot['observer']['agent_path'] = 'PRIVATE_CANARY'
        snapshot['observer']['usage_by_action']['send_message']['secret'] = 'PRIVATE_CANARY'
        snapshot['observer']['response_counts']['internal_tool'] = 1
        public = public_snapshot(snapshot)
        self.assertEqual(public, data)
        self.assertNotIn('PRIVATE_CANARY', json.dumps(public))
        with TemporaryDirectory() as directory:
            audit = Path(directory) / 'local'
            presentation = Path(directory) / 'presentation'
            write_snapshot(snapshot, audit, presentation)
            self.assertIn('PRIVATE_CANARY', (audit / 'evidence.json').read_text())
            self.assertNotIn('PRIVATE_CANARY', (presentation / 'data.json').read_text())
            self.assertEqual({p.name for p in presentation.iterdir()}, {'data.json', 'data.js'})

    def test_local_audit_cannot_be_written_into_the_presentation(self):
        with TemporaryDirectory() as directory:
            presentation = Path(directory) / 'presentation'
            for audit in (presentation, presentation / 'local'):
                with self.assertRaises(ValueError):
                    write_snapshot({}, audit, presentation)
            self.assertFalse(presentation.exists())


if __name__ == '__main__':
    unittest.main()
