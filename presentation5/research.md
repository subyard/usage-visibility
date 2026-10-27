# Research and evidence: running coding agents, 24/7

Prepared October 27, 2026. This file keeps the source evidence with the talk;
project-wide requirements belong in `docs/decisions.md`.

## Recommended implementation

Use a self-contained static HTML deck with local assets, separate HTML speaker
notes, and a Chromium-printed PDF. This matches the repository's existing decks,
retains clickable source links, supports direct slide links, and can be served
unchanged by GitHub Pages. It also allows the speaker's requested format—key
idea, slide description, spoken explanation—without putting the entire script
on the projected slide.

The existing presentation 4 navigation and print model already cover the task.
Reuse that code and its 1600 × 900 canvas. When printing, resolve local links
against the chosen public URL; restore local links for offline browsing. This
keeps shared PDFs from pointing to the author's local filesystem.
No presentation framework, remote
fonts, analytics, build service or new runtime dependency is needed. Google
Slides or PowerPoint would be useful if native collaborative editing became a
requirement; neither is needed for this repository's HTML/PDF workflow.

The selected public address is
<https://subyard.github.io/usage-visibility/presentation5/>. The final slide's
link and QR encode that address. Publication is separate from creating the
files; no commit, push or hosting configuration change is part of this work.

## Narrative and speaking budget

Lead with the presenter's scale, then give each operational mechanism a reason
to exist. The progression is personal experience → access boundaries → usable
tools → capacity → broker lifecycle → discoverable instructions → context
maintenance → evidence and improvement → implementation example → responsibility.

The broker topic deserves two slides within the 20–25 minute budget. A normal
allocation and a failure cleanup path have different triggers and outcomes.
Combining both with three benefits would obscure the key distinction: a lease
deadline is not proof that a resource has been cleaned. The final deck therefore
has 16 slides, including a separate explanation of skills as instructions on demand.

## Source map

| Final slide | Source or status | Use in this talk |
| --- | --- | --- |
| 1 | Presenter's October 27 clarification; presentation 3 slide 1 and `data.json` | Current scale, human checkpoints, publication-safe historical token table |
| 2 | Original Subyard slide 1 composition and screenshot; presenter-supplied post-training thesis | Isolation without assuming hostile intent |
| 3 | Original Subyard slide 2; Docker and Microsoft documentation | Shared kernel / guest kernel and operating recommendation |
| 4 | Presenter's jq and firmware examples; Dev Container Features | New diagram showing the full verification path |
| 5 | Presenter's operating observations | RAM and Rust storage examples, explicitly not benchmarks |
| 6 | Original Subyard slide 6; current VM/Android broker documentation | Defined environments and allocation only while needed |
| 7 | Original Subyard slide 7; current lease contract | Independent cleanup, fencing, verification and quarantine |
| 8 | Original Subyard slide 10 right panel; current Android skill | Discover → read → use, with a clickable broker link |
| 9 | Presenter's conditional-instructions framing; official OpenAI Skills documentation | Explicit invocation or description-based selection, then load instructions |
| 10 | Presenter's experience; Anthropic context-engineering research | Humans prune accumulated text; keep instructions minimal, open-ended and directional |
| 11 | Existing Usage Visibility work; OTel GenAI agent conventions | Collect team evidence and connect resource use to outcomes |
| 12 | Presentation 3 slide 10, anonymized native HTML summary | Ask an agent to review its workflow; validate its report |
| 13 | Presentation 3 slide 2, original architecture diagram | Subyard as the presenter's reference implementation |
| 14 | Original Subyard slide 5; current configuration/profile docs | Optional capabilities, with an illustrative matrix |
| 15–16 | Presenter's closing brief and publication choice | Responsibility, questions and a shareable address |

