# ChronicleBench v1.1 — Cohort Protocol (frozen)

Canonical, verbatim version with every amendment:
**[bench.chronicle.town/protocol-v1.1.html](https://bench.chronicle.town/protocol-v1.1.html)**.
This document is a faithful summary for repository use; where wording differs, the live
protocol page governs. The benchmark was developed under the working name *SagaBench*
and renamed *ChronicleBench* on 2026-09-01 (branding only; nothing methodological
changed).

## 1. Design

- **One contemporaneous cohort.** 12 models (originally 14; two withdrawn by documented
  amendment) × 2 frozen briefs × (3 sustained + 3 free-run) replicates, all via
  OpenRouter with **pinned model slugs and pinned providers**, `allow_fallbacks: false`.
  Moving/alias slugs prohibited. Every call records returned model, provider, request
  id, parameters and cost.
- **Two arms.** *Free-run*: continue only while `finish == length` — the model's own
  stop is the voluntary-length datum. *Sustained*: a neutral `CONTINUE` after every
  stop until ≥85,000 words, a stall, or the cap. Per-call word offsets are recorded.
- **The commission** (frozen template, hash recorded in every manifest): a complete
  novel of 80,000–90,000 words; manuscript prose only; no commentary. See
  `harness/sustained_run.py` for the verbatim template.
- **Uniform parameters**: temperature 0.8 where supported (documented parameter-relax
  fallback where an endpoint rejects sampling params); `max_tokens` =
  min(32,768, provider cap); SSE streaming; 40-minute per-call ceiling; hard word cap
  94,000 (below the eligibility ceiling so runaway generation cannot become an
  over-length DNF).
- **No selection.** No discretionary reruns, no cherry-picks. The only permitted rerun
  is a documented infrastructure failure (transport death), once, identical parameters.
  Refusals, stalls and failures stay visible in the manifests and on the board.

## 2. Eligibility & scoring

- **Eligibility band: 80,000–95,000 words.** Ineligible runs are still scored where
  possible and published as DNF diagnostics.
- **Five scoring windows per entry** — opening / 25K / 50K / 75K / ending — 10,000
  words each, cut on paragraph boundaries; the ending window keeps its tail (the
  closing passage is the point). See `instrument/cut_windows.py`.
- **ChronicleBench Score** = mean of the five window composites. Each window composite
  is the **median of 3 independent judge runs** at temperature 0 on the pinned
  instrument. See `docs/METHODOLOGY.md`.
- **System entries** (e.g. `Chronicle ×` rows) run the same commissions end-to-end
  through a complete generation system and are scored identically; they are labeled
  as system entries and never blended with bare-model rows.

## 3. Human reference corpus

36 published public-domain novels (plus 14 legacy calibration anchors), three genre
strata × 12, selected by a **deterministic seeded procedure** with the title list and
manuscript SHA-256 hashes committed **before scoring**
(`data/gutenberg-selection-manifest.json`). Eligibility: originally English, complete
single novel, 80,000–95,000 cleaned words, all five windows available. Boilerplate,
title and author stripped before judging; a post-scoring recognition probe is reported
as a robustness split. Framing rule: this is a *published public-domain reference
band* — survivorship, historical style, training contamination and judge recognition
are disclosed limitations, never argued away.

## 4. Amendment discipline

The protocol changes only by numbered, dated, public amendments recorded before (or,
for operational aborts, at the moment of) the affected work — never silently. The live
protocol page carries A1–A7 plus experiment-level amendments verbatim, covering: design
extension before generation (A1); budget-guard changes with spend visible (A2, A4–A6);
mechanized corpus-eligibility enforcement before any scoring (A3); and the Opus/Sol-Pro
reliability extension with full-denominator pooling (A7). Operational amendments never
change generation parameters, prompts or scoring.

## 5. Standing procedure for adding ANY model

1. Pin a concrete slug (no aliases) and provider; verify against the live catalogue;
   record completion/context caps.
2. Run the full protocol — both arms, both briefs, all replicates, same parameters.
   **No partial cohorts on any headline board.**
3. Score with the pinned instrument version current for that cohort.
4. Publish the run manifests (per-call JSONL, provider/model as returned, costs,
   manuscript SHA-256) alongside the scores — failures included.
5. Additions land as a dated cohort entry with a changelog line; the methodology page
   updates in the same change.

## 6. Claims discipline (binding)

Ties are reported as ties. No superiority-to-classics claims from small or selected
subsets — percentile language against the full reference corpus only. The benchmark's
operator (Chronicle) competes in it; its losses publish exactly like any other loss.
