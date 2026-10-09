# Usage Visibility

Usage Visibility explores and compares ways to understand resource use in
agentic software development. The goal is to provide simple, clear and reliable
metrics that help people see where resources go, identify bottlenecks and
evaluate the cost of a useful outcome.

The intended solution works across agent tools and development environments,
including standard devcontainers running Codex, Claude Code or OpenCode.
[Subyard](https://github.com/subyard/subyard) provides a reference
implementation and real examples for evaluation;
the solution should be usable independently of Subyard.

## What we want to measure

- **Tokens and inference cost:** input, cached input and output, attributed to
  the agents and steps that used them.
- **Compute resources:** CPU, memory and the processes involved in the task,
  including test execution.
- **Time to delivery:** active work, waiting and blockers on the path to a result.
- **Task outcome:** whether the task was solved successfully and what evidence
  supports that result.

These measurements should help explain patterns such as a lead agent repeatedly
invoking its model while waiting for a test observer, frequent process polling,
or tests being rerun without a new reason. Waste does not always show in
tokens: a test loop can cost little inference but a lot of compute and time.
The aim is to make those patterns easy to spot in any resource and to compare
improvements across workflows.

## Status

We are comparing existing tools before building anything. Results and the
current shortlist are in [`solutions/`](solutions/README.md).

## Where to look

- [Intro presentation](presentation1-intro/usage-visibility.pdf) — the problem,
  with figures from a sample of real agent sessions.
- [Candidate tools presentation](presentation2-solutions/usage-visibility-candidates.pdf) —
  what each shortlisted tool shows, how our goals map onto it, and other
  options.
- [Solution comparison](solutions/README.md) — candidate tools against shared
  criteria.
- [Requirements and decisions](docs/decisions.md) — what the solution must do
  and why the work is shaped this way.

Run the tests with `python3 -m unittest discover -s tests`.
