# MLflow

- **Link:** https://github.com/mlflow/mlflow
- **Version checked:** Current `/latest` documentation; no installed release tested. Cost tracking requires MLflow 3.10.0 or later with the `genai` extra.
- **Checked on:** 2026-10-12
- **License:** [Apache-2.0](https://github.com/mlflow/mlflow/blob/master/LICENSE)

## Summary

MLflow combines ML experiment tracking with GenAI tracing, usage analytics and
evaluation. Its documented integrations cover Claude Code, Codex and OpenCode,
making it a candidate for the agent side of usage visibility. System metrics
are available separately, but attributing test-process CPU and memory to an
agent step remains a gap.

## How it works

- [Claude Code](https://mlflow.org/docs/latest/genai/tracing/integrations/listing/claude_code/):
  a plugin or `mlflow autolog claude` configures hooks. Captures tools, model
  calls and nested subagents; exports a trace when the session ends.
- [Codex](https://mlflow.org/docs/latest/genai/tracing/integrations/listing/codex/):
  `@mlflow/codex` uses the `notify` hook and optionally reads the session
  transcript for tokens and tool activity. Exports after each turn. Setup
  refuses to overwrite an existing notifier.
- [OpenCode](https://mlflow.org/docs/latest/genai/tracing/integrations/listing/opencode/):
  `@mlflow/opencode` records turns when the session becomes idle, including
  tools, tokens and user/session metadata.
- [OTLP ingestion](https://mlflow.org/docs/latest/genai/tracing/opentelemetry/ingest/):
  the server also accepts OTLP/HTTP traces at `/v1/traces`, with a SQL backend.
  Native Codex OTLP describes internal execution; the hook gives a clearer
  conversation view. This endpoint is not a general metrics/logs backend.

## Reference scenarios

Initial assessment from documentation only; not observed on real runs.
✅ visible in standard views · ⚠️ needs a custom query or manual correlation ·
❌ data is missing.

| Scenario | Rating | Basis | How it shows, or what is missing |
| --- | --- | --- | --- |
| S1 Commands rerun without a change | ⚠️ | docs | Repeated tool spans show command activity and elapsed time. No documented code-change comparison or per-test process accounting; host metrics need a separate run. |
| S2 Lead model calls while waiting | ⚠️ | docs | Claude Code nests subagent activity. Relating lead calls to another agent's work requires inspection; equivalent Codex/OpenCode subagent linkage is not established by their guides. |
| S3 Polling without new information | ⚠️ | docs | Inspect repeated tool calls and their outputs. No documented standard check that a poll brought no new information. |
| S4 Long wait or blocker | ✅ | docs | Trace timeline and span duration expose long recorded steps. Idle time between turns and the reason for a wait need extra instrumentation. |
| S5 Spend without a successful outcome | ⚠️ | docs | Usage and cost can be compared with assessments. Task success must be supplied; trace execution status alone does not establish success. |

## Coverage

| Criterion | Rating | Basis | Notes |
| --- | --- | --- | --- |
| Agents | ✅ | docs | Official Claude Code, Codex and OpenCode integrations. |
| Env | ✅ | docs | Local tracking server and CLI plugins; no Subyard or root requirement. |
| Tokens | ⚠️ | docs | Per-span and trace input/output/total usage; Claude screenshot also shows cache read/write. Reasoning and consistent cache accounting across all three integrations need validation. |
| Attrib | ⚠️ | docs | Session/user metadata and tool/model spans; Claude Code has nested subagents. Full agent/subagent linkage across the other integrations is unverified. |
| Cost | ✅ | docs | Model-price estimates at span and trace level; depends on supported model names and reported usage. Subscription billing can differ. |
| Compute | ⚠️ | docs | Opt-in system CPU/memory metrics for MLflow runs. No standard per-test process tree or automatic link from CLI traces to those metrics. |
| Time | ⚠️ | docs | Step durations and trace timeline; delivery time, inter-turn waits and blockers need context. |
| Outcome | ⚠️ | docs | Human feedback and evaluation assessments can be attached to traces; a task-success definition and evidence must be supplied. |
| Setup | ✅ | docs | One local server with SQLite and agent-specific plugin/hook configuration gives an initial view. Compute/outcome correlation needs additional work. |
| Data | ✅ | docs | Local/self-hosted SQL and artifact storage; anonymous product telemetry can be disabled. |

Evidence: [trace UI](https://mlflow.org/docs/latest/genai/tracing/observe-with-traces/ui/),
[usage dashboard](https://mlflow.org/docs/latest/genai/tracing/observe-with-traces/dashboard/),
[token and cost tracking](https://mlflow.org/docs/latest/genai/tracing/token-usage-cost/),
[system metrics](https://mlflow.org/docs/latest/ml/tracking/system-metrics/).

## Minimal setup

For a future trial, create an isolated Python environment, install
`mlflow[genai]>=3.10.0`, and start a local tracking server with SQLite:

```sh
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db
```

Configure one agent integration against that server and an experiment. The
Claude Code SDK path uses `mlflow autolog claude`; Codex uses
`mlflow-codex setup` after installing `@mlflow/codex` (Node.js 18+). OpenCode
declares `@mlflow/opencode` in its configuration. These are trial instructions;
no agent configuration has been changed for this comparison.

Basic traces do not require custom code. Host metrics require `psutil` and an
explicit MLflow run with system logging enabled. Connecting those samples to
CLI sessions, collecting individual test processes, and recording task
outcomes would require glue or a separate collector.

## Data and privacy

Traces include prompt/response content, tool inputs/outputs and identifying
session metadata. Keep the server, SQL database and artifacts local for the
initial trial; shared deployment needs deliberate access configuration.
See [tracking server storage](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/)
and [authentication](https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/).

Open-source MLflow has anonymous product usage telemetry enabled by default
since 3.2.0. Set `MLFLOW_DISABLE_TELEMETRY=true` in each relevant process,
including the server, for a local-only trial; see
[usage tracking](https://mlflow.org/docs/latest/community/usage-tracking/).
The presentation uses public project screenshots, not local session data.

## Trial notes

Not tried. Pin the server and plugin versions before a real-run trial. Check
cache/reasoning token totals without double counting, Codex/OpenCode subagent
linkage, export delays, host-metric correlation and task-success assessments.

## Verdict

Keep MLflow in the comparison as an agent-tracing and evaluation candidate.
Its light local setup and coverage of all three CLIs justify a trial. Combine
it with process-level observation if selected; built-in host metrics alone
do not satisfy the compute attribution requirement.
