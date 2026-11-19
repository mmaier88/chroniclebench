#!/usr/bin/env python3
"""ChronicleBench reference scorer — the 8-dimension LLM rubric layer.

Scores one text window (or a whole manuscript) with the documented ChronicleBench
rubric: 8 dimensions, 1-10 each with mandatory evidence citations, judged by Claude
Sonnet at temperature 0, N independent runs (default 3), median composite.

  python score.py window.txt [--runs 3] [--genre "science fiction"] [--title "Untitled"] [--rubric v2.1|v2.2]

Output: <window>.score.json next to the input, with per-run and median results.

This is a faithful, self-contained re-implementation of the rubric layer of
Chronicle's pinned internal instrument (obr-v2.1-2026-03-08). The pinned instrument
additionally computes deterministic cross-check metrics (sentence-length variability,
lexical diversity, repetition analysis) that are provided to the judge as consistency
anchors and feed release-gating; the composite that ranks the board is the weighted
rubric mean implemented here. If you publish comparisons, state which implementation
produced your numbers.

Rubric versions. The default, v2.1, is the pinned instrument every published
score was produced with. --rubric v2.2 additionally gives the judge a
description for every score point (1-10) on every dimension (see
docs/SCORE_LEVELS.md). v2.2 scores are not comparable with v2.1 scores.
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

SCORE_LEVELS = {  # rubric v2.2 — mirrors SCORE_LEVELS in Chronicle's OBR (rubric.ts)
    "momentum": {
        1: "No forward pull. No question, goal or tension is established; the text is static description, summary or exposition. A reader would stop within pages.",
        2: "A situation exists but is buried. Scenes start long before anything happens, and almost none leaves a question that carries into the next. A reader continues only out of obligation.",
        3: "Occasional hooks, but long stretches (several scenes or chapters) where nothing is in motion or at stake. Repeated sag that a typical reader would quit during.",
        4: "The story moves, but slowly. Scenes routinely enter early and leave late; exposition or recap stalls progress. At least one clear sag where interest drops.",
        5: "Steady but weak pull. A central question is kept alive, but scenes rarely end on a new one. A reader continues without urgency; one or two noticeable drags.",
        6: "Solid pacing. A clear hook early; most scenes enter near the action and end with something changed. Brief lulls, but no section a reader would skim.",
        7: "Reliably engaging. Every scene raises or turns a question, and transitions carry curiosity forward. Lulls are short and purposeful (breathers after peaks).",
        8: "Strong pull-through. The reader actively wants the next scene. Short-term and long-term questions are layered, and the middle does not sag.",
        9: "Compulsive. Scene turns and chapter endings consistently compel continuation. Pace alternates deliberately between speed and breath, and every slowdown builds pressure.",
        10: "Matches the best published page-turners in its genre: sustained curiosity from first line to last with no perceptible drag, and the pacing itself serves the story's meaning.",
    },
    "voice_craft": {
        1: "Prose is broken: grammatical errors, garbled or repeated passages, no discernible voice.",
        2: "Prose functions but is mechanical throughout: dense AI-isms and clichés (\"something shifted\", \"a testament to\"), uniform sentence shapes, emotions stated rather than shown almost everywhere.",
        3: "Formulaic constructions and stock phrasing on most pages. The voice is flat or wavers; telling dominates showing.",
        4: "Competent but generic. Clean sentences, but repeated patterns, tics or images are noticeable, stock phrasing recurs, and showing and telling are unevenly balanced.",
        5: "Serviceable and mostly clean. A voice is present but not distinctive; a reader would notice some AI-isms or repeated tics, and sentence rhythm is fairly uniform.",
        6: "Solid. A consistent voice suited to the genre, varied sentences, rare stock phrasing. Important moments are shown; no tic a reader would register.",
        7: "Confident. The voice has an identifiable personality held from start to finish. Word choice is precise, images feel observed rather than borrowed, and telling is used only by choice.",
        8: "Distinctive. A reader would recognise this voice from an unattributed page. Rhythm is controlled for effect, images are fresh and specific, and there are no detectable AI fingerprints.",
        9: "Accomplished. Sentence-level craft is consistently striking without showing off; the voice adds meaning (irony, subtext, perspective) and holds without lapse across the whole length.",
        10: "Indistinguishable from a confident, accomplished human author at the top of the genre. The voice is singular and every sentence feels chosen.",
    },
    "characters": {
        1: "Characters are names only. No discernible desire, personality or conflict; they cannot be told apart.",
        2: "Characters are bare roles (the mentor, the villain) and one-note. Dialogue is interchangeable and exists only to deliver information.",
        3: "The protagonist has a stated goal but little else; the supporting cast is generic. Dialogue voices are indistinguishable, and characters sometimes act against established traits without reason.",
        4: "Main characters have desires and some traits, but these are told more than revealed. Dialogue voices blur, and there is little or no change.",
        5: "Recognisable types with clear goals and conflicts. The main pair have some distinction in dialogue; arcs are present but predictable or underdeveloped.",
        6: "Solid. Principal characters have clear wants, distinct personalities and believable behaviour. Dialogue is mostly distinguishable, and the protagonist changes credibly.",
        7: "Characters feel like people. Their desires collide and drive scenes, supporting characters have their own agendas, and most speakers have distinct dialogue voices.",
        8: "Memorable. You could identify most speakers from their dialogue alone. Relationships evolve, and growth is earned and shown through choices.",
        9: "A vivid ensemble. Even minor characters are specific. Characters surprise while staying consistent, and change is gradual, costly and fully dramatised.",
        10: "Characters as alive as the best in published fiction: unmistakable voices, conflicting desires that shape the whole story, and change that feels inevitable.",
    },
    "psychological_specificity": {
        1: "No inner life. Characters act without any visible thought or feeling.",
        2: "Inner life consists of labels (\"she felt sad\", \"he was angry\"). Motivation is absent or a single stated goal.",
        3: "Emotions are named rather than rendered, and every character thinks and reacts the same way. Motives are simple and stated.",
        4: "Some emotion is rendered, but generically (racing heart, tight chest). Motives are plausible but one-dimensional; no internal contradiction.",
        5: "Inner life is present and occasionally specific, but the characters' minds sound alike. Motives are explained rather than discovered; contradictions are hinted at but unexplored.",
        6: "Solid. Main characters have believable, somewhat layered motives, and emotion comes through behaviour and thought. At least one meaningful internal tension.",
        7: "Characters want contradictory things and act on mixed motives. Emotional texture is specific to the person and situation, and characters notice and reason in different ways.",
        8: "Each major character has a recognisably different mind: what they notice, avoid and rationalise. Self-deception and contradiction are dramatised, not explained.",
        9: "Inner lives are rich and surprising yet coherent. The reader understands characters better than they understand themselves, and minor characters show glimpses of depth.",
        10: "Inner lives so specific they could not belong to anyone else, matching the psychological depth of the best literary fiction.",
    },
    "emotional_arc": {
        1: "No tension and no stakes; nothing the reader could care about.",
        2: "Stakes are stated but not felt. The emotional register is flat and unchanging, and climactic moments land as summary.",
        3: "Tension rises occasionally but resets or dissipates. Stakes are unclear or arbitrary, and the book holds one emotional note throughout.",
        4: "Stakes are understandable but low or abstract. Escalation is uneven with plateaus, and payoffs are underpowered.",
        5: "Basic escalation with clear stakes, but monotone or predictable. Key moments land modestly.",
        6: "Solid. Stakes matter to the characters and the reader, tension builds towards a climax, there are at least two emotional registers, and the payoff satisfies.",
        7: "Tension escalates through real reversals. Emotional range includes relief, humour or tenderness amid strain, and the climax delivers a felt payoff.",
        8: "The reader is emotionally invested. Stakes become personal and irreversible, contrasts heighten the peaks, and the payoff is moving.",
        9: "A strong, controlled arc. Each escalation costs something, emotional shifts are earned and powerful, and the ending resonates.",
        10: "The reader experiences a genuine, lasting emotional shift equal to the best published novels in the genre.",
    },
    "coherence": {
        1: "Incoherent. Events contradict each other constantly; the reader cannot follow who, where or when.",
        2: "Frequent major contradictions (characters, facts, sequence) that break comprehension. Many threads are dropped.",
        3: "Several significant continuity errors or confusing jumps that a reader would stumble over. Important threads are dropped.",
        4: "Followable, but with noticeable continuity errors (changed details, impossible timing) or at least one significant dropped thread.",
        5: "Generally clear, with a few minor contradictions or loose ends an attentive reader would notice. No break in comprehension.",
        6: "Solid. Timeline and causality are clear, with at most minor slips that do not affect understanding. Major threads are resolved or deliberately left open.",
        7: "Clean. No noticeable continuity errors; details stay consistent and threads are tracked across the whole length.",
        8: "Tight. Details planted early stay consistent and pay off; a complex timeline remains clear.",
        9: "Essentially flawless across the length, with complex structure (multiple threads, time shifts) handled without confusion.",
        10: "Zero logic breaks or continuity errors; every detail and thread is accounted for.",
    },
    "promise_delivery": {
        1: "The text has nothing to do with its premise or genre; the core conflict is never addressed.",
        2: "The premise is largely abandoned or contradicted, and genre expectations are ignored.",
        3: "The premise is present but sidelined. Key genre mechanics are missing (for example, a mystery with no investigation), and the core conflict is unresolved or dismissed.",
        4: "The premise is delivered only in part. Some genre mechanics are present but thin; the resolution is perfunctory or drifts from the premise.",
        5: "Delivers the premise in a basic, expected way. Genre mechanics are present but routine; the core conflict is resolved without much impact.",
        6: "Solid. The premise and genre expectations are clearly met; the core conflict is addressed and meaningfully resolved (or, for an excerpt, credibly advanced).",
        7: "Delivers the premise fully with well-executed genre beats; the resolution satisfies the setup.",
        8: "Exceeds expectations. Genre pleasures are delivered with freshness, and promises made in the opening pay off in specific ways.",
        9: "Delivers the promise and deepens it; payoffs are both satisfying and surprising.",
        10: "Delivers exactly what was promised and then some. A reader of the genre would rank it among the genre's best.",
    },
    "causal_inevitability": {
        1: "Events are random; there is no cause and effect between major turns.",
        2: "Major turns are arbitrary or coincidental, and a deus ex machina resolves the central conflict.",
        3: "Several important turns depend on coincidence, unmotivated decisions or sudden reversals. The plot works only because the author says so.",
        4: "The causal chain is mostly present, but at least one key moment rests on a significant contrivance or convenient coincidence.",
        5: "Plausible cause and effect, but some turns feel interchangeable or under-prepared, and payoffs are partly unearned.",
        6: "Solid. Major turns follow from earlier events and character choices, with no deus ex machina; setups are mostly paid off.",
        7: "Turns are driven by characters' choices and their consequences. Removing a major event would break later events.",
        8: "A dense causal web. Payoffs are clearly earned by their setups, and outcomes surprise but make sense on reflection.",
        9: "Nearly every major outcome feels both surprising and inevitable. Setups go unnoticed on first reading and are obvious in hindsight.",
        10: "Every major outcome feels both surprising and inevitable in retrospect; the plot could not have happened otherwise.",
    },
}

SCORE_LEVELS_INSTRUCTION = "Each LLM-scored dimension below lists what every score from 1 to 10 means. Score each dimension at the level whose description best matches the evidence across the whole text."

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


def with_score_levels(prompt: str) -> str:
    """Rubric v2.2: insert the per-point descriptors under each dimension."""
    if "## Dimensions\n" not in prompt:
        raise ValueError("prompt has no '## Dimensions' section")
    out = prompt.replace("## Dimensions\n", f"{SCORE_LEVELS_INSTRUCTION}\n\n## Dimensions\n", 1)
    for dim, levels in SCORE_LEVELS.items():
        pat = re.compile(r"(### [^\n]+\(key: \"" + dim + r"\"\)\n[^\n]+(?:\nCross-check: [^\n]+)?)")
        if not pat.search(out):
            raise ValueError(f"dimension {dim} not found in prompt")
        block = "\n".join(f"- {n}: {levels[n]}" for n in range(1, 11))
        out = pat.sub(lambda m: f"{m.group(1)}\nScore levels:\n{block}", out, count=1)
    return out


SYSTEM_PROMPTS = {"v2.1": SYSTEM_PROMPT, "v2.2": with_score_levels(SYSTEM_PROMPT)}


def user_prompt(text: str, title: str, genre: str) -> str:
    return (
        f"## Context\nTitle: {title}\nGenre: {genre}\n\n## Text\n\n{text}\n\n"
        "Evaluate this text according to the rubric. Return ONLY valid JSON."
    )


def one_run(client: anthropic.Anthropic, text: str, title: str, genre: str, rubric: str = "v2.1") -> dict:
    with client.messages.stream(
        model=JUDGE_MODEL,
        max_tokens=8192,
        temperature=0,
        system=SYSTEM_PROMPTS[rubric],
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
    ap.add_argument("--rubric", choices=sorted(SYSTEM_PROMPTS), default="v2.1",
                    help="v2.1 = pinned published instrument (default); v2.2 = adds per-point score descriptors")
    args = ap.parse_args()

    text = Path(args.input).read_text()
    client = anthropic.Anthropic()
    runs = []
    for i in range(args.runs):
        r = one_run(client, text, args.title, args.genre, args.rubric)
        print(f"run {i + 1}/{args.runs}: composite {r['composite']}", file=sys.stderr)
        runs.append(r)

    composite = round(statistics.median(r["composite"] for r in runs), 1)
    med_dims = {
        k: statistics.median(r["dimensions"][k]["score"] for r in runs) for k in WEIGHTS
    }
    result = {
        "input": args.input,
        "judge_model": JUDGE_MODEL,
        "rubric": args.rubric,
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
