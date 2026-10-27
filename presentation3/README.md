# Presentation 3

An HTML presentation prepared one slide at a time as content is supplied.
Open [`index.html`](index.html) in a browser. Use its PDF action to print or save
all slides, or run the export command below to create `usage-visibility.pdf`.

## Image sources and publication edits

Slide 1 uses a publication-safe raster recreated from the supplied token table
in [`img/token-usage-public.png`](img/token-usage-public.png). It has a solid
black background, retains the dates, model names and daily token totals, and
omits the financial column. It includes October 5–13; the headline and average
still count October 6–13 only, excluding October 5. The raster is an edited
derivative rather than the original screenshot.

The original Default Dashboard screenshot is saved unchanged in
[`img/ai-observer-default-dashboard-original.png`](img/ai-observer-default-dashboard-original.png)
and is the main content of slide 5.

The original Metrics screenshot is saved unchanged in
[`img/ai-observer-metrics-original.png`](img/ai-observer-metrics-original.png)
and is the main content of slide 6.

The original MLflow trace screenshot is saved unchanged in
[`img/mlflow-trace-original.jpg`](img/mlflow-trace-original.jpg) and opens the
MLflow section on slide 7. Its trace identifiers and instructions are retained
as the explicit publication exception in D17.

The remaining original image file is still pending:

- `img/ai-observer-all-tools-original.png` — slide 4, supplied annotated image.

Use the actual source extension if it differs from PNG. The filename above
is an intended destination, not an existing file. Do not treat the existing
official dashboard image as the user's annotated original. Once the files are
available, update the image references and layouts, then rebuild and visually
verify the PDF.

## Subyard image source

