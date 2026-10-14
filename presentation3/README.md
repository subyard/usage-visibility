# Presentation 3

An HTML presentation prepared one slide at a time as content is supplied.
Open [`index.html`](index.html) in a browser. Use its PDF action to print or save
all slides, or run the export command below to create `usage-visibility.pdf`.

## Requested original images — four saved, one pending

The original token-usage screenshot is saved unchanged in
[`img/token-usage-original.png`](img/token-usage-original.png) and replaces the
right-hand chart on slide 1. It includes October 5–13; the headline and average
still count October 6–13 only, excluding October 5. Slide 1 uses narrow margins
and gives most of the width to the screenshot, with compact figures on the left.

The original Default Dashboard screenshot is saved unchanged in
[`img/ai-observer-default-dashboard-original.png`](img/ai-observer-default-dashboard-original.png)
and is the main content of slide 5.

The original Metrics screenshot is saved unchanged in
[`img/ai-observer-metrics-original.png`](img/ai-observer-metrics-original.png)
and is the main content of slide 6.

The original MLflow trace screenshot is saved unchanged in
[`img/mlflow-trace-original.jpg`](img/mlflow-trace-original.jpg) and opens the
MLflow section on slide 7.

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
The user describes roughly 5–7 sessions running nearly 24/7. This is operating
context, not an exact session count or a measured concurrency claim.

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

Slide 3: **Two harnesses. Three data layers.** Compares required Codex CLI and
Claude Code support (D13): default local records, optional OTel export, and
separately enabled trace spans. Claude Code native tracing is labeled beta.
OpenCode remains optional. The highlighted project gap is process CPU/RAM and
cross-harness task/agent/step attribution. Official source links and configuration
caveats are in Sources; checked October 14, 2026, without testing live exports.

Slide 4: **AI Observer All Tools dashboard.** Reuses the matching official image
from presentation 2, with the five numbered callouts from the user's supplied
slide. The image is example data, not a result from the local instance.

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

Slides 6 and 7 place compact titles to the left of enlarged, right-aligned
screenshots, using the title area for image height. On narrow screens, titles
and images stack vertically. Full originals remain visible without cropping.

## Add the next slide

Insert a new `<section class="slide" id="slide-8" aria-labelledby="title-8">`
inside `#deck`, with an `h1` or `h2` carrying `id="title-8"`. Continue unique
numbering for later slides. Navigation, progress indicators, the slide counter
and print pagination discover all `.slide` sections automatically. Update the
fallback counter in the HTML and this content list when adding slides.

Use arrow keys or Page Up / Page Down to navigate, Home / End to jump, F for
fullscreen, and All slides for overview. Sources opens the calculation notes.
The deck works directly from a local file without a web server or dependencies.

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
must occupy one A4 landscape page. Verify the page count against the slide
count and render every PDF page with `pdftoppm` for visual inspection; check
for clipped text, chart labels and footnotes before delivering an update.

The October 14 export succeeded using a temporary Playwright Chromium headless
installation, with `preferCSSPageSize: true` and `printBackground: true`.
[`usage-visibility.pdf`](usage-visibility.pdf) contains seven A4 landscape pages,
one per slide. All seven browser print layouts were visually checked and had no
layout overflow. All four saved original screenshots were verified byte for byte
against their attachments.
