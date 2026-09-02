# ChronicleBench

**An open, preregistered benchmark for sustained long-form generation: can an AI system
deliver a complete, commissioned novel — and how good is it, measured against published
fiction on one pinned instrument?**

Live board: **[bench.chronicle.town](https://bench.chronicle.town)** · built by
[Chronicle](https://chronicle.town), which also competes in it — read that disclosure as
a reason to check our work, not to take our word.

## Why this benchmark exists

Frontier models write excellent prose. Left alone with the commission *"write a complete
80–90,000-word novel"*, they stop at a median of ~13,000 words — a novella at best.
Every eligible AI novel in this benchmark exists because the model ran inside a
continuation harness. ChronicleBench measures two things nobody else measures at this
length:

1. **Sustain** — does the entrant deliver a commissioned novel at all (80–95K words)?
2. **Quality at position** — five 10,000-word windows (opening / 25K / 50K / 75K /
   ending) scored independently, so late-book collapse cannot hide behind a strong start.

## Headline results (v1.1 cohort + system entries, Sep 2026)

| Entrant | Score | Notes |
|---|---|---|
| Chronicle × Opus 5 | **81.5** | full engine, preregistered model swap |
| Chronicle × Sonnet (production) | 68.3 | full engine, production round |
| GPT-5.6 Sol (harness) | 73.4 | best bare-model result |
| GPT-5.6 Sol Pro (harness) | 70.3 | |
| Qwen 3.8 Max (harness) | 67.7 | |
| **Published-novel reference (36 books)** | **median 64.3 / mean 65.3** | Gutenberg corpus, seeded selection |
| 4 of 12 models | DNS | never reached novel length, even on the harness |

Every run — including failures, stalls, refusals and withdrawn models — is published in
[`data/`](data/). Nothing is selected after the fact.

## What's in this repository

| Path | Contents |
|---|---|
| [`docs/PROTOCOL.md`](docs/PROTOCOL.md) | The frozen v1.1 cohort protocol, verbatim, with every amendment |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | How books are judged: the instrument, rubric, weights, aggregation, limitations |
| [`instrument/`](instrument/) | Reference scorer: window cutter + 8-dimension LLM rubric scorer (3-run medians) |
| [`harness/`](harness/) | The **neutral entrant harness** — run any model on the benchmark yourself |
| [`data/`](data/) | Full results (JSON/CSV), per-book window scores, the human-corpus selection manifest |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | The standing procedure for adding a model (preregistration rules included) |

## What's deliberately NOT here

Chronicle's **generation engine is proprietary** and is not part of the benchmark. This
repository lets you *test* any system — including your own — under the same rules and
instrument; it does not contain Chronicle's planning, memory, pacing or repair machinery.
The `Chronicle ×` rows on the board are system entries produced by that engine; the
harness in this repo is the *neutral* one every bare-model row used.

## Quickstart — score a manuscript

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...

# 1. Cut the five positional windows (paragraph-boundary, tail-kept ending)
python instrument/cut_windows.py my-novel.txt out/windows 10000

# 2. Score each window (Claude Sonnet judge, temperature 0, 3-run median)
python instrument/score.py out/windows/my-novel--opening.txt --genre "science fiction"
# ... repeat for 25k / 50k / 75k / ending

# 3. ChronicleBench Score = mean of the five window composites
```

## Quickstart — run a model on the entrant harness

```bash
pip install requests
export OPENROUTER_API_KEY=...
python harness/sustained_run.py --model anthropic/claude-sonnet-4.6 --brief data/briefs/B2.txt
```

The harness is deliberately minimal: the frozen commission template, a neutral
`CONTINUE` on every stop, per-call word offsets recorded, hard word cap. That
minimalism is the point — it measures the *model*, not prompt engineering.

## Integrity properties

- **Preregistered**: protocol, briefs, roster, eligibility and scoring frozen and
  committed before generation; changes only via numbered public amendments.
- **One instrument**: the same pinned rubric judges every AI window and every human
  reference novel, temperature 0, 3-run medians.
- **Publish-all**: failures, DNFs, refusals and withdrawn models stay on the record.
- **Human anchor**: 36 published public-domain novels, deterministic seeded selection
  committed before scoring (see `data/gutenberg-selection-manifest.json`).

## A note on reference vs. pinned instrument

Official board scores come from Chronicle's pinned internal instrument
(`obr-v2.1-2026-03-08`), which includes deterministic cross-check metrics alongside the
LLM rubric. `instrument/score.py` is a faithful, self-contained reference
implementation of the rubric layer — the layer that determines the composite. If you
publish comparisons, state which implementation produced them.

## License

Code: MIT. Data and documentation: CC BY 4.0. Manuscript excerpts in `data/` derive
from Project Gutenberg (public domain) and Chronicle-generated text.
