# AgentSight

- **Link:** https://github.com/eunomia-bpf/agentsight
- **Version checked:**
- **Checked on:** YYYY-MM-DD
- **License:** MIT

## Summary

Two or three sentences: what it is, what it covers well, and the verdict.

## How it works

From the README, not yet tried: a local Linux tool that observes the agent
from outside with eBPF, without an SDK or proxy. It captures LLM traffic at
TLS calls, process spawns, file and network activity, and CPU and memory, and
correlates them per session. `agentsight record -- <command>` saves a session
to a local SQLite file; `agentsight report` and a local web UI show tokens,
a timeline, the process tree and metrics. eBPF capture needs root or
`CAP_BPF`; without it, `top`, `report` and `vis` fall back to native Claude,
Codex and Gemini session files. It can also export LLM calls as OpenTelemetry
GenAI spans.

## Reference scenarios

How quickly a person can see each [reference scenario](README.md#reference-scenarios).
✅ visible in standard views · ⚠️ needs a custom query or manual correlation ·
❌ data is missing.

| Scenario | Rating | Basis | How it shows, or what is missing |
| --- | --- | --- | --- |
| S1 Commands rerun without a change | ? | tried / docs | |
| S2 Lead model calls while waiting | ? | tried / docs | |
| S3 Polling without new information | ? | tried / docs | |
| S4 Long wait or blocker | ? | tried / docs | |
| S5 Spend without a successful outcome | ? | tried / docs | |

## Coverage

| Criterion | Rating | Basis | Notes |
| --- | --- | --- | --- |
| Agents | ? | tried / docs | |
| Env | ? | tried / docs | |
| Tokens | ? | tried / docs | |
| Attrib | ? | tried / docs | |
| Cost | ? | tried / docs | |
| Compute | ? | tried / docs | |
| Time | ? | tried / docs | |
| Outcome | ? | tried / docs | |
| Setup | ? | tried / docs | |
| Data | ? | tried / docs | |

## Minimal setup

The smallest configuration that gives useful results. List anything that
would need custom code.

## Data and privacy

What is collected, where it is stored and what leaves the machine.

## Trial notes

For finalists: which real runs we looked at, in which environment and with
which agents, and which weak spots were or were not easy to see.

## Verdict

Adopt, combine with another tool, or reject, and why.