The README diagram is copied unchanged from
[`docs/assets/agent-workspace.webp`](https://github.com/subyard/subyard/blob/dbf15e3ee96a249f153324167f7c06afd498a401/docs/assets/agent-workspace.webp)
at commit `dbf15e3ee96a249f153324167f7c06afd498a401`. Its local copy is
[`img/subyard-agent-workspace.webp`](img/subyard-agent-workspace.webp).

## Current content

Slide 1: **13.4 billion tokens in 8 days**, October 6–13, 2026.
The user describes roughly 5–7 sessions running nearly 24/7, with many sessions
lasting 20–40 hours. This is user-supplied operating context, not an exact session
count, a measured concurrency claim or durations inferred from the usage screenshot.

[`data.json`](data.json) transcribes the eight daily token totals from the
user's screenshot. The identical All and Codex rows are counted once per day.
The total column has no visible header, but each value equals the sum of the
three nonzero preceding token columns. No breakdown labels are inferred.
The sum is 13,396,361,355; the daily average is 1,674,545,169.375. These totals
measure volume and do not establish spend, waste or efficiency.

Slide 2: **Subyard — Workspaces for coding agents.** Uses the architecture
image from the project's README, saved as `img/subyard-agent-workspace.webp`,
and links to [github.com/subyard/subyard](https://github.com/subyard/subyard).
The diagram shows local and remote yards, agents and shared staging, SSH
management, Git settings and encrypted staging credentials. A context column
explains isolation, shared staging and host management beside the slightly
smaller diagram, with a large, high-contrast repository link. Subyard is a
reference environment; the visibility solution must also work without it (D2).

Slide 3: **What each harness records and exports.** Compares Codex CLI,
Claude Code and OpenCode by collection method: local records, configurable
metrics/events, and optional timed spans. These are our comparison categories,
not vendor-defined levels; traces are a type of telemetry. Each column lists
concrete records and collection controls. Claude Code tracing is beta. OpenCode
v1.19.0 has native OTLP/HTTP logs and traces, enabled by a collector endpoint;
`experimental.openTelemetry` adds AI SDK call spans. Community OTLP metrics
and ready-made MLflow/Langfuse tracing plugins are documented separately.
This corrects the earlier development-source-only review that marked native
trace export unverified and implied a custom adapter was necessary.
Local usage fields are source/version/provider-dependent; OpenCode CLI source
is pinned to release commit `733b2c627e5aec39cb33cc22373bdce33053ef2c`.
Claude Code's 30-day cleanup applies to CLI session transcripts, not all stats.
Codex OTel controls belong in user-level configuration. D13's implementation
priorities are unchanged. Official documentation and source references are in
Sources, rechecked October 14, 2026; live exports were not tested.
The highlighted integration work is normalization, task/agent/step correlation
and process CPU/RAM collection.

Slide 4: **AI Observer All Tools dashboard.** Reuses the matching official image
from presentation 2, with the five numbered callouts from the user's supplied
slide. The shared publication asset is an anonymized interface illustration
with the browser label **Demo dashboard**. It is edited example data, not an
unchanged screenshot or a fresh measurement from the local instance.

Slide 5: **AI Observer Default Dashboard.** The user-supplied Last 1 hour view
lists Codex CLI as an active service, 830,397 metric points, 210,782 logs, zero
traces/spans and a displayed 0.00% error rate. It shows no recent traces.

Slide 6: **AI Observer Metrics selector.** The user-supplied view shows Claude
Code and Gemini CLI groups, All Services, Last 15 minutes, no selected metric
and a 697 real-time updates counter. The visible Gemini CLI entries include Lines
Changed and Memory Usage; the capture does not establish a complete metric
or agent catalog.

With the harness comparison inserted as slide 3, the Default Dashboard is slide 5 and
the Metrics selector is slide 6. Both slides display the supplied original screenshots.
No internal host addresses or session content are included.

Slide 7: **MLflow Trace explorer.** The original MLflow 3.17.0 screenshot shows
a trace marked Success, the span hierarchy and timings on the left, and the
selected LLM call's attributes on the right. The image includes the supplied
browser chrome and trace details. No live instance was accessed or candidate
ratings changed.

Slide 8: **OpenLIT LLM dashboard.** Opens the OpenLIT section with an anonymized
interface illustration based on the supplied v2.1.0 dashboard, saved as
`img/openlit-llm-dashboard-public.png`, with the account **John Doe**.
The selected 24H view displays 7.11M
requests, 0.6487 seconds average duration, zero average tokens per request,
$0 costs and zero detection counters. These are source UI values shown for
interface context, not fresh measurements. Collection and evaluation coverage
and the underlying measurements were not verified.

Slide 9: **OpenLIT Custom evaluations.** The supplied OpenLIT v2.1.1
screenshot shows the evaluation type fields and judge prompt, plus guidance on
judge outputs and trace-based Rule Engine conditions. The publication copy in
`img/openlit-custom-evaluation-public.png` uses the generic account **John Doe**
and organization **Example Organization**. This is an edited setup view, not a
completed evaluation or a verified live integration. Like the other edited UI
images, it is an anonymized interface illustration rather than an unchanged
screenshot.

All slides use the same compact header with a fixed slide number/topic position.
Content slides also share title sizing and alignment. A flexible body centers
each image or content group between the header and footer. The closing title
is part of its centered message. Screenshots retain their original proportions
without cropping; click an image to open the full-resolution displayed asset.

Slide 10: **Ask the worker agent how to improve.** An anonymized native HTML
prompt asks for a workflow review. Four generic recommendations cover less
coordination chatter, selective reruns, early prerequisite checks and releasing
resources when finished. The original review screenshots, exact session counts
and internal incident details are omitted from the publication copy. The
recommendations are hypotheses to validate; necessary waiting and coordination
are not automatically waste, and no exact wasted VM-hours are established.

Slide 11: **Thank you.** Closing message: “LLMs are great tools. Use them wisely.”

## Add the next slide

Insert a new `<section class="slide" id="slide-12" aria-labelledby="title-12">`
inside `#deck`, with an `h1` or `h2` carrying `id="title-12"`. Continue unique
numbering for later slides. Navigation, progress indicators, the slide counter
and print pagination discover all `.slide` sections automatically. Update the
fallback counter in the HTML and this content list when adding slides.

Use arrow keys or Page Up / Page Down to navigate, Home / End to jump, F for
fullscreen, and All slides for overview. Sources opens the calculation notes.
The deck works directly from a local file without a web server or dependencies.
The toolbar is 44px high and navigation is 48px high. Their combined height is
defined once in CSS. On desktop windows wider than 900px, slides share a
1600×900 (16:9) composition with the PDF and scale to the available viewport
below the toolbar and above navigation. The complete slide remains visible without vertical scrolling.
At narrower widths, content reflows and can scroll vertically; the comparison
table has its own horizontal scrolling area. Displayed image assets remain uncropped.

## Rebuild and verify the PDF

From the repository root:

```sh
/usr/bin/chromium --headless --no-sandbox --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/presentation3/usage-visibility.pdf" \
  "file://$PWD/presentation3/index.html"
pdfinfo presentation3/usage-visibility.pdf
```

Chromium prints the HTML with its print stylesheet and backgrounds. Each slide
must occupy one 16:9 page (1200×675 PDF points). Verify the page count against the slide
count and render every PDF page with `pdftoppm` for visual inspection; check
for clipped text, chart labels and footnotes before delivering an update.

The October 14 export succeeded using a temporary Playwright Chromium headless
installation, with `prefer_css_page_size=True` and `print_background=True`.
[`usage-visibility.pdf`](usage-visibility.pdf) contains eleven 16:9 pages,
one per slide. All eleven browser print layouts pass overflow checks, and all
PDF pages were visually reviewed.

The screen composition was checked on all 11 slides at 1920×1080, 1440×900,
1366×768 and 1024×768: slide content and navigation fit the viewport, and
content stays inside its body area. At 900×700, 390×844 and 320×640 there is no
document-wide horizontal overflow. Header positions match across slides.
Overview switching and opening an image in a new tab were verified.

The token table, shared AI Observer dashboard and both OpenLIT images are
publication derivatives; the worker review is native HTML. These are not
byte-identical copies of the supplied originals. Slide 7 deliberately retains
its original MLflow trace.

The publication-sanitized PDF was rebuilt on October 27, 2026 with headless
Chromium: eleven 16:9 pages, one per slide, all visually reviewed. Print overflow,
image loading, local links and navigation checks passed. The token raster's
dates and 72 nonzero numeric cells were OCR-checked against the supplied table
(one split OCR cell was reassembled); zeros and model labels were checked
visually, and all eight headline daily totals match `data.json`. Presentation
3 slide 7's HTML and original image remain byte-identical to their pre-cleanup
versions. Git history was not changed.
