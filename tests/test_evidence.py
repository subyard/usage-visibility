import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect_evidence import package_test, summarize, tool_calls


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
          await tools.exec_command({cmd: "go test ./internal/adapters/reconcileruntime", yield_time_ms: 1000});
          await tools.write_stdin({session_id: 3, chars: ""});
        '''
        calls = list(tool_calls(code))
        self.assertEqual([name for name, _ in calls], ['exec_command', 'write_stdin'])
        self.assertEqual(calls[1][1]['session_id'], 3)
        self.assertEqual(calls[1][1]['chars'], '')

    def test_package_test_excludes_quotes_and_other_packages(self):
        self.assertTrue(package_test('go test -count=1 ./internal/adapters/reconcileruntime -run "^TestFoo$"'))
        self.assertTrue(package_test('cd /repo && go test ./internal/adapters/reconcileruntime'))
        self.assertFalse(package_test('rg "go test ./internal/adapters/reconcileruntime" README.md'))
        self.assertFalse(package_test('echo go test ./internal/adapters/reconcileruntime'))
        self.assertFalse(package_test('go test ./internal/adapters/releaseruntime'))
        self.assertFalse(package_test('cat ./internal/adapters/reconcileruntime/file.go'))

    def test_wrong_thread_is_rejected(self):
        events = [(1, {'type': 'session_meta', 'payload': {'id': 'parent', 'cwd': '/srv/workspaces/Subyard-2/src'}}),
                  (2, {'type': 'token_usage_record', 'payload': {'thread_id': 'child', 'response_id': 'r'}})]
        with self.assertRaises(ValueError):
            summarize(events, 'fixture')

    def test_snapshot_and_offline_data_agree(self):
        root = Path(__file__).resolve().parents[1] / 'presentation1-intro'
        data = json.loads((root / 'evidence.json').read_text())
        javascript = (root / 'evidence.js').read_text()
        self.assertEqual(data, json.loads(javascript.removeprefix('window.USAGE_EVIDENCE = ').rstrip().removesuffix(';')))
        self.assertEqual(data['parent']['usage']['total_tokens'], 127397656)
        self.assertEqual(data['parent']['wait_usage']['total_tokens'], 59202748)
        self.assertEqual(data['observer']['poll_calls'], 505)
        self.assertEqual(data['observer']['test_runs'], 4)


if __name__ == '__main__':
    unittest.main()
