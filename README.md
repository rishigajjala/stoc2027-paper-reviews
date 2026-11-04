# STOC 2027 — The Reading Room

Independent, AI-assisted reviews of the 1,665 manuscripts in the [STOC 2027 submission catalogue](https://stoc2027.sigact-ec.workers.dev), with a shortlist based on explicit rating criteria.

## Selection rule

Significance must equal 5; novelty, technical depth, and exposition must each be at least 4; at least one of those three must also equal 5. Proof-audit status is informational and does not affect selection. There is no fixed count cap. The weighted merit score determines display order, with ties ordered by submission number.

All 578 papers meeting the rating threshold are selected. Existing proof notes remain visible: 172 main arguments checked, 296 partial large-proof audits, 106 without a deep audit, and 4 with unresolved concerns. Recompute selection from the recorded reviews with `python3 scripts/update_shortlist.py`. This updates selection, not the underlying ratings or audits.

## Review scope

- 1,665 individual screening records and ratings for significance, novelty, technical depth and exposition.
- 578 papers selected by ratings alone.
- 25 manuscript-grounded desk-reject recommendations.
- Each record gives the inspected PDF pages, checks performed, qualifications and remaining proof obligations.

These are independent reading recommendations, not official STOC decisions or formal correctness certificates. A partial audit does not verify its remaining arguments. Closely scored papers should be read as a group; the website documents the tie policy.

## Hosting

This is a buildless static website. GitHub Pages publishes the root of the `main` branch; `.nojekyll` disables Jekyll processing. All browser assets and data use relative paths.

The main files are `index.html`, `style.css`, `app.js`, and `data.json`. The `audits/` directory contains supplementary verification artifacts where available. Saved-paper bookmarks stay in the visitor’s browser.

To preview locally, run `python3 -m http.server 8765` in this directory, then open http://localhost:8765.
