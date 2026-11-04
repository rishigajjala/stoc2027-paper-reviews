# STOC 2027 — The Reading Room

Independent, AI-assisted reviews of the 1,665 manuscripts in the [STOC 2027 submission catalogue](https://stoc2027.sigact-ec.workers.dev), with a 400-paper reading shortlist.

## Review scope

- 1,665 individual screening records and ratings for significance, novelty, technical depth and exposition.
- 400 selected recommendations: 157 main arguments checked and 243 explicitly partial large-proof audits.
- 25 manuscript-grounded desk-reject recommendations.
- Each record gives the inspected PDF pages, checks performed, qualifications and remaining proof obligations.

These are independent reading recommendations, not official STOC decisions or formal correctness certificates. A partial audit does not verify its remaining arguments. Closely scored papers should be read as a group; the website documents the tie policy.

## Hosting

This is a buildless static website. GitHub Pages publishes the root of the `main` branch; `.nojekyll` disables Jekyll processing. All browser assets and data use relative paths.

The main files are `index.html`, `style.css`, `app.js`, and `data.json`. The `audits/` directory contains supplementary verification artifacts where available. Saved-paper bookmarks stay in the visitor’s browser.

To preview locally, run `python3 -m http.server 8765` in this directory, then open http://localhost:8765.
