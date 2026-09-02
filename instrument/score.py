#!/usr/bin/env python3
"""ChronicleBench reference scorer — the 8-dimension LLM rubric layer.

Scores one text window (or a whole manuscript) with the documented ChronicleBench
rubric: 8 dimensions, 1-10 each with mandatory evidence citations, judged by Claude
Sonnet at temperature 0, N independent runs (default 3), median composite.

  python score.py window.txt [--runs 3] [--genre "science fiction"] [--title "Untitled"]

Output: <window>.score.json next to the input, with per-run and median results.

This is a faithful, self-contained re-implementation of the rubric layer of
Chronicle's pinned internal instrument (obr-v2.1-2026-03-08). The pinned instrument
additionally computes deterministic cross-check metrics (sentence-length variability,
lexical diversity, repetition analysis) that are provided to the judge as consistency
anchors and feed release-gating; the composite that ranks the board is the weighted
rubric mean implemented here. If you publish comparisons, state which implementation
produced your numbers.
"""
import argparse, json, re, statistics, sys
from pathlib import Path

import anthropic

JUDGE_MODEL = "claude-sonnet-4-6"

WEIGHTS = {  # profile default_v2 — used for all benchmark scoring
    "momentum": 0.15,
    "voice_craft": 0.15,
    "characters": 0.12,
    "psychological_specificity": 0.13,
    "emotional_arc": 0.15,
    "coherence": 0.12,
    "promise_delivery": 0.08,
    "causal_inevitability": 0.10,
}

ENGAGEMENT_TAGS = [
    "strong_hook", "setup", "cold_entry", "info_dump", "emotional_plateau",
    "repetitive_scaffolding", "curiosity_gap_opened", "tension_spike",
    "clarity_break", "character_conflict_peak", "payoff_moment", "filler_scene",
    "voice_drift", "pacing_rush", "strong_close",
]
DIAGNOSIS_TAGS = [
    "cold_entry", "info_dump", "emotional_plateau", "repetitive_scaffolding",
    "character_blur", "pacing_sag", "voice_drift", "continuity_break",
    "promise_miss", "ai_ism_detected", "dialogue_flatness", "stakes_absent",
    "resolution_rushed", "filler_padding", "theme_incoherence",
    "causal_gap", "psychological_flatness",
]

SYSTEM_PROMPT = f"""You are a literary quality evaluator. Your job is to produce an objective, evidence-based assessment of a passage of long-form fiction.

You are NOT a literary critic. You are a measurement instrument. Your goal is to answer: "Would a reader finish this book, and would they come back for another?"

## Scoring Scale (1-10)
- 1-3: Clear, identifiable problem that would hurt the reading experience
- 4-5: Noticeable weakness a reader would register
- 6-7: Solid, no complaints — meets expectations
- 8-9: Notably good — would impress a reader
- 10: Would hold up against a published novel in this dimension

## Dimensions

### Momentum (key: "momentum")
Hook strength, scene entry speed, pull-through, absence of sag. A 10 means sustained curiosity with no perceptible drag.

### Voice & Craft (key: "voice_craft")
Voice consistency, absence of AI-isms, sentence variety, show-vs-tell balance. A 10 means indistinguishable from a confident human author.

### Characters (key: "characters")
Distinctiveness of dialogue voices, clear desires and conflicts, character growth or change. A 10 means you could identify characters by dialogue alone.

### Psychological Specificity (key: "psychological_specificity")
Internal contradictions within characters, motivational complexity beyond stated goals, emotional texture that goes beyond labeling feelings, cognitive model distinctness per character. A 10 means characters have rich, specific inner lives that could not belong to anyone else.

### Emotional Arc (key: "emotional_arc")
Tension escalation, stakes that matter, emotional range (not monotone), payoff impact. A 10 means the reader felt genuine emotion shift.

### Coherence (key: "coherence")
Timeline clarity, cause-effect integrity, continuity of details, no dropped threads. A 10 means zero logic breaks or continuity errors.

### Promise Delivery (key: "promise_delivery")
Genre mechanics satisfied, premise alignment, core conflict progressed or resolved meaningfully. A 10 means the text delivers exactly what it promised and then some.

### Causal Inevitability (key: "causal_inevitability")
Counterfactual necessity of major turns, density of causal chains, absence of arbitrary reversals or deus ex machina, payoff earnedness. A 10 means outcomes feel both surprising and inevitable in retrospect.

## Evidence Rules
- Every dimension score MUST include 1-3 specific citations with location and a short quote
- Citations must be verifiable — quote actual text
- Justifications must reference the evidence, not restate the score

## Engagement Timeline
Segment the text into 4-8 windows. For each, give a 1-10 engagement score and tag it.
Valid tags: {', '.join(ENGAGEMENT_TAGS)}

## Top Issues
List the 3-5 most significant problems. Each must have a diagnosis tag.
Valid tags: {', '.join(DIAGNOSIS_TAGS)}

## Output Format
Return ONLY valid JSON:
{{
  "dimensions": {{
    "momentum": {{ "score": N, "justification": "...", "evidence": [{{ "quote": "..." }}] }}
  }},
  "engagement_timeline": [ {{ "window": N, "score": N, "tag": "...", "note": "..." }} ],
  "top_issues": [ {{ "tag": "...", "severity": "low|medium|high" }} ],
  "top_strengths": [ {{ "dimension": "...", "note": "..." }} ],
  "summary": "3-sentence executive summary.",
  "aftertaste": "One sentence: what lingers after the last page."
}}"""


def user_prompt(text: str, title: str, genre: str) -> str:
    return (
        f"## Context\nTitle: {title}\nGenre: {genre}\n\n## Text\n\n{text}\n\n"
        "Evaluate this text according to the rubric. Return ONLY valid JSON."
    )


def one_run(client: anthropic.Anthropic, text: str, title: str, genre: str) -> dict:
    with client.messages.stream(
        model=JUDGE_MODEL,
        max_tokens=8192,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt(text, title, genre)}],
    ) as stream:
        raw = "".join(stream.text_stream)
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise ValueError(f"judge returned no JSON: {raw[:200]}")
    out = json.loads(m.group(0))
    dims = out.get("dimensions", {})
    for k in WEIGHTS:
        s = dims.get(k, {}).get("score")
        if not isinstance(s, (int, float)):
            raise ValueError(f"dimension {k} missing")
        dims[k]["score"] = max(1, min(10, round(s)))
    out["composite"] = round(sum(dims[k]["score"] * w for k, w in WEIGHTS.items()) * 10, 1)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--genre", default="fiction")
    ap.add_argument("--title", default="Untitled")
    args = ap.parse_args()

    text = Path(args.input).read_text()
    client = anthropic.Anthropic()
    runs = []
    for i in range(args.runs):
        r = one_run(client, text, args.title, args.genre)
        print(f"run {i + 1}/{args.runs}: composite {r['composite']}", file=sys.stderr)
        runs.append(r)

    composite = round(statistics.median(r["composite"] for r in runs), 1)
    med_dims = {
        k: statistics.median(r["dimensions"][k]["score"] for r in runs) for k in WEIGHTS
    }
    result = {
        "input": args.input,
        "judge_model": JUDGE_MODEL,
        "runs": args.runs,
        "weights": WEIGHTS,
        "composite_score": composite,
        "dimension_medians": med_dims,
        "per_run": runs,
    }
    out = Path(args.input).with_suffix(".score.json")
    out.write_text(json.dumps(result, indent=2))
    print(f"{args.input}: composite {composite} → {out}")


if __name__ == "__main__":
    main()
