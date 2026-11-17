# Articles

Personal articles, one folder per article. Each article builds into a single
self-contained `index.html` (photos inlined), so it can be hosted anywhere or
sent as one file.

- `web-summit-2026/` — Lisbon, robots and the storm: Web Summit 2026.
  - `photos/` — source photos, EXIF/GPS removed.
  - `build.py` — rebuilds `index.html` (`python3 web-summit-2026/build.py`, needs Pillow).
- `shared/dancing-robots-header.html` — reusable animated header; copy the block
  between `HEADER:BEGIN` and `HEADER:END` into a page.

Published with GitHub Pages from the `main` branch.
