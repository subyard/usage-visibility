# Requirements and decisions

This file records what the solution must do and the decisions that shape the
work. The [README](../README.md) is the short human introduction; candidate
tools are compared in [`solutions/`](../solutions/README.md).

Add a decision when a choice constrains later work. Do not rewrite old
decisions: mark them as superseded and add a new entry.

## Requirements

### Primary goal

A person can quickly see where a pipeline is inefficient, whatever the
resource. Waste is not only tokens: an agent that reruns the same tests may
use few tokens but a lot of compute and time. Tokens, compute and time must be
visible side by side for each step, so a step that is cheap in one dimension
but expensive in another still stands out.

### Must have

- **Works without Subyard.** Runs in ordinary environments: a local
  repository, a terminal session or a standard devcontainer running Codex,
  Claude Code or OpenCode.
- **Tokens:** input, cached input, output and reasoning output per model,
  counted without double counting (cached input is part of input; reasoning
  output is part of output).
- **Compute:** CPU, memory and the processes involved in a task, including
  test runs; elapsed time separate from CPU time.
- **Time to delivery:** active work, waiting and blockers are visible on a
  timeline.
- **Attribution:** tokens, processes and time can be traced from a task to an
  agent or subagent and to the step or tool call that caused them.
- **Inefficiency signals:** known patterns are easy to spot without reading
  raw logs, for example:
  - tests or other commands rerun without a code or environment change;
  - a lead agent repeatedly calling its model while waiting for another agent;
  - frequent process polling or status messages without new information;
  - long waits or blockers on the path to delivery;
  - high resource use without a successful outcome.

### Should have

- **Cost:** estimated inference cost from model pricing on the request date,
  kept separate from actual billing.
- **Outcome:** whether the task succeeded and what evidence supports it.

### Constraints

- Prefer configuration of existing tools over new code.
- Detailed session data stays local by default; publish only aggregates.

## Decisions

### D1. Evaluate existing tools before building anything

2026-10-08 · Accepted

The problem is general and existing tools likely cover most of it. We compare
candidates in `solutions/` before implementing. Custom work is limited to
configuration and thin glue for gaps that no candidate covers. A combination of
tools is acceptable if each covers part of the requirements.

### D2. Subyard is a reference environment, not a dependency

2026-10-08 · Accepted

Subyard provides a reference implementation and real sessions for evaluation.
The chosen solution must work without it. Subyard is public and can be cited.

### D3. Audience and document roles

2026-10-08 · Accepted

The repository is public. It is written for people working on visibility of
agent pipelines, including people outside this team who want a short view of
the problem, the comparison and the conclusion.

- `README.md`: problem, current status and where to look.
- `docs/decisions.md`: requirements and decisions (this file).
- `solutions/`: comparison of candidate tools, one file per candidate.
- `presentation1-intro/`: intro presentation and its evidence.

### D4. Publish aggregate metrics only

2026-10-06 · Accepted

The presentation uses an allowlisted aggregate export (`data.json`). The
detailed audit with session identifiers stays in `.local/usage-evidence/`,
which is ignored by Git.

An earlier commit (`b74171d`) published two detailed session entries: session
IDs, log file names, model names, an agent path and a test command. A review
on 2026-10-08 found no keys, tokens or other secrets in the history, so it is
kept unchanged.

### D5. The intro audit is a one-off sample

2026-10-08 · Accepted

`scripts/collect_evidence.py` reproduces the October 5–6 audit from Codex logs
of a separate Subyard instance with many agents. Those logs are not part of
this repository or this environment, so the figures cannot be regenerated
here. The script is not the basis for the general solution.

### D6. Judge candidates by how fast they reveal inefficiency

2026-10-08 · Accepted

Token totals alone miss waste that shows up in compute or time, such as tests
rerun in a loop. Candidates are evaluated against reference scenarios in
[`solutions/`](../solutions/README.md#reference-scenarios): can a person see
each problem quickly, and in which resource it appears? Compute and time are
must-have requirements alongside tokens.
