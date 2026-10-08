# Solution comparison

This folder compares existing tools that could provide usage visibility for
agent workflows, before anything is implemented. See
[decisions D1](../docs/decisions.md#d1-evaluate-existing-tools-before-building-anything):
we prefer configuring existing tools over building new ones.

Each candidate has its own file, based on [`_template.md`](_template.md). The
tables below are the summary; the candidate file holds the evidence.

## Candidates

Confirmed for comparison
([D9](../docs/decisions.md#d9-shortlist-ai-observer-openlit-and-langfuse)):

| Candidate | What it is | File |
| --- | --- | --- |
| [AI Observer](https://github.com/tobilg/ai-observer) | Self-hosted telemetry backend for AI coding agents; Subyard integrates it | [ai-observer.md](ai-observer.md) |
| [OpenLIT](https://github.com/openlit/openlit) | Open-source, OpenTelemetry-based observability for LLM applications | [openlit.md](openlit.md) |
| [Langfuse](https://github.com/langfuse/langfuse) | Open-source LLM engineering platform with tracing and cost tracking | [langfuse.md](langfuse.md) |

Possible additions, if the confirmed candidates leave gaps:

- Local log analyzers such as `ccusage`.
- An LLM gateway or proxy in front of the model API.
- Container and process metrics for compute (scenario S1), combined with one
  of the candidates above.

To add a candidate, copy the template, add a row to every table below and link
its file.

## Reference scenarios

The main question is how quickly a person can see where a pipeline wastes
resources. Waste can appear in tokens, compute or time, and a step can be
cheap in one and expensive in another. Each candidate, alone or combined with
others, is rated against these scenarios. Finalists are then integrated and
checked on real, everyday runs, not on synthetic tasks
([D7](../docs/decisions.md#d7-people-evaluate-candidates-finalists-are-checked-on-real-runs)).

| ID | Scenario | Where the waste shows |
| --- | --- | --- |
| S1 | Tests or other commands rerun without a code or environment change | Compute, time; few tokens |
| S2 | A lead agent keeps calling its model while waiting for another agent | Tokens |
| S3 | Frequent process polling or status messages without new information | Tokens, time |
| S4 | A long wait or blocker on the path to delivery | Time |
| S5 | High resource use without a successful outcome | All, plus outcome |

For each scenario, record whether the problem is visible in the tool's
standard views (✅), needs a custom query or manual correlation (⚠️), or
cannot be seen because the data is missing (❌).

| Candidate | S1 | S2 | S3 | S4 | S5 |
| --- | --- | --- | --- | --- | --- |
| [AI Observer](ai-observer.md) | ? | ? | ? | ? | ? |
| [OpenLIT](openlit.md) | ? | ? | ? | ? | ? |
| [Langfuse](langfuse.md) | ? | ? | ? | ? | ? |

## Criteria

Criteria follow the [requirements](../docs/decisions.md#requirements).

| Key | Criterion | Question |
| --- | --- | --- |
| Agents | Agent coverage | Does it work with Codex, Claude Code and OpenCode? |
| Env | Environment | Does it run in a plain devcontainer or local terminal, without Subyard? |
| Tokens | Token accounting | Input, cached input, output and reasoning per model, without double counting? |
| Attrib | Attribution | Can usage be traced to an agent, subagent and step or tool call? |
| Cost | Cost estimate | Does it estimate cost and keep estimates separate from billing? |
| Compute | Compute | CPU, memory and processes, including test runs? |
| Time | Time to delivery | Can active work, waiting and blockers be seen on a timeline? |
| Outcome | Task outcome | Can usage be linked to whether the task succeeded? |
| Setup | Setup effort | What is needed beyond installation? How much custom code? |
| Data | Data location | Where does data go? Can it stay local or self-hosted? |

Ratings: ✅ covered · ⚠️ partial · ❌ not covered · ? not checked yet.
In candidate files, mark each rating as *tried* (seen on real runs) or *docs*
(based on documentation only).

## Coverage

No single tool is expected to cover every criterion. A solution may combine
tools, for example one for model usage and one for compute.

| Candidate | Agents | Env | Tokens | Attrib | Cost | Compute | Time | Outcome | Setup | Data | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [AI Observer](ai-observer.md) | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Not started |
| [OpenLIT](openlit.md) | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Not started |
| [Langfuse](langfuse.md) | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Not started |

## Conclusion

Not reached yet. When it is, record the choice as a decision in
[`docs/decisions.md`](../docs/decisions.md) and summarize it here.
