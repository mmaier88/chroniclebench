# How books are judged

One instrument scores everything on the board — every AI window, every human reference
novel. Judge: **Claude Sonnet 4.6, temperature 0, three independent runs, median
aggregation**. The instrument is pinned (internal id `obr-v2.1-2026-03-08`) and never
changes mid-cohort.

## The three layers

1. **Deterministic layer (code, no LLM).** The text is measured mechanically —
   sentence-length variability, lexical diversity, repetition and structural metrics.
   These numbers are handed to the judge as consistency anchors and feed release
   gating in the full pinned instrument. The reference scorer in this repository
   implements the rubric layer, which determines the composite.
2. **LLM rubric layer.** Eight dimensions, each scored 1–10 **with mandatory verifiable
   evidence** — every score must cite 1–3 short quotes; outputs failing schema
   validation are rejected and re-run. The scale is anchored ("6–7: solid, no
   complaints" … "10: would hold up against a published novel in this dimension") and
   the judge is instructed as a measurement instrument, not a critic: the governing
   question is *"would a reader finish this book, and come back for another?"*
3. **Engagement timeline.** The judge segments the text into windows, scoring each
   1–10 with a controlled tag vocabulary (`strong_hook`, `tension_spike`,
   `filler_scene`, `pacing_sag`, `strong_close`, …) plus 3–5 top issues from a fixed
   diagnosis taxonomy.

## Dimensions and weights (profile `default_v2`)

| Dimension | Weight | A 10 means |
|---|---|---|
| Momentum | 0.15 | sustained curiosity, no perceptible drag |
| Voice & craft | 0.15 | indistinguishable from a confident human author |
| Emotional arc | 0.15 | genuine emotion shift; stakes that matter; payoff lands |
| Psychological specificity | 0.13 | inner lives that could not belong to anyone else |
| Characters | 0.12 | identifiable by dialogue alone |
| Coherence | 0.12 | zero logic breaks or continuity errors |
| Causal inevitability | 0.10 | surprising yet inevitable in retrospect |
| Promise delivery | 0.08 | delivers exactly what the premise promised |

**Composite** = weighted mean × 10 → a 0–100 score. The full pinned instrument applies
deterministic hard caps afterwards (e.g. a manuscript-level canonical contradiction of
a central identity caps the composite regardless of prose quality); caps and reasons
are recorded in every score file.

## From composites to the board

- **ChronicleBench Score** = mean of the five positional-window composites
  (opening / 25K / 50K / 75K / ending), each a 3-run median. Positional sampling is
  the design point: late-book collapse — the dominant AI failure mode at novel
  length — cannot hide behind a strong opening.
- A **whole-book composite** (single pass over the full manuscript) is recorded as a
  diagnostic; it is structurally more forgiving and never ranks the board.
- Entrant scores pool over **eligible novels (80–95K words) across all attempts**,
  with full denominators in the published data.

## Integrity measures and disclosed limitations

- Temperature 0 + 3-run medians damp residual judge nondeterminism; per-run outputs
  are archived with instrument hash, run count, weights and scoring cost.
- Texts are judged without model attribution; human novels are stripped of title,
  author and front matter, with a post-scoring recognition probe reported as a split.
- The judge shares a base model with one entrant and with Chronicle itself — a
  disclosed limitation, mitigated by the human-reference percentile framing and
  identical treatment of every text, not claimed away.
- Chronicle's engine internally uses a *separate* generic-craft judge for its own
  decisions — deliberately **not** this instrument — so the system cannot optimize to
  the benchmark rubric during generation.
- Scores are comparative measurements on a fixed instrument, not absolute literary
  judgments.
