#!/usr/bin/env python3
"""ChronicleBench neutral entrant harness — sustained arm.

Runs one model against one brief under the frozen v1.1 generation protocol:
the commission template below, then a neutral CONTINUE after every stop, until the
manuscript reaches the 85,000-word sustain target, the model stalls (three
consecutive continues under 400 words), or the hard word cap. Per-call word offsets
are recorded so every voluntary stop survives into analysis.

  python sustained_run.py --model anthropic/claude-sonnet-4.6 --brief ../data/briefs/B2.txt \
      [--genre "science fiction"] [--out out/] [--max-calls 25]

Requires OPENROUTER_API_KEY. The harness is deliberately minimal — it measures the
model, not prompt engineering. Do not modify the template or continuation message if
you intend to compare against published board results (their SHA-256 hashes are
recorded in every official manifest).
"""
import argparse, hashlib, json, os, time
from pathlib import Path

import requests

TEMPLATE = """Write a complete {genre} novel for adult readers, 80,000 to 90,000 words, based on this brief:

{brief}

Requirements:
- A complete story with a genuine, earned ending.
- Output only the manuscript prose (chapter breaks are allowed).
- Do not discuss the task. No outlines, notes, summaries, or commentary of any kind."""

CONTINUE_MSG = "Continue the manuscript exactly where you stopped. Do not summarize, restart, revise, or comment."

SUSTAIN_TARGET = 85_000
HARD_WORD_CAP = 94_000  # below the 95K eligibility ceiling
STALL_WORDS = 400
STALL_STRIKES = 3


def words(t: str) -> int:
    return len(t.split())


def call(model: str, messages: list, max_tokens: int) -> dict:
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json={"model": model, "messages": messages, "max_tokens": max_tokens},
        timeout=2400,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--genre", default="fiction")
    ap.add_argument("--out", default="out")
    ap.add_argument("--max-calls", type=int, default=25)
    ap.add_argument("--max-tokens", type=int, default=32_768)
    args = ap.parse_args()

    brief = Path(args.brief).read_text().strip()
    prompt = TEMPLATE.format(genre=args.genre, brief=brief)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    stem = f"{args.model.split('/')[-1]}-{Path(args.brief).stem}-sustained"

    messages = [{"role": "user", "content": prompt}]
    manuscript = ""
    offsets = []
    stalls = 0
    stop_reason = "target_reached"

    for n in range(args.max_calls):
        t0 = time.time()
        resp = call(args.model, messages, args.max_tokens)
        choice = resp["choices"][0]
        text = choice["message"]["content"] or ""
        finish = choice.get("finish_reason", "?")
        manuscript += ("\n\n" if manuscript else "") + text
        w = words(manuscript)
        offsets.append({"call": n, "finish": finish, "added_words": words(text),
                        "words_after": w, "seconds": round(time.time() - t0, 1)})
        print(f"call {n}: {finish} +{words(text)}w → {w}w")

        if w >= HARD_WORD_CAP:
            stop_reason = "word_cap"
            break
        if w >= SUSTAIN_TARGET and finish != "length":
            break
        stalls = stalls + 1 if (finish != "length" and words(text) < STALL_WORDS) else 0
        if stalls >= STALL_STRIKES:
            stop_reason = "stalled"
            break
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content": CONTINUE_MSG})
    else:
        stop_reason = "max_continuations"

    w = words(manuscript)
    eligible = 80_000 <= w <= 95_000
    Path(args.out, f"{stem}.txt").write_text(manuscript)
    Path(args.out, f"{stem}.manifest.json").write_text(json.dumps({
        "model": args.model, "brief": Path(args.brief).stem,
        "template_sha256": hashlib.sha256(TEMPLATE.encode()).hexdigest()[:16],
        "continue_sha256": hashlib.sha256(CONTINUE_MSG.encode()).hexdigest()[:16],
        "word_count": w, "eligible_80_95k": eligible, "stop_reason": stop_reason,
        "manuscript_sha256": hashlib.sha256(manuscript.encode()).hexdigest(),
        "calls": offsets,
    }, indent=2))
    print(f"{stem}: {w} words · {stop_reason} · {'ELIGIBLE' if eligible else 'DNF'}")
    print("Next: cut windows (instrument/cut_windows.py) and score them (instrument/score.py).")


if __name__ == "__main__":
    main()
