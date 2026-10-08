Do not write to input folder. Only humans write there.

Write all repository content in English.

Record requirements and decisions in `docs/decisions.md`. Compare candidate
tools in `solutions/`, one file per candidate based on `solutions/_template.md`.

After changing a presentation, rebuild its PDF by printing `index.html` with
headless Chromium (`/usr/bin/chromium` in the Yard; for example Playwright
`page.pdf` with `prefer_css_page_size` and `print_background`). Check that
every slide fits on one page.
