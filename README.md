# STOC 2027 — The Reading Room

Independent, AI-assisted reviews of the 1,665 manuscripts in the [STOC 2027 submission catalogue](https://stoc2027.sigact-ec.workers.dev), with a shortlist based on explicit rating criteria.

## Selection rule

Significance must equal 5; novelty, technical depth, and exposition must each be at least 4; at least one of those three must also equal 5. This qualifies 578 papers. Proof-audit status is informational and does not affect selection.

The approved shortlist has **466 papers**, approximately 28% of the 1,665-paper catalogue. The 28% rate is a user-chosen working target, not a verified current conference acceptance rate. All 367 papers above the weighted-score cutoff of 92 are retained. The remaining 99 positions are allocated among 211 papers tied at 92 using equal-weight STOC 2026 and FOCS 2026 topic proportions. Within-topic equal-score ties are resolved by submission number. Higher-scored papers are never displaced by lower-scored ones.

The allocation minimizes the sum over topics of `(selected count − target count)² / target count`, subject to the stronger-paper floor and available qualified manuscripts. It uses exact rational arithmetic. Historical topic shares are soft reference points, not official caps or area-specific acceptance rates. PC coverage is documented without converting committee membership into quotas. No SODA data is used.

The [topic comparison](topic-balance/) includes the 418-paper sensitivity at the verified FOCS 2025 rate of 137/546, plus STOC-only and FOCS-only topic scenarios. 450 papers are selected in all three 466-paper topic scenarios. It includes classifications, primary sources, uncertainties and committee-coverage examples.

Existing proof notes remain visible: 152 selected main arguments checked, 261 partial large-proof audits, 49 without a deep audit, and 4 with unresolved concerns. Recompute selection with `python3 scripts/update_shortlist.py`. This changes selection and metadata, not the underlying ratings or audits. The classification and reference inputs are preserved in `topic-balance/proposal.json` and `topic-balance/evidence/`.

## Review scope

- 1,665 individual screening records and ratings for significance, novelty, technical depth and exposition.
- 466 papers selected from 578 rating-qualified candidates.
- 25 manuscript-grounded desk-reject recommendations.
- Each record gives the inspected PDF pages, checks performed, qualifications and remaining proof obligations.

These are independent reading recommendations, not official STOC decisions or formal correctness certificates. A partial audit does not verify its remaining arguments. Closely scored papers should be read as a group; the website documents the tie policy.

## Hosting

This is a buildless static website. GitHub Pages publishes the root of the `main` branch; `.nojekyll` disables Jekyll processing. All browser assets and data use relative paths.

The main files are `index.html`, `style.css`, `app.js`, and `data.json`. The `audits/` directory contains supplementary verification artifacts where available. Saved-paper bookmarks stay in the visitor’s browser.

To preview locally, run `python3 -m http.server 8765` in this directory, then open http://localhost:8765.
