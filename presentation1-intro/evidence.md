# Session audit: a Subyard sample for a general agent workflow problem

This audit uses locally available Codex logs from October 5–6, 2026. The
reported interval is `[2026-10-05 00:00:00, 2026-10-07 00:00:00)` UTC, with an
inclusive snapshot cutoff of `2026-10-06 23:27:43 UTC`. It is a bounded sample
from matching Subyard workspaces, not a measure of all Subyard activity or all
agent use. The product direction is broader: explain resource use in ordinary
agent workflows and work across environments without requiring Subyard.

## Cohort result

The scan checked session metadata first and selected logs whose working
directory matched the Subyard workspace root filter. It found 631 matching
log files; 179 contained
at least one model usage record in the reporting interval. Event timestamps,
not log filenames or creation dates, determine inclusion. This includes a
session started on October 3 whose log contributed five usage records during
the interval. Other workspaces and providers are outside this cohort.

Across 26,330 unique model responses, recorded input plus output was
2,874,272,332 tokens. Cached input is included in input, and reasoning output
is included in output.

| Model response category | Responses | Input + output tokens |
| --- | ---: | ---: |
| `wait_agent` | 2,106 | 233,202,116 |
| `sleep` | 1,580 | 175,547,751 |
| `wait` | 2,133 | 256,842,423 |
| **All three waiting categories** | **5,819** | **665,592,290** |
| All cohort responses | 26,330 | 2,874,272,332 |

The three waiting categories account for 23.16% of cohort input-plus-output
tokens. In their 664,746,447 input tokens, 660,457,728 were cached. These are
token volumes associated with model responses that invoke a waiting tool; they
are not tokens generated while a tool is blocked, a dollar cost estimate, or
proof that the work was avoidable.

The tool categories have distinct meanings. `wait_agent` waits for an agent;
its arguments do not identify which child returns. `sleep` pauses for a set
period. `wait` continues a yielded tool execution. Combining them gives a
useful view of model activity around waiting, but it does not make them the
same operation.

## Largest related session family

One root session and 19 selected descendants from the same matching workspace
form the largest family in this scan. The family contains 9,194 usage
responses and 1,096,196,283 total tokens; 295,123,384 tokens are associated
with the three waiting categories. The collector selects the family with the
largest recorded token total, without hardcoded session identifiers.

| Family wait category | Input + output tokens |
| --- | ---: |
| `wait_agent` | 65,877,366 |
| `sleep` | 45,253,400 |
| `wait` | 183,992,618 |
| **All three** | **295,123,384** |

This family is a tree of recorded parent links among sessions that passed the
workspace filter. Descendants whose working directories do not match that
filter are not included.

## Remote-check session

The session with the most wait-associated tokens in the selected family is
a remote-check agent. It recorded 300,819,073 tokens in total. Of these,
154,174,122 belong to 1,051 model responses that continue a yielded tool with
`wait`.

The session also has 226,877,594 tokens associated with tool waiting and
observation actions, or 75.42% of its total:

| Response category | Responses | Input + output tokens |
| --- | ---: | ---: |
| `wait` tool continuation | 1,051 | 154,174,122 |
| Direct process poll | 162 | 22,992,970 |
| `send_message` | 345 | 49,710,502 |
| **Observation-associated responses** | **1,558** | **226,877,594** |

Of the 345 coordination messages, 343 target the lead and two target a peer.
Messages can contain findings or useful instructions; they are not necessarily
redundant status reports. This session supports a remote package-review/check
example, not a count of identical test reruns.

The 162 process-poll responses meet a conservative rule: the recorded tool
body contains exactly one direct `write_stdin` call, with empty input and a
literal session ID, and has no loop or callback. The parser also finds 288
literal empty-input `write_stdin` call expressions across embedded tool
bodies. That is a static call-site count, not 288 confirmed distinct process
polls; only the 162 qualifying responses are used for token attribution.

Observation-associated model activity can contain useful work. The 75.42%
figure is neither evidence of waste nor a savings estimate. This audit did not
measure CPU time, elapsed test time, task success, or dollar cost.

## Accounting and reproduction

Public aggregate metrics are in [`data.json`](data.json); the presentation
loads the same metrics from `data.js`. Rebuild from locally available logs:

```sh
python3 scripts/collect_evidence.py --sessions-root /path/to/local/session-logs
```

The collector selects by `session_meta.cwd`, then filters usage records by
event timestamp and the fixed cutoff. It requires each usage record's
`thread_id` to match its session metadata and deduplicates once across the
selected logs by `(thread_id, response_id)`. It sums `token_usage_record.payload.usage`
once per key; `total_tokens` equals input plus output. Cached input and
reasoning output are subsets and are not added again. The frozen cohort had no
duplicate keys or cross-thread usage records.

A response is associated with waiting when the tool calls preceding its usage
record consist only of `wait_agent`, `sleep`, and/or `wait`. A response with an
unrelated tool action is excluded from the waiting total. This attributes the
model response that invokes a wait operation; the waiting interval itself
does not generate model tokens.

For process polling, the parser reads embedded JavaScript without executing
it, recognizes direct literal tool calls, and applies the conservative rule
above. It does not reconstruct dynamic code, loops, or callbacks.
The public export uses an explicit allowlist: the reporting period, aggregate
token counts, session/response counts, and the featured agent's three action
categories. It contains no session IDs, parent links, source paths, workspace
names, internal role labels, per-session rows, raw session text, command output,
credentials, or configuration.
This script reproduces the selected audit; it is not a general-purpose usage
collector.

The detailed audit is generated at `.local/usage-evidence/evidence.json`, which
is ignored by Git and kept outside the served presentation directory. It
contains session identifiers and operational metadata and should stay local.
The collector refuses to write this audit inside the presentation directory.
The presentation and PDF use only the public export. No local audit is needed
to view a fresh checkout or open the slides offline.

Ignoring files does not remove versions already in Git history. Removing old
history is a separate repository-owner decision.

## Existing capabilities and project direction

Subyard provides a useful source for this sample. Its AI Observer integration
reads Claude Code and Codex session files; its documented file-based
integration does not collect OpenCode or pi. `yard usage` forwards arguments
to `ccusage`, which reports usage but does not provide universal step-to-result
attribution. This context comes from Subyard's AI Observer documentation and
usage-command tests.

Usage Visibility is intended to help with ordinary agent workflows beyond
Subyard, including common devcontainer setups. A portable view that connects
model steps, tool/process activity, elapsed time, and outcomes across providers
is a project goal, not a capability this Subyard integration already supplies.
