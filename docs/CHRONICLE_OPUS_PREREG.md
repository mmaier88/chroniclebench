<!-- Verbatim copy of the preregistration referenced by
data/chronicle-x-opus.json ("docs/CHRONICLE_OPUS_PREREG.md @cd8af9e").
Frozen before any generation; amendments O1/O2 are transport-only and were
recorded before the affected runs resumed. -->

# Chronicle × Opus — Preregistered Model-Swap Experiment (frozen before any generation)

**2026-09-01, owner-directed.** One question: is Chronicle a model-agnostic long-form
generation architecture, or a good Sonnet stack? This is a model-swap experiment, not a
tuning exercise.

## Hypotheses (stated in advance)

1. **Completion:** Chronicle materially improves Opus 5's ability to deliver a
   commissioned novel versus bare Opus on the neutral harness (bare Opus, A7 record:
   3 eligible novels in 12 attempts; failure modes: voluntary stall, continuation grind).
2. **Quality:** for books that complete, Opus's intrinsic prose quality survives the
   Chronicle scaffolding — eligible-book quality retained or improved versus
   Chronicle × Sonnet (production round: 68.3 pooled).

Prediction, worded for the record: Chronicle × Opus is predicted to materially improve
completion versus bare Opus while retaining or improving eligible-book quality. No
numeric quality target is preregistered.

## Frozen design

- **Engine:** the current production engine, byte-frozen — branch
  `engine/tailfork-production` @`2f94bc3` (attainment + fork-at-88% + K=2 selection +
  v003.2 chapterizer). **The ONLY code delta permitted is the enabling config: one new
  pinned model-policy registry entry for the writer** (slug `claude-opus-5`, params
  mirroring the Sonnet policy wherever Opus supports them, honest pricing snapshot).
  No prompt changes, no Opus-specific tuning of any kind, before or during the round —
  regardless of intermediate results. The writer policy is the only stage that swaps;
  every other stage (state extraction, tail selection judging via the writer policy path,
  repair, chapterization) runs exactly as the frozen engine wires it.
- **Commissions:** the SAME six as the comparable Chronicle × Sonnet production round —
  frozen briefs B2 (sci-fi) ×3 and N1 (family drama) ×3, 85,000-word commission, 300p
  production shape.
- **Execution:** staging engine (identical image + the policy entry; production stays
  untouched and frozen). All six run to terminal state regardless of intermediate
  outcomes; the only permitted rerun is a documented infrastructure failure (transport
  death before content), once, per the standing mechanical rule. Operational (disclosed,
  non-generative): staging's worst-case budget-guard rate env raised for Opus output
  pricing so the pre-call accumulator cannot abort a legitimate book.
- **Measurement order:** completion/attainment first (words, ratio, terminal prose,
  fork telemetry), then every eligible book (80–95K words) scored on the frozen pinned
  instrument — five 10K windows × 3-run medians, identical to every board row. DNFs
  publish as DNFs.
- **Publication:** ALL six outcomes publish, including failures — a separate
  **"Chronicle × Opus"** system entry alongside (never replacing) Chronicle × Sonnet.

## Interpretation (all three outcomes are useful)

| Result | Interpretation |
|---|---|
| High completion + quality above Sonnet-row | The harness unlocks frontier models — strongest demonstration of architecture value |
| High completion, quality ≈ Sonnet | Architecture solves completion; Sonnet already captures the available quality |
| Opus still stalls under the engine | Instability is partly model-specific — a real boundary condition; strengthens the Sonnet choice |

## Budget

~$15–25/book at Opus pricing (rolling prompt cache active) ≈ **$100–150 generation**
(Anthropic API) + ~$15 scoring. Owner-approved.

## Pre-run notes (recorded BEFORE generation)

1. **Zero code delta.** The frozen engine already contains the pinned Opus writer policy
   (`opus5-e5@1`, from the E5 challenger work: identical harness contract to the Sonnet
   policy — same per-call cap, streaming, caching, prompt version; only slug, pricing and
   `omitTemperature` differ, the latter because Opus 5 rejects sampling parameters). The
   experiment runs on the deploy already live; nothing is built or changed.
2. **Cost correction:** at actual Opus 5 pricing ($5/$25 per M) the round projects
   **~$35–50 generation**, below the approved envelope.
