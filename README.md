# Usage Visibility

Usage Visibility explores and compares ways to understand resource use in
agentic software development. The goal is to provide simple, clear and reliable
metrics that help people see where resources go, identify bottlenecks and
evaluate the cost of a useful outcome.

The intended solution works across agent tools and development environments,
including standard devcontainers running Codex, Claude Code or OpenCode.
Subyard provides a reference implementation and real examples for evaluation;
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
or tests being rerun without a new reason. The aim is to make those patterns
reviewable and compare improvements across workflows.

[Intro presentation](presentation1-intro/usage-visibility.pdf)
