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
  repository, a terminal session or a standard devcontainer. Codex and
  Claude Code support is mandatory; OpenCode support is optional (D13).
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

- **Cost:** a basic estimate from token counts and published model prices,
  kept separate from actual billing. No billing or provider API integration.
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
The chosen solution must work without it. Subyard is public
([github.com/subyard/subyard](https://github.com/subyard/subyard)) and can be
cited.

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

### D5. The intro data is a fixed example

2026-10-08 · Accepted

The October 5–6 figures are an example provided by one of the users, from
Codex logs of a separate Subyard instance with many agents. They describe the
kind of problem the solution must make easy to see. They are not re-verified
or regenerated, and hardcoded figures in the presentation are intended.
`scripts/collect_evidence.py` documents how they were produced; it is not the
basis for the general solution.

### D6. Judge candidates by how fast they reveal inefficiency

2026-10-08 · Accepted

Token totals alone miss waste that shows up in compute or time, such as tests
rerun in a loop. Candidates are evaluated against reference scenarios in
[`solutions/`](../solutions/README.md#reference-scenarios): can a person see
each problem quickly, and in which resource it appears? Compute and time are
must-have requirements alongside tokens.

### D7. People evaluate candidates; finalists are checked on real runs

2026-10-08 · Accepted

People compare candidates in `solutions/`. We then implement the main
candidate, or two finalists, and integrate it into ordinary work. The check is
whether weak spots in real, everyday runs are quick and convenient to see. We
do not create synthetic tasks to provoke the reference scenarios.

### D8. Lead with total tokens

2026-10-08 · Accepted

Total tokens (input plus output) is the figure the industry uses, so it stays
the headline number. Uncached input and output are shown next to it in smaller
type, because cached input usually makes up most of the total.

### D9. Shortlist: AI Observer, OpenLIT and Langfuse

2026-10-08 · Accepted

The comparison starts with AI Observer, OpenLIT and Langfuse. Other tools can
be added if these leave gaps, for example in compute visibility.

### D10. Add AgentSight to the shortlist

2026-10-08 · Accepted

AgentSight is added to the comparison alongside the D9 candidates. It observes
agents from the system side with eBPF, so it may cover compute and process
activity, which the other candidates are least likely to show.

### D11. Present candidates from their real interfaces

2026-10-09 · Accepted

`presentation2-solutions/` shows the D9 and D10 candidates as they look: the
projects' own screenshots, their documentation and a running AI Observer. It
maps the reference scenarios and requirements onto each tool and lists other
options. Its ratings are a first reading from documentation, not trial
results; `solutions/` records the ratings once candidates are tried. Screenshots
of local instances are not published, because they show session data (D4).

### D12. Add MLflow to the shortlist

2026-10-12 · Accepted

MLflow joins the D9 and D10 candidates at the user's request. Evaluate its
GenAI tracing, coding-agent integrations, token and cost views, and optional
system metrics against the same requirements and reference scenarios.

Add the project's official screenshots and an explanation of its interface
and fit to `presentation2-solutions/`, with source links. Record the initial
MLflow ratings as documentation-based in `solutions/`; they do not replace
the real-run validation required by D7. Rebuild the presentation PDF and check
that every slide fits on one page.

### D13. Require Codex and Claude Code support

2026-10-12 · Accepted

The user clarified that the selected solution must support both Codex and
Claude Code. OpenCode remains in the comparison, but its support is optional
and must not block selection. This narrows the mandatory agent coverage; it
does not select a candidate or replace the real-run validation required by D7.

### D14. Prepare presentation 3 incrementally from supplied material

2026-10-14 · Accepted

Create `presentation3/` using the existing HTML presentation conventions,
with a printable PDF and navigation ready for later slides. Prepare only the
first slide now; the user will supply subsequent slides later.

Slide 1 shows token usage for October 6–13 from the user-provided screenshot:
13,396,361,355 total tokens across eight daily aggregates, or about 1.67 billion
per day. Count the identical All and Codex rows only once. Treat the last token
column as the total because it equals the sum of the three nonzero preceding
token columns; the screenshot omits the headers, so do not assign breakdown
labels. Preserve the transcribed totals and source limitations in
`presentation3/data.json` and the deck's source notes.

The user's context is roughly 5–7 sessions running nearly 24/7. Present it as
an estimate, without implying measured concurrency or exact operating hours.
Keep total tokens as the headline (D8); do not infer cost or inefficiency from
the totals alone. Rebuild the PDF and verify one page per slide after updates.

### D15. Follow the supplied AI Observer slide order

2026-10-14 · Accepted

The next three slides in `presentation3/` cover AI Observer. The user confirmed
the order: slide 2 is the annotated All Tools dashboard, slide 3 is the supplied
local Default Dashboard, and slide 4 is the earlier Metrics selector screenshot.

Reuse the matching official dashboard image from presentation 2 for slide 2,
including its five callouts. Distinguish its example data from the local view.
Slides 3 and 4 summarize only visible aggregate values and metric labels from
the supplied captures. The original image files for these two views are not
available in the workspace; use labeled transcriptions until they are available.
Do not reproduce internal host addresses or session-level content (D4, D11).

Scope the Default Dashboard observations to the displayed Last 1 hour view:
829,535 metric data points, 210,553 logs, zero traces/spans and a displayed
0.00% error rate, with Codex CLI listed as an active service. Zero spans do not
establish a meaningful error rate. Scope the metric selector to its visible
Claude Code and Gemini CLI groups; the cropped menu does not establish complete
agent support, available data or successful CPU collection. These observations
do not change candidate ratings in `solutions/` or replace D7's evaluation.

### D16. Preserve supplied original images beside presentation 3

2026-10-14 · Accepted · Supersedes D15's use of text summaries as slide content

The user requires the original supplied images to be saved in
`presentation3/img/`. Preserve all four originals: token usage, the annotated
All Tools dashboard, the local Default Dashboard and the Metrics selector.
The existing official dashboard asset is not an archive of the user's annotated
image. Generated images and text summaries are not replacements for originals.

On slide 1, replace the right-hand daily bar chart with the user's original
token-usage screenshot. Keep the headline and session context on the left.
Keep the confirmed order of the four slides. The user explicitly authorizes
using the supplied screenshots for this presentation; D11 does not prevent
their requested inclusion.

Implementation is pending access to the original image files. The attachments
are visible in the conversation but have not been exposed as files through
the available tools. Checks of the repository and available attachment
locations found no originals. Do not claim they have been saved or insert
broken image references. Once the files are available, embed them, rebuild
the PDF and verify every page.

### D17. Use the supplied token screenshot on slide 1

2026-10-14 · Accepted · Updates D16's pending status for the token image

The user supplied the token-usage image as an accessible file. Preserve it
unchanged in `presentation3/img/token-usage-original.png` and replace slide 1's
right-hand chart with it. Keep the headline and session context on the left.
The screenshot shows October 5–13; the existing headline, average and JSON
aggregates remain scoped to October 6–13, excluding October 5. Explain that
scope in the caption and source notes. The other three originals remain pending.


### D18. Make the supplied screenshot the main content of slide 3

2026-10-14 · Accepted · Updates D15's snapshot and D16's pending image status

Preserve the newly supplied Default Dashboard screenshot unchanged as
`presentation3/img/ai-observer-default-dashboard-original.png`. Replace slide
3's text summary with the full screenshot as its main content; supporting
headings and captions may surround it. The new Last 1 hour capture shows
830,397 metric data points and 210,782 log records, superseding the earlier
snapshot's counts. Codex CLI remains listed, with zero traces/spans and a
displayed 0.00% error rate. The All Tools and Metrics originals remain pending.


### D19. Enlarge slide 1 and use the original Metrics screenshot on slide 4

2026-10-14 · Accepted · Updates D15's Metrics snapshot and D16's image status

Reduce the empty margins on slide 1 and enlarge its screenshot, keeping the
headline and supporting figures compact on the left. Preserve the full image.

Save the supplied Metrics screenshot unchanged as
`presentation3/img/ai-observer-metrics-original.png` and make it the main content
of slide 4. This capture shows All Services, Last 15 minutes, no selected metric
and 697 real-time updates, superseding the earlier 146 counter. The visible
Gemini CLI menu now also includes Lines Changed and Memory Usage. Menu entries
do not establish successful resource collection. Only the original annotated
All Tools image for slide 2 remains pending.


### D20. Open the MLflow section with the supplied trace screenshot

2026-10-14 · Accepted

Add slide 5 after the AI Observer slides to start the MLflow section. Preserve
`.orca/drops/mlflow_trace_view_real.jpg` unchanged as
`presentation3/img/mlflow-trace-original.jpg` and make the full screenshot the
main content, with a short heading and caption. The user's request authorizes
inclusion of this supplied trace view, including its browser chrome and visible
trace details, extending D16's screenshot inclusion decision to MLflow.

Describe only what is visible: MLflow 3.17.0, a trace marked Success, a hierarchy
of spans and timings, and attributes of the selected LLM call. This does not
change candidate ratings or establish task outcome beyond the displayed trace
status. Rebuild the PDF with five pages, one per slide.


### D21. Use the title area to enlarge screenshots on slides 4 and 5

2026-10-14 · Accepted

Move the screenshots on slides 4 and 5 slightly right and place compact titles
beside them so the images can start higher and appear larger. Keep the full
originals visible without cropping. Use the same layout in the PDF and stack
titles above images on narrow screens. Other slides retain their layouts.


### D22. Insert a Subyard introduction as slide 2

2026-10-14 · Accepted · Updates the slide numbering in D15–D21

Add a Subyard slide immediately after token usage, using the architecture image
from the project's README and a visible, clickable repository link:
https://github.com/subyard/subyard. Save the image unchanged as
`presentation3/img/subyard-agent-workspace.webp`; source asset
`docs/assets/agent-workspace.webp`, commit `dbf15e3ee96a249f153324167f7c06afd498a401`.

Describe its container or VM yards for coding agents, shared staging, SSH host
management and Git settings, based on the README. Keep Subyard's role as a
reference environment rather than a dependency (D2). Existing slides keep their
relative order: All Tools is now 3, Default Dashboard 4, Metrics 5 and MLflow 6.
Preserve the enlarged image layouts for Metrics and MLflow. Rebuild and verify
six PDF pages, one per slide.


### D23. Make the Subyard link prominent and add context

2026-10-14 · Accepted

Reduce slide 2's diagram slightly to make room for a context column covering
isolated containers or VMs and resource limits, shared staging, and SSH/Git
host management. Move the repository link out of the small footer into a large,
high-contrast link beside the explanation. Keep the README diagram intact and
the link clickable in both the presentation and its PDF.


### D24. Compare required harness data sources on slide 3

2026-10-14 · Accepted · Updates D22's slide numbering

Insert a designed comparison of Codex CLI and Claude Code at position 3, after
Subyard. They remain mandatory and OpenCode optional (D13). Separate default
local persistence from telemetry sent to our collector and separately enabled
native trace spans. Use OpenTelemetry (OTel) and OTLP terminology; label Claude
Code's enhanced tracing beta. Record official source links and export controls
in the deck's Sources notes, checked October 14, 2026.

Local session formats are version-dependent. Provider operational analytics
are separate from configured collector exports, and redacting exported prompt
content does not remove local transcripts. The remaining need for process-level
CPU/RAM and cross-harness task/agent/step correlation is a project assessment,
not a claim that native tool timing or spans are absent. No private sessions
were inspected, exporters enabled, or candidate ratings changed.

The deck now has seven slides: usage, Subyard, harness data, All Tools, Default
Dashboard, Metrics and MLflow. Rebuild the PDF and verify one page per slide.