3. **Known, disclosed, untouched:** Opus 5 thinks by default and `max_tokens` caps
   thinking + prose together, so its prose-words-per-call may run lower than Sonnet's.
   Per the freeze, nothing is adjusted for this — the attainment loop absorbs short
   chunks by scheduling more of them, and any pacing difference publishes as a result,
   not a tuning input.

## Amendment O1 (2026-09-01, mid-round, operational only — recorded before resuming)

First runs surfaced a systematic **transport-ceiling artifact**: every failure across
three books was the identical `kind: timeout` at the engine's Sonnet-calibrated
**8-minute per-call ceiling** — Opus generating a 16K-token chunk plus mandatory thinking
legitimately exceeds it. This measures our timer, not the model, and answers neither
hypothesis. Remedy, mirroring the A7 pattern: transport timeout ceilings made
env-overridable (defaults unchanged; content-neutral — a timer changes which calls
survive, never what is generated; 1,271 tests green), staging set to
total-call 30 min / first-token 10 min / stream-idle 10 min via the env template.
The three affected books resume from their durable checkpoints per the standing
mechanical rule; no prose was lost, no prompts or generation parameters changed.
Production is untouched.

## Amendment O2 (2026-09-01, mid-round, operational only — recorded before resuming)

After O1 removed the timeout ceiling, a second systematic transport artifact surfaced:
intermittent failures classified `kind: unknown, action: fail` striking between and
during calls. Diagnosis was obstructed by long-standing error masking (plain
normalized-error objects stringified to "[object Object]"), now fixed. Root cause
hypothesis with strong circumstantial fit (load-correlated, six concurrent Opus books;
strikes both seconds and ~19 minutes into calls): **Anthropic mid-stream overload
errors carry no HTTP status** and fell through classification to `unknown`, which
permanently fails the job instead of retrying a retryable condition. Remedies, both
content-neutral transport handling: (1) status 529 / "overloaded" classified
`transient` (retryable); (2) terminal error messages now surface kind + message.
1,271 tests green. Affected books resume from durable checkpoints; two additional
interruptions during the O1 worker recreation (N1-r2/r3 at 24K words) are recorded as
mechanical restarts. No prompts or generation parameters changed; production untouched.

## RESULTS (2026-09-01 evening — both hypotheses CONFIRMED)

| Book | Words | % | Score (5-win) | Ending | Whole | Cost |
|---|---|---|---|---|---|---|
| B2-r1 | 83,736 | 98.5 | 77.82 | 76.3 | 77.5 | $6.72 |
| B2-r2 | 84,100 | 98.9 | 83.34 | **88.8** | 85.0 | $8.27 |
| B2-r3 | 83,966 | 98.8 | 80.06 | 85.0 | 83.8 | $6.08 |
| N1-r1 | 87,196 | 102.6 | 83.52 | 82.5 | 83.8 | $7.25 |
| N1-r2 | 84,549 | 99.5 | 83.52 | 82.5 | 83.8 | $7.91 |
| N1-r3 | 84,579 | 99.5 | 80.78 | 81.3 | 86.3 | $5.72 |

**Pooled: SagaScore 81.51 (77.8–83.5) · endings 82.73 · whole-book 83.37 ·
completion 6/6 eligible (99.8% mean) · $41.95 total generation.**

1. **Completion hypothesis: CONFIRMED.** Bare Opus: 3 eligible in 12 attempts.
   Chronicle × Opus: 6 of 6, every book 98.5–102.6% of commission, every fork fired.
2. **Quality hypothesis: CONFIRMED.** Bare Opus's 3 finishers pooled 82.97;
   Chronicle × Opus pooled 81.51 across ALL six — the intrinsic quality survives the
   scaffolding (delta within instrument noise), now delivered reliably instead of
   1-in-4. Endings — the historic collapse point — averaged 82.73 and were the
   strongest window on two books.
3. Reference (same pinned instrument): Chronicle × Sonnet production 68.3 · best
   reliable bare model (Sol) 73.4 · published-novel mean 65.3 / median 64.3 ·
   36-corpus maximum 93.3. Chronicle × Opus sits ≈ the 92nd percentile of the
   published reference.

Published per the freeze: separate "Chronicle × Opus" system entry on
bench.chronicle.town alongside Chronicle × Sonnet; all six books, all windows, raw
data in /chropus.json. Amendments O1/O2 (transport-only) stand as recorded. The
model-agnosticity thesis — frontier models write excellent prose; Chronicle turns it
into completed novels — now has its cleanest demonstration.
