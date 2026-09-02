<!-- Verbatim copy of the frozen cohort protocol (internal file
SAGABENCH_V1_1_PROTOCOL.md). The benchmark was developed under the working name
SagaBench and renamed ChronicleBench on 2026-09-01 (branding only). The live page
https://bench.chronicle.town/protocol-v1.1.html is generated from this same source
and remains the canonical rendering. -->

# SagaBench v1.1 — Cohort Protocol (FROZEN before generation)

**2026-08-21.** One contemporaneous cohort, all models via OpenRouter, uniform harness, no reuse of v1.0 generations. v1.0 is archived, never rewritten. This document is the canonical methodology reference and is mirrored publicly at `sagabench.vercel.app/protocol-v1.1.html`; every future model addition follows §6 verbatim.

**Amendment A7 (2026-09-01, owner-directed reliability extension):** additional sustained replicates under the unchanged frozen protocol — Opus 5: r4–r6 on both briefs (base cohort: 1 of 6 attempts reached eligible length; its single novel is the board's highest individual score) and Sol Pro: B2 r4 (B2-r3 finished at 95,748 words, 748 over the eligibility ceiling — the 94,000-word cap under-enforced by one final long call). Every attempt publishes; scores pool over all eligible novels with the full denominator shown. Budget guards $390→$490 total / opus5 $110→$200 for the approved extension (~$60–90); the account balance remains the true binding cap. The first three Opus attempts aborted on the pre-A7 guard before any content beyond one recorded call and were mechanically restarted, per §2.

**Amendment A2 (2026-08-21, mid-generation, owner-directed, operational only):** budget guards lowered from $900 total / $80 per-model to **$250 total / $60 per-model** at 63/168 runs complete ($41.05 spent; full-cohort projection ~$120–180). Guards are abort ceilings, not methodology — no generation parameter, roster, brief or scoring change rides along. Applied by restarting the per-model runners from their manifests (in-flight partial calls discarded and re-run clean, as with any mechanical restart).

**Amendment A6 (2026-08-21, late final stretch):** N1 sustained runs proved costlier than every projection (more stalls → more continuation calls); at 132/144 ($317.50) the remaining need (~$60–70) exceeded both the A5 guards and the account balance (~$56). Guards moved to $390/$110 — above the account ceiling — so that any stop records as an `Insufficient credits` infrastructure failure (resumable under §2) rather than a guard abort. The account balance, controlled solely by the owner, is the true binding budget from here; the owner was notified before departure. If the balance exhausts short of 144, the missing runs auto-resume on any future top-up via the standing supervisor.

**Amendment A5 (2026-08-21, owner-approved final stretch):** guards $320→$360 total, $80→$95 per-model at 113/144 roster runs ($249). Opus 5 and Sol Pro each projected ~$78–82 — a per-model trip within the last replicates would have left a top model partial. Final guard change; a box-side supervisor relaunches any guard-aborted session under the recalibrated guards, with the abort visible in the manifest.

**Amendment A4 (2026-08-21, owner-directed mid-generation):** (1) **Roster reduced 14→12**: Moonshot Kimi K3 (0/12 complete) and Z.AI GLM 5.3 (2/12) withdrawn by owner budget decision; their partial outputs publish as diagnostics only, never on any board; either may rejoin later via the §6 full-protocol procedure. (2) At 109/168 runs ($178.90) the OpenRouter account exhausted its credits; all affected runs failed with recorded `Insufficient credits` errors and were re-run after an owner top-up under §2's mechanical infrastructure-failure rule (transport failure, identical parameters). (3) Budget guards recalibrated $250→$320 total, $60→$80 per-model, owner-approved with the ~$265 expected total stated — the A2 guards sat below the corrected projection and a guard abort near completion would have forced a partial cohort, which §6.2 forbids on headline boards. No generation parameters changed.

**Amendment A3 (2026-08-21, BEFORE any reference-corpus scoring):** the first seeded Gutenberg selection surfaced candidates violating the preregistered eligibility rules in ways the automated filter could not see from gutendex metadata (publication language ≠ original language; collected-works volumes; multi-volume fragments; authorless anthologies). Enforcement was mechanized — translator-field + non-anglophone-author exclusion, title patterns for volumes/collections/abridgements, empty-author exclusion — and the selection re-run under the unchanged seed; superseded manifests are preserved. Additionally, one narrow content exclusion: works whose primary subject is the promotion of racial violence are excluded from the public reference corpus, recorded individually (applied once: Dixon's *The Clansman*). All exclusions are title-level and pre-scoring; no book was ever removed after being scored.

**Amendment A1 (2026-08-21, BEFORE any generation):** roster extended to 14 (GPT-5.6 Sol added alongside Sol Pro — both OpenAI configurations were requested); free-run arm upgraded to full 2 briefs × 3 replicates (parity with the sustained arm); one infrastructure-only smoke call per model precedes the scored cohort and never enters the benchmark; budget guards raised for the larger design ($900 total / $80 per model); §7 adds the preregistered Human Reference Corpus expansion. Nothing had been generated when A1 was committed.

## 1. Roster (pinned slugs + pinned providers, verified against the live OpenRouter catalogue 2026-08-21)

| Lab | Entry | Pinned slug | Pinned provider | Note |
|---|---|---|---|---|
| OpenAI | GPT-5.6 Sol | `openai/gpt-5.6-sol` | `openai` | v1.0 leader, rerun cleanly |
| OpenAI | GPT-5.6 Sol Pro | `openai/gpt-5.6-sol-pro` | `openai` | best available OpenAI configuration |
| Anthropic | Claude Opus 5 | `anthropic/claude-opus-5` | `anthropic` | flagship |
| Anthropic | Claude Fable 5 | `anthropic/claude-fable-5` | `anthropic` | creative-writing specialist; no temperature support |
| Anthropic | Claude Sonnet 4.6 | `anthropic/claude-sonnet-4.6` | `anthropic` | **required architecture control** (Chronicle's underlying model) |
| Google | Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` | `google-ai-studio` | |
| xAI | Grok 4.6 | `x-ai/grok-4.6` | `xai` | |
| DeepSeek | DeepSeek V4 Pro 0813 | `deepseek/deepseek-v4-pro-0813` | `alibaba` | **documented substitution (smoke phase):** first-party `deepseek` endpoint is blocked by the account's OpenRouter data-policy settings; same model slug, highest-capacity permitted host |
| Alibaba | Qwen 3.8 Max | `qwen/qwen3.8-max` | `alibaba` | sole provider |
| Meta | Llama 4 Maverick | `meta-llama/llama-4-maverick` | `deepinfra` | no first-party hosting exists; documented third-party host |
| Mistral | Mistral Medium 3.5 | `mistralai/mistral-medium-3-5` | `mistral` | sole provider |
| Moonshot | Kimi K3 | `moonshotai/kimi-k3` | `deepinfra` | no first-party hosting on OpenRouter; documented host |
| Z.AI | GLM 5.3 | `z-ai/glm-5.3` | `z-ai` | sole provider |
| MiniMax | MiniMax M3 | `minimax/minimax-m3` | `deepinfra` | no first-party hosting on OpenRouter; documented host |

Every recorded call captures: returned model, returned provider, request id, timestamp, request parameters and cost. Dropped from the headline roster: GPT-5.6 Terra (another OpenAI SKU, not another lab; its v1.0 result stays in the historical dashboard). Moving `latest`/alias slugs are prohibited.

## 2. Generation protocol (identical for every model, byte-identical harness to wave-1)

- **Briefs:** the two frozen program briefs B2 (science fiction) and N1 (ensemble family drama), verbatim from the corpus; template and briefs hashed into every manifest.
- **Arms per model × brief (A1):** **three free-run replicates** (continue only while `finish=length`; the model's own stop is the voluntary-length datum) and **three sustained replicates** (neutral `CONTINUE` after every call, including voluntary stops, until ≥85,000 words at a stop / stall / cap). Per-call word offsets are recorded so every voluntary stop survives into analysis. 14 models × 2 briefs × 6 runs = 168 scored runs.
- **Smoke phase (A1):** one infrastructure-only call per model (tiny fixed prompt, ~200 tokens) to surface API/schema incompatibilities before the runner freezes. Smoke outputs never enter the benchmark; a model is NOT excluded for a bad or refusing smoke — only genuine transport/schema fixes may result.
- **Explicit commission:** the generation template commissions a complete novel of 80,000–90,000 words (unchanged frozen wave-1 template; hash recorded).
- **Uniform parameters:** temperature 0.8 where the endpoint supports it (Fable and Sol-family reasoning endpoints do not; the harness's recorded 404-fallback drops temperature and logs `params_transformed`); `max_tokens` = min(32,768, provider completion cap); SSE streaming; 40-min per-call ceiling; hard word cap 94,000 (below the 95K eligibility ceiling so runaway generation cannot convert a run into an over-length DNF).
- **Provider discipline:** `provider: { only: [pinned], allow_fallbacks: false }`; the returned `provider` and `model` of every call are recorded in the per-run JSONL. A pinned-provider failure is a recorded failure, not a silent reroute.
- **No selection:** no discretionary reruns, no cherry-picks; refusals, stalls and failures remain visible in the manifest and on the public board. The only permitted rerun is a documented infrastructure failure (transport death before any content), re-run once under identical parameters.
- **Budget guards (A1, lowered by A2):** $250 total OpenRouter abort; $60 per-model abort — hitting a guard is a visible `failed` entry, never a quiet retry. Infrastructure failures (transport death before any content) may be rerun exactly once under the mechanical rule in §2; nothing else reruns.

## 3. Eligibility & scoring (v1.1 contract)

- **Eligibility band: 80,000–95,000 words** (replaces v1.0's defective 72,250 floor, which admitted books with no 75K window).
- **Five scoring windows for every entry:** opening / 25K / 50K / 75K / ending; SagaScore = mean of the five; pinned whole-instrument scoring, temp 0, 3-run medians — same instrument hash as v1.0.
- All v1.1 entries (including Chronicle) are scored uniformly across all five windows. Ineligible runs are still scored and published as DNF diagnostics.
- **Chronicle's entry** generates on the current production engine (2 briefs × 3 books, explicit 85K commission) after its length-calibration release passes its own frozen gates; it is a SYSTEM entrant and additionally reported against raw Sonnet 4.6 as the controlled architecture comparison.

## 4. What the public page may claim, by result

Three separate boards, never blended: (1) complete-novel SYSTEM entrants; (2) sustained model+standard-harness leaderboard; (3) short-horizon voluntary-generation leaderboard. The controlled Chronicle-vs-same-Sonnet exhibit stands independent of all three.

## 5. Archival

v1.0 (contract v1.0.1) remains published as the prior benchmark version with its own data file; nothing is rescored retroactively into it.

## 6. Standing procedure for adding ANY future model

1. Pin a concrete slug (no aliases) and a provider; verify both against the live catalogue; record completion/context caps.
2. Run the full §2 protocol — both arms, both briefs, all replicates, same parameters, same budget guards. **No partial cohorts on any headline board.**
3. Score per §3 with the pinned instrument version current for that cohort; if the instrument has changed, the entire cohort the model joins must be on the same instrument.
4. Publish the run manifests (per-call JSONL, provider/model as returned, costs, sha256 of every manuscript) alongside the scores; failures included.
5. Additions land as a dated cohort entry on the site with a changelog line; they never silently appear inside an existing cohort's table.
6. The public methodology footnote (`/protocol-v1.1.html`) is updated in the same change that adds the model.

## 7. Human Reference Corpus expansion (preregistered with A1)

**Goal:** grow the public-domain human reference from 14 to 50 novels; the existing 14 stay as legacy calibration anchors, never replaced or rescored away.

- **Additions:** 36 Project Gutenberg novels in three strata of 12: plot-forward (SF/mystery/adventure), character-forward (family/romance/social/literary), broader controls (horror/satire/historical/adjacent).
- **Eligibility:** originally English; complete single novel (no collections/plays/fragments); cleanly extractable prose; **80,000–95,000 cleaned words** (matching the v1.1 band); all five windows available; no duplicates/adaptations/alternate editions of anything in the corpus. If a stratum genuinely lacks 12 eligible works, the ceiling extends mechanically to 110,000 and those books are reported in a separate length-sensitivity analysis — never loosened on the basis of scores.
- **Selection:** build the full candidate pool with recorded exclusion reasons → assign genres before any scoring → select via a deterministic seeded procedure (seed string `sagabench-v1.1-gutenberg`, SHA-256 over sorted Gutenberg IDs) → commit the title list + manuscript SHA-256 hashes **before** scoring.
- **Preparation:** strip Gutenberg boilerplate, title, author and identifying front matter before judging.
- **Scoring:** identical five windows, identical pinned instrument, 3 judge runs per window — exactly as every v1.1 entrant.
- **Recognition probe:** after scoring, ask the judge whether it can identify each work; recognized books are never excluded post hoc; recognized-vs-unrecognized is reported as a robustness split.
- **Reporting:** median + IQR human band; full distribution; per-stratum results; per-window distributions; Chronicle and per-model percentiles with uncertainty; 14-book vs 50-book comparison.
- **Naming & framing:** "Human reference corpus: published public-domain novels" — never "average bookstore book" or a claim about contemporary publishing; survivorship, historical style, training contamination and judge recognition are disclosed limitations. Human novels are a reference band, not contestants under the commission.

**Clarification (2026-08-31, post-scoring):** the published v1.1 five-window human band is computed over the 36 newly selected books only. The 14 legacy calibration novels were scored under the v1.0 contract, whose SagaScore aggregates four windows rather than v1.1's five, so their scores are a different metric object; they remain published as v1.0 calibration anchors rather than being mixed into the v1.1 band — the "legacy calibration anchors, never replaced or rescored away" treatment preregistered above.

## 8. Claims discipline (binding)

"#1 full-novel system" only after real system competitors are tested. "Best-performing complete-novel generator tested" only if Chronicle wins under the frozen contract and uncertainty treatment. Ties reported as ties. No superiority-to-classics claims from small or selected subsets — percentile language against the full 50-book reference. Chronicle losses publish exactly like any other loss. The live site (/, /pilot.html, /chronicle.html) is not restructured until the cohort completes and results are reviewed; v1.1 outputs build separately for review.