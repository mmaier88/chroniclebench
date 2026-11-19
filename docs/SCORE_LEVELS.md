# OBR score levels (rubric v2.2)

Added November 2026. The OBR scale used to be anchored only at the band level
(1–3 a clear problem, 4–5 a noticeable weakness, 6–7 solid, 8–9 notably good,
10 would hold up against a published novel) plus one "a 10 means…" sentence per
dimension. Rubric v2.2 gives the judge **a description for every point from 1
to 10 on every dimension**. The bands still hold; the per-point descriptions sit
inside them.

## Status and comparability

- **Every published score on this board was produced with v2.1**
  (`obr-v2.1-2026-03-08`). The cohort instrument is frozen and is not re-scored.
- `instrument/score.py` defaults to v2.1, so published numbers reproduce.
  `--rubric v2.2` adds the descriptions below; the output records which rubric
  was used.
- **v2.2 scores are not comparable with v2.1 scores.** The descriptions may
  move scores in either direction, by different amounts per dimension. Any
  future cohort adopting v2.2 would be announced as a new instrument version
  under the protocol's amendment discipline, with both versions run on a common
  set to report the shift.
- The text below is identical to the levels in Chronicle's production OBR.

## How the judge receives them

Under each dimension's definition the prompt adds `Score levels:` followed by
the ten descriptions, and before the dimensions it adds: *"Each LLM-scored
dimension below lists what every score from 1 to 10 means. Score each
dimension at the level whose description best matches the evidence across the
whole text."* The evidence rules (1–3 verifiable quotes per score) are
unchanged.

## Next steps (not done)

The descriptions say what each point means. They do not yet show that the
judge applies them the way human readers would. Two steps would close that gap:

1. **Reference passages per level.** Short published-fiction excerpts at known
   levels for each dimension, given to the judge as worked examples.
2. **Human-rated calibration set.** Texts scored by human readers on the same
   dimensions, so judge scores can be checked against reader judgement
   dimension by dimension, and descriptions revised where the two disagree.

Contributions toward either are welcome (see `CONTRIBUTING.md`).

## The levels

### Momentum (`momentum`)

Hook strength, scene entry speed, pull-through across acts, absence of mid-book sag. A 10 means sustained curiosity with no perceptible drag.

| Score | What it means |
|---|---|
| 10 | Matches the best published page-turners in its genre: sustained curiosity from first line to last with no perceptible drag, and the pacing itself serves the story's meaning. |
| 9 | Compulsive. Scene turns and chapter endings consistently compel continuation. Pace alternates deliberately between speed and breath, and every slowdown builds pressure. |
| 8 | Strong pull-through. The reader actively wants the next scene. Short-term and long-term questions are layered, and the middle does not sag. |
| 7 | Reliably engaging. Every scene raises or turns a question, and transitions carry curiosity forward. Lulls are short and purposeful (breathers after peaks). |
| 6 | Solid pacing. A clear hook early; most scenes enter near the action and end with something changed. Brief lulls, but no section a reader would skim. |
| 5 | Steady but weak pull. A central question is kept alive, but scenes rarely end on a new one. A reader continues without urgency; one or two noticeable drags. |
| 4 | The story moves, but slowly. Scenes routinely enter early and leave late; exposition or recap stalls progress. At least one clear sag where interest drops. |
| 3 | Occasional hooks, but long stretches (several scenes or chapters) where nothing is in motion or at stake. Repeated sag that a typical reader would quit during. |
| 2 | A situation exists but is buried. Scenes start long before anything happens, and almost none leaves a question that carries into the next. A reader continues only out of obligation. |
| 1 | No forward pull. No question, goal or tension is established; the text is static description, summary or exposition. A reader would stop within pages. |

### Voice & Craft (`voice_craft`)

Voice consistency from first page to last, absence of AI-isms, sentence variety, show-vs-tell balance. A 10 means indistinguishable from a confident human author.

