# Minimal OpenTelemetry Collector with the same SQLite sink

- **Link:** [Subyard comparison implementation](https://github.com/subyard/subyard/tree/master/dev/telemetry-compare)
- **Version checked:** Collector service/OTLP receiver 0.163.0, pdata 1.69.0; measured binary SHA-256 `1483d3cf16c5ed45d97aa137d5f7e238fa89a5f8802ebe750493b1d55bdf34a4`
- **Checked on:** 2026-10-24
- **License:** Subyard glue is MIT; dependencies retain their own licenses.

## Summary

A minimal actual Collector service assembles the official OTLP receiver and the
same custom SQLite sink and content policy as the embedded service. It is a
collection-packaging comparison, not an analytics platform. Keep as a reproducible
comparison; the embedded receiver was selected for the installed service.

## How it works

Collector factories and configuration assemble logs, metrics and traces pipelines
around the shared receiver/consumer. Durability, schema, capture policy, identities
and resource attribution remain the same custom local components; selecting the
Collector wrapper does not eliminate that work.

## Reference scenarios

No user-facing analytics trial has occurred. It has the same collection evidence
and limitations as the [embedded receiver](local-otlp-receiver.md), with different
runtime assembly. D7's ordinary-work evaluation remains pending.

| Scenario | Rating | Basis | How it shows, or what is missing |
| --- | --- | --- | --- |
| S1 Commands rerun without a change | ? | not evaluated | Raw compute/time needs analytics; command bodies excluded by default. |
| S2 Lead model calls while waiting | ? | not evaluated | No dedicated view. |
| S3 Polling without new information | ? | not evaluated | No automatic interpretation. |
| S4 Long wait or blocker | ? | not evaluated | Time/lifecycle source records need a later timeline. |
| S5 Spend without a successful outcome | ? | not evaluated | No billing, quality or outcome layer. |

## Coverage

| Criterion | Rating | Basis | Notes |
| --- | --- | --- | --- |
| Agents | ? | shared implementation; physical acceptance pending | Same native adapters, not an additional Collector integration. |
| Env | ⚠️ | native Collector commit smoke | Standalone collector service; Linux compute delegation is separate. |
| Tokens | ⚠️ | shared protocol contracts | Native semantics retained without universal normalization. |
| Attrib | ⚠️ | shared protocol contracts | Same explicit temporal graph and unknown/shared states. |
| Cost | ❌ | scope | No billing layer. |
| Compute | ? | shared implementation; physical acceptance pending | Requires the same process and resource producers. |
| Time | ⚠️ | shared protocol contracts | Source/receive times and domains retained. |
| Outcome | ❌ | scope | No quality/outcome evaluation. |
| Setup | ⚠️ | implementation | Additional Collector service/factory/config assembly around the sink. |
| Data | ✅ | native commit/replay tests | Same policy, SQLite and export contracts. |

## Minimal setup

Build `dev/telemetry-compare/collector` and run its `serve` command with private
data and credential files. The benchmark uses the same arguments and load driver
for both actual binaries. This wrapper is not shipped as the installed collector.

## Data and privacy

Identical to the embedded service: policy before persistence, local durable
records and stable export/replay identities. No additional analytics server or
public OTLP listener is required by this comparison.

## Trial notes

The same three-trial disposable experiment is documented in the embedded
receiver comparison. Median idle CPU was 0.10% of one core; load CPU 19.40%;
mean sampled load RSS 38.73 MiB; process block writes 1.175 MiB/s;
SQLite/WAL/SHM growth 0.126 MiB/s. All offered requests committed; one 90-second
trial offered 2699 rather than 2700 requests, without client drops or rejects.
Load CPU ranged 10.11–27.64%, so a general performance claim is unjustified.

The numbers bind to the binary SHA above. Subsequent correctness repairs were
outside the measured finite payload; final installed collection consumption is
measured separately. No D7 ordinary-work analytics trial is claimed.

## Verdict

Use the embedded official receiver for this single local sink. Retain this
minimal Collector harness when evaluating future packaging changes; revisit if
real requirements call for a broader Collector pipeline that offsets the extra
assembly. No analytics product is selected by this result.
