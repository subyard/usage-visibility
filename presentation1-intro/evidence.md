# Examples from Subyard sessions, October 5–6, 2026

Period: `[2026-10-05 00:00:00, 2026-10-07 00:00:00)` UTC.
This is one connected case drawn from two Codex session logs in Yard, not a
share of all Subyard costs over two days. Only aggregates are retained in the
repository; session text, command output, configuration, and credentials are
not copied.

## Main agent waiting

Session log path relative to the Codex `sessions` directory:

`2026/10/05/rollout-2026-10-05T14-05-23-01a10c62-2cf9-73f1-bb64-168f19cb794d.jsonl`

Working copy: `Subyard-2/src`. Model: `gpt-6.1-sol`.
The log contains 1,247 unique model usage records.

| Measure | All responses | Responses associated with waiting |
| --- | ---: | ---: |
| Input | 126,869,158 | 59,051,146 |
| Cached input, included in input | 124,111,744 | 58,311,936 |
| Output | 528,498 | 151,602 |
| Reasoning, included in output | 283,603 | 123,366 |
| Input + output | 127,397,656 | 59,202,748 |

Share: `59,202,748 / 127,397,656 × 100 = 46.47%`.
There were 571 `wait_agent` calls and one `sleep`. Cached input accounts for
98.75% of the input tokens in responses associated with waiting. Therefore,
the token share is not the dollar cost share.

Example event sequence: line 176 is a `wait_agent` call, line 177 is a
`token_usage_record`, and line 179 is the result of that call. Usage is
recorded before the tool result, so we count the model response that invokes
the wait. The blocked wait itself does not generate model tokens.

During the lifetime of the child test session (October 5, 20:02:10–October 6,
11:37:31 UTC), the log records 466 `wait_agent` calls with a combined duration
of 19,002.548 seconds—about 5 hours and 17 minutes, or 33.86% of the 56,120.926
second interval. This is time inside `wait_agent`, not CPU time or inference
time. One `sleep` call in this interval contributes to the waiting-token total,
but not to the duration above. The `wait_agent` arguments do not identify a
specific child agent; the waits may have been for other agents as well.

## Test agent and repeated checks

Child session log:

`2026/10/05/rollout-2026-10-05T20-02-10-01a10da8-d27f-7cd1-af60-92091d6bc1b8.jsonl`

Model: `gpt-6-luna`; role: `/root/full_tests_luna`. The `session_meta` record
links this log to the main session through `parent_thread_id`.

- 505 `tools.write_stdin` calls with empty input. For this specific log, each
  is confirmed to be in a separate `exec`, with no loops or callbacks, and to
  use a literal process identifier. These are polls, not 505 test launches.
- 386 `send_message` calls.
- Four `go test` commands for `./internal/adapters/reconcileruntime`.
  The `-run` filters differed: these tested the same package, not one
  unchanged set of tests.

| Time UTC, October 6, 2026 | Child log line |
| --- | ---: |
| 07:28:00 | 7,758 |
| 10:05:27 | 10,184 |
| 10:06:24 | 10,212 |
| 10:55:28 | 11,335 |

The number of checks is a signal to investigate. To conclude that a run was
unnecessary, compare the commit and file contents, parameters, environment,
and previous result. A rerun after a change, error, or flaky test may be
needed. This data slice did not assess whether the runs were necessary, and it
did not measure test duration, CPU usage, dollar cost, task success, or
potential savings.

## Method and reproduction

`scripts/collect_evidence.py` reads only the two specified files. All numbers
are saved in `presentation1-intro/evidence.json`; `evidence.js` contains the same data
for opening the presentation standalone through `file://`.

1. Select events by UTC time; verify the working copy and parent/child link.
2. Sum `token_usage_record.payload.usage` by unique `response_id`. Check
   `thread_id` within each log.
3. Associate a response with waiting if all tool calls before its usage record
   are `wait_agent` or `sleep`. A response may include reasoning.
4. Measure wait duration as the difference between the call and result with
   the same `call_id`.
5. Extract nested `tools` calls from JavaScript tokens without executing code.
   For tests, parse only literal `cmd` values in `tools.exec_command`. Exclude
   quoted text, comments, and read commands that mention `go test`.

Cached input is already included in input, and reasoning is already included
in output. Do not add either a second time. `event_msg.token_count` can repeat
and lag behind: the latest count here is 125,379,436, while the sum of
individual usage records and the latest `thread_token_usage` agree at
127,397,656. Do not add the two formats together.

```sh
python3 scripts/collect_evidence.py --sessions-root /home/dev/.codex/sessions
python3 -m unittest discover -s tests
```

The parser reproduces this case; it is not a universal collector. It counts
literal direct calls recorded in JavaScript. Dynamic calls, interpolated
templates, and loops are not reconstructed. Changes to the log format require
methodology review before updating the findings.

## Project brief and current capabilities

- `input/goal.md` — Usage Visibility project brief: tokens/cost, compute, time
  to outcome, and success; applicability beyond Subyard.
- `/srv/workspaces/Subyard-4/src/docs/ai-observer.md` — AI Observer reads
  Codex and Claude Code logs through read-only mounts; OpenCode/pi are not
  collected through this mechanism.
- `/srv/workspaces/Subyard-4/src/tests/yard-usage.sh` and
  `internal/cli/cli.go` — `yard usage` passes arguments and the exit code to
  ccusage; this is not a universal step-attribution system.

A complete pipeline, attribution of costs to outcomes, and portable adapters
are project goals, not capabilities that this repository already provides.
