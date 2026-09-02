# Data files

Everything on [bench.chronicle.town](https://bench.chronicle.town) is derived from
the files in this directory. Licensing: CC BY 4.0 (see `LICENSE` here).

## `benchmark-v1.1.json` — the complete cohort record

The single source of truth for the v1.1 board. Top-level keys:

- `version`, `instrument` (`obr-v2.1-2026-03-08`, pinned), `protocol` (live page),
  `spend_usd` (total cohort generation spend).
- `boards.sustained` / `boards.free` — one row per model per arm: attempt
  denominators (`n_complete`, `n_eligible`, `n_scored`, `dnf`), pooled score
  (`sagascore`, with `_min`/`_max` across eligible novels), per-window means
  (`win_opening` … `win_ending`), and `human_percentile` (position within the
  36-novel published reference).
- `boards.human.band` — the published reference band: n, median/quartiles/min/max,
  per-stratum medians (plot / character / control), and the post-scoring
  **recognition split** (judge recognized 29/36; recognized median 65.5 vs
  unrecognized 54.5 — published, not argued away).
- `boards.human.books` — **per-novel scores for all 36 reference novels**,
  window by window.
- `runs` — all 175 recorded generation runs, including DNFs, stalls, withdrawn
  models and infrastructure failures. Per run: model, arm, brief, replicate,
  status, word count, generation cost, manuscript SHA-256 (first 16 hex chars),
  pinned provider, voluntary stop offsets, and per-window scores where scored.
- `deviations` — every place execution departed from the frozen protocol that is
  not already a numbered amendment (e.g. one window scored on 2 judge runs
  instead of 3).

## `runs-v1.1.csv`

The `runs` array flattened to CSV for spreadsheet use. Same content.

## `chronicle-x-opus.json` / `chronicle-x-sonnet.json` — system entries

Summary records for the two `Chronicle ×` system rows: configuration (disclosed
at mechanism level), preregistration reference, attempt denominators, pooled and
per-window scores, completion percentages, and generation spend. The Sonnet
entry's `provenance` block discloses the withdrawn outage round — see
[`docs/INCIDENT_2026-08-31_E2_Q10.md`](../docs/INCIDENT_2026-08-31_E2_Q10.md).
The Opus entry's preregistration is published verbatim:
[`docs/CHRONICLE_OPUS_PREREG.md`](../docs/CHRONICLE_OPUS_PREREG.md).

## `scores/` — full instrument output per scored window (system entries)

One JSON file per scored text: 5 positional windows plus a whole-book diagnostic
pass for each of the 6 books per entry (36 files per entry). Each file is the
pinned instrument's actual output: 8 rubric dimension scores, the deterministic
metric layer (sentence/paragraph statistics, lexical diversity, n-gram
repetition, dialogue ratio, …), computed Canon Integrity and Prose Authenticity,
caps applied (with reasons, when any), engagement-timeline summary, and the
judge's top issues with severity and locations. `runs: 3` marks the 3-run
temperature-0 median aggregation described in
[`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md).

Two normalizations against the internal originals, disclosed here: internal
filesystem paths and experiment labels are dropped, and the Prose Authenticity
fingerprint is summarized (total flags, patterns exceeded, severity) rather than
listed per pattern — the per-pattern detector taxonomy is part of the pinned
internal instrument, consistent with the reference-vs-pinned split described in
the README. Composite and all published numbers are unaffected.

Bare-model cohort scoring used the same instrument; its per-window results are
published in `benchmark-v1.1.json` (`runs[].window_scores`).

## `gutenberg-selection-manifest.json`

The deterministic seeded selection of the human reference corpus: Gutenberg IDs,
strata, seed string, eligibility filters, recorded exclusions, and manuscript
SHA-256 hashes — committed **before scoring**. The enforcement tightening and
the single content exclusion are amendment A3 in
[`docs/PROTOCOL-v1.1-full.md`](../docs/PROTOCOL-v1.1-full.md).

## `briefs/`

The two frozen commission briefs (B2, N1) used by every entrant and both system
entries.
