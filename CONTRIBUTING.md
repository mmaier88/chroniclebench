# Contributing

## Adding a model to the board

Follow the standing procedure in `docs/PROTOCOL.md` §5 exactly: pinned slug + provider,
full protocol (both arms, both briefs, all replicates), pinned-instrument scoring, and
publish every manifest including failures. Open a PR containing your manifests, window
scores and manuscripts' SHA-256 hashes; partial cohorts are not accepted for the
headline board. If the pinned instrument version has moved since the cohort you are
comparing against, say so — cross-instrument comparisons must be labeled.

## Improving the reference instrument

PRs to `instrument/` are welcome where they improve fidelity to the documented
methodology (`docs/METHODOLOGY.md`). Changes that alter what the instrument measures
require a versioned instrument id and never rescore existing published results.

## What this repo does not accept

Chronicle's generation engine is proprietary and out of scope. PRs attempting to add
engine-side generation machinery will be closed.