| Score | What it means |
|---|---|
| 10 | Indistinguishable from a confident, accomplished human author at the top of the genre. The voice is singular and every sentence feels chosen. |
| 9 | Accomplished. Sentence-level craft is consistently striking without showing off; the voice adds meaning (irony, subtext, perspective) and holds without lapse across the whole length. |
| 8 | Distinctive. A reader would recognise this voice from an unattributed page. Rhythm is controlled for effect, images are fresh and specific, and there are no detectable AI fingerprints. |
| 7 | Confident. The voice has an identifiable personality held from start to finish. Word choice is precise, images feel observed rather than borrowed, and telling is used only by choice. |
| 6 | Solid. A consistent voice suited to the genre, varied sentences, rare stock phrasing. Important moments are shown; no tic a reader would register. |
| 5 | Serviceable and mostly clean. A voice is present but not distinctive; a reader would notice some AI-isms or repeated tics, and sentence rhythm is fairly uniform. |
| 4 | Competent but generic. Clean sentences, but repeated patterns, tics or images are noticeable, stock phrasing recurs, and showing and telling are unevenly balanced. |
| 3 | Formulaic constructions and stock phrasing on most pages. The voice is flat or wavers; telling dominates showing. |
| 2 | Prose functions but is mechanical throughout: dense AI-isms and clichés ("something shifted", "a testament to"), uniform sentence shapes, emotions stated rather than shown almost everywhere. |
| 1 | Prose is broken: grammatical errors, garbled or repeated passages, no discernible voice. |

### Characters (`characters`)

Distinctiveness of dialogue voices, clear desires and conflicts, character growth or change. A 10 means you could identify characters by dialogue alone.

| Score | What it means |
|---|---|
| 10 | Characters as alive as the best in published fiction: unmistakable voices, conflicting desires that shape the whole story, and change that feels inevitable. |
| 9 | A vivid ensemble. Even minor characters are specific. Characters surprise while staying consistent, and change is gradual, costly and fully dramatised. |
| 8 | Memorable. You could identify most speakers from their dialogue alone. Relationships evolve, and growth is earned and shown through choices. |
| 7 | Characters feel like people. Their desires collide and drive scenes, supporting characters have their own agendas, and most speakers have distinct dialogue voices. |
| 6 | Solid. Principal characters have clear wants, distinct personalities and believable behaviour. Dialogue is mostly distinguishable, and the protagonist changes credibly. |
| 5 | Recognisable types with clear goals and conflicts. The main pair have some distinction in dialogue; arcs are present but predictable or underdeveloped. |
| 4 | Main characters have desires and some traits, but these are told more than revealed. Dialogue voices blur, and there is little or no change. |
| 3 | The protagonist has a stated goal but little else; the supporting cast is generic. Dialogue voices are indistinguishable, and characters sometimes act against established traits without reason. |
| 2 | Characters are bare roles (the mentor, the villain) and one-note. Dialogue is interchangeable and exists only to deliver information. |
| 1 | Characters are names only. No discernible desire, personality or conflict; they cannot be told apart. |

### Psychological Specificity (`psychological_specificity`)

Internal contradictions within characters, motivational complexity beyond stated goals, emotional texture that goes beyond labeling feelings, cognitive model distinctness per character. A 10 means characters have rich, specific inner lives that could not belong to anyone else.

| Score | What it means |
|---|---|
| 10 | Inner lives so specific they could not belong to anyone else, matching the psychological depth of the best literary fiction. |
| 9 | Inner lives are rich and surprising yet coherent. The reader understands characters better than they understand themselves, and minor characters show glimpses of depth. |
| 8 | Each major character has a recognisably different mind: what they notice, avoid and rationalise. Self-deception and contradiction are dramatised, not explained. |
| 7 | Characters want contradictory things and act on mixed motives. Emotional texture is specific to the person and situation, and characters notice and reason in different ways. |
| 6 | Solid. Main characters have believable, somewhat layered motives, and emotion comes through behaviour and thought. At least one meaningful internal tension. |
| 5 | Inner life is present and occasionally specific, but the characters' minds sound alike. Motives are explained rather than discovered; contradictions are hinted at but unexplored. |
| 4 | Some emotion is rendered, but generically (racing heart, tight chest). Motives are plausible but one-dimensional; no internal contradiction. |
| 3 | Emotions are named rather than rendered, and every character thinks and reacts the same way. Motives are simple and stated. |
| 2 | Inner life consists of labels ("she felt sad", "he was angry"). Motivation is absent or a single stated goal. |
| 1 | No inner life. Characters act without any visible thought or feeling. |

### Emotional Arc (`emotional_arc`)

Tension escalation, stakes that matter, emotional range (not monotone), payoff impact. A 10 means the reader felt genuine emotion shift across the book.

