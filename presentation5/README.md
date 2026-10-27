# Presentation 5: Running coding agents, 24/7

English, 15 slides, 16:9, 20–25 minutes. A personal account of running coding
agents continuously: isolation, complete toolchains, compute limits, brokered
resources, discoverable skills, minimal useful instructions and observability.
Subyard is a reference implementation.

- [Open the deck](index.html).
- [Download the PDF](running-coding-agents.pdf).
- [Read the speaker outline](notes.html): key idea, slide description, spoken
  explanation, timing and sources for every slide.
- [Read the research and evidence map](research.md).

The original broker topic is split into allocation and failure cleanup, so
the final deck has 15 slides. Slide 1 reuses the publication-safe token-table
raster from presentation 3; slide 11 uses an anonymized native HTML workflow
review; slide 12 reuses the original architecture diagram from presentation 3.
Slide 2 reuses the original terminal image from presentation 4.
Source attribution and numerical qualifications remain in
the speaker notes and research file.

## Present

Open `index.html` directly or serve this directory with a static web server.
The deck has no external runtime assets or dependencies. Use arrows,
Page Up/Page Down or Space to navigate, Home/End to jump, F for fullscreen,
and N for the current speaker notes. URL fragments such as `#7` select a slide.
The PDF button opens the committed export.

The public URL and QR target are
<https://subyard.github.io/usage-visibility/presentation5/>. Publishing requires
making this directory available through the repository's GitHub Pages host.
Creating these files does not publish them or alter the hosting configuration.

## Edit and export

Edit slide content in `index.html`, layout in `styles.css`, and the speaking
outline in `notes.html`. `deck.js` reuses presentation 4's navigation and adds
public link targets during printing, so shared PDFs do not point to local files.
Keep source evidence in `research.md`; do not add routine layout changes to
the project decision log.

Print the HTML using headless Chromium. For example, from the repository root:

```sh
/usr/bin/chromium --headless --no-sandbox --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/presentation5/running-coding-agents.pdf" \
  "file://$PWD/presentation5/index.html"
```

With Python Playwright, wait for fonts and images, then use:

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1600, "height": 956})
    page.goto(Path("presentation5/index.html").resolve().as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
    page.pdf(path="presentation5/running-coding-agents.pdf",
             prefer_css_page_size=True, print_background=True)
    browser.close()
```

The export must contain exactly 15 pages, each 1200 × 675 points. Check every
slide for clipping, overlapping text, broken assets and footer collisions;
verify navigation, note anchors, PDF links and QR decoding. The October 27
export used temporary Playwright Chromium tooling because system Chromium
was unavailable. Tooling is for export and verification only, not a deck
runtime dependency.

Verified October 27, 2026: 15 PDF pages with one slide each; no slide overflow
or footer collisions; keyboard/hash navigation and all 15 note anchors; local
asset loading; public PDF link targets; QR decoding from
both HTML and the printed PDF. Chromium rounds the page height to 675.12 points.
The nine existing repository tests and JavaScript syntax check passed.
The publication-sanitized export was rebuilt and all 15 pages visually reviewed.
The token raster's dates and 72 nonzero numeric cells were checked with OCR,
with one split cell reassembled; zero cells and model labels were checked
visually. All eight headline daily totals match `presentation3/data.json`.
Superseded private originals are absent from the current public tree.
Run `subyard-preview presentation5` from the repository root for a local preview.
GitHub Pages publication and Git history were not changed.

To regenerate the QR with Python's `qrcode` package:

```python
import qrcode
from qrcode.image.svg import SvgPathImage

url = "https://subyard.github.io/usage-visibility/presentation5/"
qrcode.make(url, image_factory=SvgPathImage, border=4).save(
    "presentation5/assets/presentation-qr.svg")
```
