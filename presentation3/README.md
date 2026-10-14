# Presentation 3

An HTML presentation prepared one slide at a time as content is supplied.
Open [`index.html`](index.html) in a browser. Use its PDF action to print or save
all slides, or run the export command below to create `usage-visibility.pdf`.

## Requested original images — pending

The user requires all four supplied images to be preserved in `img/` and the
right-hand chart on slide 1 to be replaced by the original token-usage image.
The attachments are visible in the conversation but their original image files
are not available to the workspace tools. The current HTML still has the chart
and the slide 3–4 summaries described below; these do not fulfill the requested
image-based layout. Do not treat the existing official dashboard image as the
user's annotated original.

Expected original assets:

- `img/token-usage-original.png` — slide 1, right side instead of the chart.
- `img/ai-observer-all-tools-original.png` — slide 2, supplied annotated image.
- `img/ai-observer-default-dashboard-original.png` — slide 3.
- `img/ai-observer-metrics-original.png` — slide 4.

Use the actual source extension if it differs from PNG. Once the files are
available, update the image references and layouts, then rebuild and visually
verify the PDF. The filenames above are intended destinations, not existing
files.

## Current content

Slide 1: **13.4 billion tokens in 8 days**, October 6–13, 2026.
The user describes roughly 5–7 sessions running nearly 24/7. This is operating
context, not an exact session count or a measured concurrency claim.

[`data.json`](data.json) transcribes the eight daily token totals from the
user's screenshot. The identical All and Codex rows are counted once per day.
The total column has no visible header, but each value equals the sum of the
three nonzero preceding token columns. No breakdown labels are inferred.
The sum is 13,396,361,355; the daily average is 1,674,545,169.375. The chart
uses a shared zero-based 2-billion-token scale. These totals measure volume
and do not establish spend, waste or efficiency.

Slide 2: **AI Observer All Tools dashboard.** Reuses the matching official image
from presentation 2, with the five numbered callouts from the user's supplied
slide. The image is example data, not a result from the local instance.

Slide 3: **AI Observer Default Dashboard.** The user-supplied Last 1 hour view
lists Codex CLI as an active service, 829,535 metric points, 210,553 logs, zero
traces/spans and a displayed 0.00% error rate. It shows no recent traces.

Slide 4: **AI Observer Metrics selector.** The user-supplied view shows Claude
Code and Gemini CLI groups, All Services, Last 15 minutes, no selected metric
and a 146 real-time updates counter. Only fully visible menu entries are listed;
the capture does not establish a complete metric or agent catalog.

The user confirmed that the Default Dashboard is slide 3 and the earlier Metrics
selector moves to slide 4. Slides 3 and 4 currently use labeled text summaries:
the screenshots are visible in chat but their image files are not available in
the workspace. Replace these summaries with the supplied originals when the
files are available. No internal host addresses or session content are included.

## Add the next slide

Insert a new `<section class="slide" id="slide-5" aria-labelledby="title-5">`
inside `#deck`, with an `h1` or `h2` carrying `id="title-5"`. Continue unique
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

The initial export on October 14 could not run in the current execution
environment: Chromium failed with `shutdown: Operation not permitted`, including
when launched with elevated tool permissions and single-process mode. The PDF
is not yet generated, and visual layout verification remains pending. Run the
export in the Yard or another environment that permits Chromium's system calls.