The requested published Subyard deck could not be fetched by the web reader.
Its exact HTML and notes were read through the GitHub connector from
[`docs/presentations/subyard/`](https://github.com/subyard/subyard/tree/c4348a10768abe619a8dc9fd073cf87353116085/docs/presentations/subyard).
The local `presentation4/` contains an earlier import of the same deck.

## Primary-source findings that affect the wording

### Boundaries depend on effective permissions

The presenter frames agents as trained to complete the immediate task rather
than weigh long-term consequences. This is the talk's operating principle, not
a universal claim about all post-training objectives or proof of the cause of
the reported deletion.

[Docker Engine security](https://docs.docker.com/engine/security/) explains
namespaces, control groups and the privileged daemon. Broad host mounts,
privileges or daemon access can undermine the intended container boundary.
[Docker's container overview](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
supports the shared-kernel / separate-guest-kernel comparison.
[Microsoft's container isolation documentation](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
also makes clear that Windows supports more than one isolation mode.

The Linux-devcontainer / Windows-VM guidance is the presenter's practical
starting point for Linux development, not a platform limitation. A VM still
exposes whatever mounts, networking, devices and credentials are configured.
[Anthropic's sandboxing research](https://www.anthropic.com/research/claude-code-sandboxing)
describes actual OS-enforced filesystem and network controls. Accordingly,
the talk does not claim that harness restrictions are always prompts or that
they cannot enforce isolation. The presenter's experience with his own setup
is kept distinct from that broader claim.

### Repeatable setup and isolation solve different problems

Official starting points linked directly under Devcontainer on slide 3:

- [Anthropic's Claude Code devcontainer configuration](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json)
  builds the supplied [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile).
  It is a full example configuration, not a prebuilt Anthropic image.
- [OpenAI's codex-universal](https://github.com/openai/codex-universal)
  publishes a reference base image and Dockerfile. The
  [official OpenAI environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environment)
  points to it for local development. It is labeled **base image**, not a
  ready-made devcontainer. The repository describes it as similar to the
  hosted base environment, not identical. The checked `.devcontainer` paths in
  `openai/codex` and `openai/codex-universal` did not exist.

Checked October 27, 2026. These links identify reusable setup, not a claim that
either example has been run or audited in this workspace. The
[official OpenAI security documentation](https://learn.chatgpt.com/docs/agent-approvals-security)
also describes using Codex in Dev Containers; no provider-specific sandbox
flags are added to this slide.

The [Dev Container Features specification](https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainer-features.md)
supports reusable tool installation and configuration. Some capabilities can
require extra privileges or have base-image dependencies. Having the SDK and
test tools present improves usability; it does not by itself establish a
security boundary. The board example also requires a real flashing and reset
path appropriate to that hardware.

### Configured limits are not physical capacity

[Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)
documents that containers have no resource constraints by default and explains
memory limits, pressure and CPU controls. Limits, reserved capacity, current
use and resource holding time must remain distinct. The presentation therefore
uses the presenter's observations without inventing a balanced RAM allocation
chart or extrapolating universal concurrency.

### Expiry and cleanup are separate

[Kubernetes Leases](https://kubernetes.io/docs/concepts/architecture/leases/)
provide coordination and heartbeat records.
[TTL cleanup for finished Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/)
is controller work and can be delayed by lifecycle requirements. These are
supporting examples, not a proposal to add Kubernetes.

The directly relevant implementation is Subyard's
[resource lease contract](https://github.com/subyard/subyard/blob/c4348a10768abe619a8dc9fd073cf87353116085/docs/reference/resource-leases.md),
[test VM pool](https://github.com/subyard/subyard/blob/c4348a10768abe619a8dc9fd073cf87353116085/docs/test-vms.md),
and [Android broker](https://github.com/subyard/subyard/blob/c4348a10768abe619a8dc9fd073cf87353116085/docs/android.md).
Revoke access, stop the runtime, clean disposable state, verify the result and
quarantine unsuccessful cleanup. Do not imply instant physical destruction at
the deadline. Reusable base images and caches have separate lifetimes.

### The Android skill is a current, concrete example

The original source slide 10 showed `subyard-github`, while its left panel
described cross-host borrowing as planning. The requested Android example is
independently supported by the current
[`subyard-android` skill](https://github.com/subyard/subyard/blob/c4348a10768abe619a8dc9fd073cf87353116085/config/profiles/android/skills/subyard-android/SKILL.md)
and [skill delivery contract](https://github.com/subyard/subyard/blob/c4348a10768abe619a8dc9fd073cf87353116085/config/skills/README.md).

The skill directs agents to inspect catalog/status, then use
`android-broker run --device phone --api 35 -- ./run-device-tests.sh`.
The wrapper renews and releases the lease. Skill presence records successful
provisioning; it does not prove live readiness. The talk therefore links the
broker and skill separately, and does not claim a shipped cross-host scheduler.

Organization, the user inside the container, and repository are scopes of
guidance. The slide assigns shared policies to the organization and AGENTS.md
plus skills to the user and repository. It does not show filesystem paths or
assert that all harnesses discover the same files or implement the same
instruction precedence rules. The user-level example is supported by the
[official AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

### Skills are instructions loaded on demand

[Official OpenAI documentation: Skills](https://developers.openai.com/plugins/concepts/skills)
describes metadata-first discovery: the name and description are visible before
the full instructions. A direct user invocation or a matching task can select
the skill and cause its instructions to be loaded. The new slide uses the
presenter's conditional-instructions framing for this behavior. Skills can also package
references, scripts and assets; invocation syntax and discovery depend on the
harness. The slide is a conceptual explanation, not a requirement for a new
runtime feature in this repository.

### Minimal context means sufficient context

[Anthropic's effective context engineering research](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)
supports high-signal context, clear tool contracts and loading details when
needed. It explicitly distinguishes sufficient context from simply short
context. The talk treats verbosity and retention of existing text under uncertain
importance as the presenter's observation and causal framing. The source does
not establish that explanation for every model. Human judgment determines what
still matters and what can be removed; necessary constraints remain useful.
The presenter favors minimal, open-ended instructions that set a direction and
leave the model to infer ordinary steps. This is operating guidance, not a
measured claim that models need no task-specific detail.

### Instrumentation still determines coverage

[OpenTelemetry's GenAI agent span conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
provide vocabulary for agent and tool operations. The conventions are in
Development status. They do not establish which events a particular harness
actually exports, or attribute child-process CPU and RAM automatically.

The talk follows this repository's D14 collection model: explicit correlation,
separate actual consumption and held capacity, visible unknown/shared work,
and no default collection of prompt, response or tool bodies. Choosing the
perfect analytics product is not a prerequisite for collecting useful evidence.

## Numeric and visual evidence

- **Current scale:** 1–2B tokens/day (98% cached input), about four nonstop
  sessions, roughly half running longer than a day, supplied by the presenter.
  The cache share is the presenter's clarification, not a calculation from the
  historical screenshot, whose column labels are outside the image.
  The presenter describes this as
  effective use; no independent efficiency measurement is claimed.
- **Human checkpoints:** at least task formulation and personally checked
  acceptance for every task. This does not imply continuous supervision or
  forbid additional conversations during execution.
- **Historical token table:** October 6–13, 2026; 13,396,361,355 tokens; average
  1,674,545,169.375/day. Count duplicate All/Codex rows once; exclude October 5.
  Its historical 5–7-session context differs from the current estimate.
  The publication raster is recreated with a solid black background, retaining
  daily totals and model names while omitting the financial column.
- **Capacity examples:** 32 GB for about three smaller-project sessions and
  over 100 GB of Rust build caches/artifacts per agent are personal observations.
  No host benchmark, disk inventory or raw session evidence was accessed.
- **Agent review:** an anonymized native HTML prompt and four generic
  recommendations replace the original screenshots: reduce coordination
  chatter, rerun selectively, check prerequisites early and release resources
  when finished. Exact session counts and internal incident details are omitted.
  The recommendations are hypotheses, not measurements of waste or wasted
  resource-hours.
- **Subyard diagram:** copied unchanged from presentation 3; original source
  revision `dbf15e3ee96a249f153324167f7c06afd498a401`. It is a historical
  architecture illustration, not proof that every planned capability is shipped.
- **Current implementation references:** pinned to
  `c4348a10768abe619a8dc9fd073cf87353116085`. Profile selections are examples,
  not a report of deployed yards. AI Observer's retired profile is not offered
  as a current toggle.


The token-table raster is an edited publication derivative shared with
presentation 3. The worker-review slide uses native HTML rather than the source
screenshots. The architecture diagram is copied unchanged from presentation 3.
The terminal image is the original attachment from
[u/LovesWorkin's Reddit report](https://www.reddit.com/r/ClaudeAI/comments/1pgxckk/claude_cli_deleted_my_entire_home_directory_wiped/),
dated December 7, 2025, copied unchanged from presentation 4. It establishes
what the author reported; the incident and cause are not independently verified.
The [attachment](https://i.redd.it/egjqmw80bv5g1.png) is third-party material
and is not relicensed by this deck. New
diagrams are HTML/CSS. The QR is a deterministic encoding of the chosen URL;
the edited token raster is not an unchanged screenshot or a fresh measurement.

## Public image-edit evidence

Publication derivatives are made with the built-in imagegen tool. Edited UI
images are anonymized interface illustrations, not unchanged screenshots or
fresh measurements. The public edit instructions below describe the requested
replacements without reproducing private source strings.

| Asset group | Public edit instructions |
| --- | --- |
| Token table in presentations 3 and 5 | Use a solid, opaque black background. Remove the financial column and all money values. Preserve the remaining foreground, including the exact date, model and token strings. |
| OpenLIT custom evaluation | Replace the account with **John Doe** and the organization with **Example Organization**. Preserve the interface structure. |
| OpenLIT dashboard and remaining demo accounts | Use **John Doe** for the account and **JD** for account initials. |
| Demo filesystem details | Replace personal home-directory paths with `/home/john/project`. |
| Demo trace and session details | Use `example-trace` and `example-session` for trace and session identifiers. |
| Shared AI Observer dashboard | Use **Demo dashboard** for the browser label. |

The token raster was checked against the supplied original: OCR verified all
nine dates and 72 nonzero numeric cells, with one split OCR cell reassembled.
Zero cells and model labels were checked visually. All eight headline daily
totals match [`presentation3/data.json`](../presentation3/data.json). No financial
column remains. Image editing does not supply new measurement evidence.

The original MLflow trace on presentation 3, slide 7 remains unchanged under
D17's explicit exception. The Reddit terminal image reused from presentation 4
and the public Subyard architecture diagram also remain unchanged; they are
source material rather than generated derivatives. The worker-review prompt
and recommendations are anonymized native HTML, with the source screenshots
omitted from the public files.