| Score | What it means |
|---|---|
| 10 | The reader experiences a genuine, lasting emotional shift equal to the best published novels in the genre. |
| 9 | A strong, controlled arc. Each escalation costs something, emotional shifts are earned and powerful, and the ending resonates. |
| 8 | The reader is emotionally invested. Stakes become personal and irreversible, contrasts heighten the peaks, and the payoff is moving. |
| 7 | Tension escalates through real reversals. Emotional range includes relief, humour or tenderness amid strain, and the climax delivers a felt payoff. |
| 6 | Solid. Stakes matter to the characters and the reader, tension builds towards a climax, there are at least two emotional registers, and the payoff satisfies. |
| 5 | Basic escalation with clear stakes, but monotone or predictable. Key moments land modestly. |
| 4 | Stakes are understandable but low or abstract. Escalation is uneven with plateaus, and payoffs are underpowered. |
| 3 | Tension rises occasionally but resets or dissipates. Stakes are unclear or arbitrary, and the book holds one emotional note throughout. |
| 2 | Stakes are stated but not felt. The emotional register is flat and unchanging, and climactic moments land as summary. |
| 1 | No tension and no stakes; nothing the reader could care about. |

### Coherence (`coherence`)

Timeline clarity, cause-effect integrity, continuity of details, no dropped threads. A 10 means zero logic breaks or continuity errors.

| Score | What it means |
|---|---|
| 10 | Zero logic breaks or continuity errors; every detail and thread is accounted for. |
| 9 | Essentially flawless across the length, with complex structure (multiple threads, time shifts) handled without confusion. |
| 8 | Tight. Details planted early stay consistent and pay off; a complex timeline remains clear. |
| 7 | Clean. No noticeable continuity errors; details stay consistent and threads are tracked across the whole length. |
| 6 | Solid. Timeline and causality are clear, with at most minor slips that do not affect understanding. Major threads are resolved or deliberately left open. |
| 5 | Generally clear, with a few minor contradictions or loose ends an attentive reader would notice. No break in comprehension. |
| 4 | Followable, but with noticeable continuity errors (changed details, impossible timing) or at least one significant dropped thread. |
| 3 | Several significant continuity errors or confusing jumps that a reader would stumble over. Important threads are dropped. |
| 2 | Frequent major contradictions (characters, facts, sequence) that break comprehension. Many threads are dropped. |
| 1 | Incoherent. Events contradict each other constantly; the reader cannot follow who, where or when. |

### Promise Delivery (`promise_delivery`)

Genre mechanics satisfied, preview/blurb alignment, core conflict resolved meaningfully. A 10 means the book delivered exactly what was promised and then some.

| Score | What it means |
|---|---|
| 10 | Delivers exactly what was promised and then some. A reader of the genre would rank it among the genre's best. |
| 9 | Delivers the promise and deepens it; payoffs are both satisfying and surprising. |
| 8 | Exceeds expectations. Genre pleasures are delivered with freshness, and promises made in the opening pay off in specific ways. |
| 7 | Delivers the premise fully with well-executed genre beats; the resolution satisfies the setup. |
| 6 | Solid. The premise and genre expectations are clearly met; the core conflict is addressed and meaningfully resolved (or, for an excerpt, credibly advanced). |
| 5 | Delivers the premise in a basic, expected way. Genre mechanics are present but routine; the core conflict is resolved without much impact. |
| 4 | The premise is delivered only in part. Some genre mechanics are present but thin; the resolution is perfunctory or drifts from the premise. |
| 3 | The premise is present but sidelined. Key genre mechanics are missing (for example, a mystery with no investigation), and the core conflict is unresolved or dismissed. |
| 2 | The premise is largely abandoned or contradicted, and genre expectations are ignored. |
| 1 | The text has nothing to do with its premise or genre; the core conflict is never addressed. |

### Causal Inevitability (`causal_inevitability`)

Counterfactual necessity of major turns (would the plot still work if this event were removed?), density of causal chains, absence of arbitrary reversals or deus ex machina, payoff earnedness. A 10 means every major outcome feels both surprising and inevitable in retrospect.

| Score | What it means |
|---|---|
| 10 | Every major outcome feels both surprising and inevitable in retrospect; the plot could not have happened otherwise. |
| 9 | Nearly every major outcome feels both surprising and inevitable. Setups go unnoticed on first reading and are obvious in hindsight. |
| 8 | A dense causal web. Payoffs are clearly earned by their setups, and outcomes surprise but make sense on reflection. |
| 7 | Turns are driven by characters' choices and their consequences. Removing a major event would break later events. |
| 6 | Solid. Major turns follow from earlier events and character choices, with no deus ex machina; setups are mostly paid off. |
| 5 | Plausible cause and effect, but some turns feel interchangeable or under-prepared, and payoffs are partly unearned. |
| 4 | The causal chain is mostly present, but at least one key moment rests on a significant contrivance or convenient coincidence. |
| 3 | Several important turns depend on coincidence, unmotivated decisions or sudden reversals. The plot works only because the author says so. |
| 2 | Major turns are arbitrary or coincidental, and a deus ex machina resolves the central conflict. |
| 1 | Events are random; there is no cause and effect between major turns. |
