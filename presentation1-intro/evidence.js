window.USAGE_EVIDENCE = {
  "period": {
    "start_inclusive": "2026-10-05T00:00:00.000Z",
    "end_exclusive": "2026-10-07T00:00:00.000Z",
    "timezone": "UTC"
  },
  "captured_at": "2026-10-06T23:17:38.170961+00:00",
  "method": "Deduplicate token_usage_record by response_id; count input + output. Associate tool calls preceding each usage record. Wait-only tool responses have exclusively wait_agent/sleep calls. Embedded execution parsed as JS tokens; only literal cmd fields of tools.exec_command considered for tests.",
  "parent": {
    "id": "01a10c62-2cf9-73f1-bb64-168f19cb794d",
    "source_file": "2026/10/05/rollout-2026-10-05T14-05-23-01a10c62-2cf9-73f1-bb64-168f19cb794d.jsonl",
    "models": [
      "gpt-6.1-sol"
    ],
    "parent_id": null,
    "agent_path": null,
    "usage": {
      "input_tokens": 126869158,
      "cached_input_tokens": 124111744,
      "output_tokens": 528498,
      "reasoning_output_tokens": 283603,
      "total_tokens": 127397656
    },
    "wait_usage": {
      "input_tokens": 59051146,
      "cached_input_tokens": 58311936,
      "output_tokens": 151602,
      "reasoning_output_tokens": 123366,
      "total_tokens": 59202748
    },
    "wait_calls": 571,
    "sleep_calls": 1,
    "poll_calls": 17,
    "non_poll_stdin_calls": 0,
    "message_calls": 123,
    "responses": 1247,
    "test_runs": 0,
    "test_label": "go test ./internal/adapters/reconcileruntime",
    "test_method": "Four go test commands for the internal/adapters/reconcileruntime package on October 6 at 07:28, 10:05, 10:06 and 10:55 UTC. The -run selectors differed; these are checks of one package, not four reruns of the same test.",
    "test_events": [],
    "source_window": {
      "first": "2026-10-05T14:06:01.655Z",
      "last": "2026-10-06T13:19:10.574Z"
    }
  },
  "observer": {
    "id": "01a10da8-d27f-7cd1-af60-92091d6bc1b8",
    "source_file": "2026/10/05/rollout-2026-10-05T20-02-10-01a10da8-d27f-7cd1-af60-92091d6bc1b8.jsonl",
    "models": [
      "gpt-6-luna"
    ],
    "parent_id": "01a10c62-2cf9-73f1-bb64-168f19cb794d",
    "agent_path": "/root/full_tests_luna",
    "usage": {
      "input_tokens": 194896621,
      "cached_input_tokens": 192784384,
      "output_tokens": 289008,
      "reasoning_output_tokens": 69316,
      "total_tokens": 195185629
    },
    "wait_usage": {
      "input_tokens": 8268893,
      "cached_input_tokens": 8192000,
      "output_tokens": 3640,
      "reasoning_output_tokens": 1716,
      "total_tokens": 8272533
    },
    "wait_calls": 3,
    "sleep_calls": 93,
    "poll_calls": 505,
    "non_poll_stdin_calls": 0,
    "message_calls": 386,
    "responses": 1880,
    "test_runs": 4,
    "test_label": "go test ./internal/adapters/reconcileruntime",
    "test_method": "Four go test commands for the internal/adapters/reconcileruntime package on October 6 at 07:28, 10:05, 10:06 and 10:55 UTC. The -run selectors differed; these are checks of one package, not four reruns of the same test.",
    "test_events": [
      {
        "timestamp": "2026-10-06T07:28:00.164Z",
        "line": 7758
      },
      {
        "timestamp": "2026-10-06T10:05:27.939Z",
        "line": 10184
      },
      {
        "timestamp": "2026-10-06T10:06:24.648Z",
        "line": 10212
      },
      {
        "timestamp": "2026-10-06T10:55:28.619Z",
        "line": 11335
      }
    ],
    "source_window": {
      "first": "2026-10-05T20:02:10.252Z",
      "last": "2026-10-06T11:37:31.178Z"
    }
  },
  "observer_interval": {
    "start": "2026-10-05T20:02:10.252Z",
    "end": "2026-10-06T11:37:31.178Z",
    "elapsed_seconds": 56120.926,
    "parent_usage": {
      "input_tokens": 79864718,
      "cached_input_tokens": 78383360,
      "output_tokens": 284474,
      "reasoning_output_tokens": 163437,
      "total_tokens": 80149192
    },
    "parent_wait_usage": {
      "input_tokens": 48081168,
      "cached_input_tokens": 47519104,
      "output_tokens": 109849,
      "reasoning_output_tokens": 88151,
      "total_tokens": 48191017
    },
    "wait_calls": 466,
    "wait_seconds": 19002.548
  },
  "limitations": [
    "One pair of sessions, not a sample of all Yard work.",
    "wait_agent does not identify a child; waits can be for other agents.",
    "Wait-associated inference can contain reasoning; waiting itself does not generate model tokens.",
    "Wait duration includes wait_agent calls only; wait-associated token totals also include sleep.",
    "Cached input is a subset of input; reasoning output is a subset of output.",
    "Embedded write_stdin count means literal empty-input call sites recorded in exec bodies; dynamic executions/loops are not reconstructed.",
    "Repeated package checks have different -run selectors; necessity is not established.",
    "CPU time, dollar cost, task success and avoidable spend are not measured."
  ]
};
