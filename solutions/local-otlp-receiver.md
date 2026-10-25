# Local official OTLP receiver with SQLite

- **Link:** [Subyard collection contracts](https://github.com/subyard/subyard/blob/master/docs/reference/agent-telemetry.md)
- **Version checked:** OTLP receiver 0.163.0, pdata 1.69.0, modernc SQLite 1.61.0; measured product SHA-256 `f6ad4f0d2561ebfa2ebbea24b8fb74f4eead4f0f2175a3c1ddabda4c8efb747c`
- **Checked on:** 2026-10-24
- **License:** Subyard glue is MIT; dependencies retain their own licenses.

## Summary

An independently runnable service embeds the official OpenTelemetry receiver and
commits sanitized logs, metrics and traces to SQLite. Subyard optionally manages
its lifecycle and adds explicit agent execution, process and broker-resource
observations. Selected as the collection layer; no analytics UI is selected.

## How it works

Native HTTP/protobuf OTLP and versioned resource records enter a bounded,
serialized SQLite WAL writer. Success means a durable commit. Managed cgroups
account for descendant work, while owner-side observers provide generation-safe
VM/emulator evidence through restricted read-only interfaces. Relationships are
explicit and temporal; a shared backend does not get charged to each session.
Resource registration uses bounded private durable intents and retained-journal
replay, so a busy observer need not lose a completed short allocation. Transport
credentials remain outside telemetry records and export.

## Reference scenarios

This is a data layer. D7's ordinary-work evaluation of a user-facing analytics
product remains pending; collection acceptance is not a substitute.

| Scenario | Rating | Basis | How it shows, or what is missing |
| --- | --- | --- | --- |
| S1 Commands rerun without a change | ? | not evaluated | Compute/time records are available; command bodies are excluded by default. |
| S2 Lead model calls while waiting | ? | not evaluated | Native event times and explicit run relations need later analytics. |
| S3 Polling without new information | ? | not evaluated | No automatic inefficiency interpretation. |
| S4 Long wait or blocker | ? | not evaluated | Lifecycle/time evidence needs a later timeline. |
| S5 Spend without a successful outcome | ? | not evaluated | Quality, billing and outcome evaluation are outside collection. |

## Coverage

| Criterion | Rating | Basis | Notes |
| --- | --- | --- | --- |
| Agents | ⚠️ | native protocol/process acceptance | Actual Codex 0.164.0 and Claude 2.1.287 with local fixture providers; native tools bound distinct runs and sessions to both VM and Android allocations; owner failure/recovery and export/replay checks passed. |
| Env | ⚠️ | native standalone smoke | Receiver is standalone; complete compute coverage depends on safe Linux delegation. |
| Tokens | ⚠️ | native protocol contracts | Raw metric/event semantics retained; no universal token normalization. |
| Attrib | ⚠️ | native protocol contracts | Explicit run/session/resource identities; unsupported paths stay unknown/shared. |
| Cost | ❌ | scope | No monetary billing. |
| Compute | ⚠️ | local scope physical acceptance | Pre-exec counters, short-lived/background descendants, nested runs and VM owner observations passed; Android profile lifecycle, owner failure/recovery and generation reuse passed. |
| Time | ⚠️ | protocol contracts | Source/receive times and interval/counter domains retained. |
| Outcome | ❌ | scope | No agent-quality or outcome scoring. |
| Setup | ⚠️ | implementation | Optional profile or standalone binary; custom SQLite and attribution glue. |
| Data | ✅ | native commit/replay tests | Local SQLite, capture policy before durable storage, open export/replay. |

## Minimal setup

Run the standalone binary with a private data directory and bearer credential, or
enable Subyard's optional `telemetry` profile. Full process/resource attribution
requires explicit managed launches and updated owner observation capabilities.
OpenLIT, ClickHouse, Redis and a SQL server are unnecessary.

## Data and privacy

No telemetry must leave the yard for collection. The default policy excludes
prompt/response/tool bodies, credentials, command lines and environment capture
before raw/spool/database writes. Raw means supported source structure within that
policy. Stable export identities enable replay; equal payloads are not universal
duplicate identities. Replay retains the original capture-policy fingerprint separately from
the trusted local policy applied on import; SQLite v1 stores migrate transactionally
to v2. Native OTLP retries can remain ambiguous, so automatic
exactly-once token totals are not claimed.

## Trial notes

Three alternating trials per binary used one disposable Debian 13 amd64 VM,
4 vCPU/4 GiB, Linux 6.12.113, SQLite 3.54.1. Each trial used a fresh DB,
15-second warmup, 60-second idle and 90-second load at 30 mixed requests/s,
32 records/request. The driver was outside collector accounting. Median idle CPU
was 0.05% of one core; load CPU 10.15%; mean sampled load RSS 35.63 MiB;
block writes 1.175 MiB/s; SQLite/WAL/SHM growth 0.127 MiB/s. Every offered request
matched committed rows, with no rejects or driver queue drops.

CPU under load ranged 9.50–13.10%; the host was shared. Later correctness repairs
changed the product binary; this comparison binds only to the SHA above and finite
synthetic input. Final installed service/observer consumption is a separate measure.
These are collection benchmarks, not ordinary-work D7 analytics trials.

A separate installed-stack trial used a 4 GiB disposable Linux stage and product
SHA-256 `cf16ded93c82fcd65b4d6ff87f539c3bcd34132dd08989dac3f4c4319300ce73`,
with launcher SHA-256 `461cae184f9e270669f0dc1bfbf2cfcd39a0a4d829d53f967466c357660a53c1`.
At five-second agent sampling, 60 seconds idle and 90.46 seconds of 30 mixed
requests/s plus managed short descendants, collector/manager CPU was
0.075%/0.053% idle and 5.993%/0.183% loaded, measured as fractions of one core.
Their sampled maximum load RSS was 36.38/25.38 MiB. Collector block writes
averaged 1.178 MiB/s, manager writes 2.70 KiB/s; DB/WAL/SHM apparent growth was
0.127 MiB/s. All 2700 load requests were accepted and 900 load rows per OTLP signal were
retained, alongside a separate pre-load metric-unit probe. This one shared-host trial excludes workload sibling groups and does
not establish remote-owner polling cost at arbitrary fleet size. The local lane
also passed crash/storage recovery, short-lived/background descendants and actual
native Codex/Claude session binding. The separate VM lane passed native tool/session/run attribution, held-resource
measurements, storage failure, owner downtime/recovery, natural expiry with a live
draining worker, generation fencing and clean reuse. Separate Android checks passed
native tool/session/run attribution and supported profile enable/disable inside
Incus, including retained history, background completion and unchanged pool identity.
The Android lane also passed owner downtime/recovery, a natural 1200-second
expiry after requester loss, generation reuse and final counters. Its 3220-record
export retained all three OTLP types and resource records; two replays preserved
record counts, kinds and a sample SQL projection. These are segmented physical
results; final code review and any resulting focused repairs remain separate.

## Verdict

Adopt for collection and combine later with a separately selected analytics layer.
Compared with the [minimal Collector](local-otel-collector.md), it keeps the same
official protocol receiver and sink with less service/config/factory assembly and
lower observed RSS. The small comparison does not prove a universal CPU speedup.
