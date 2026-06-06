<!--
TEMPLATE: research prototype / experiments. Copy the fenced block to AGENTS.md and fill it in.
Replace <…>. Use EXACT commands you verified. Keep under ~150 lines. Delete non-behavioral lines.
Emphasis for research: reproducibility, traceability, stated assumptions over polished abstractions.
-->

```md
# AGENTS.md

<name> is a research prototype for <purpose>. Reproducibility matters more than polish.
See README.md for the experiment overview.

## Working style
- Preserve experiment traceability; prefer local, well-scoped changes over broad refactors.
- When assumptions are unclear, state them explicitly in code/run notes rather than guessing.
- Do not silently change defaults, seeds, or metric definitions.

## Repository map
- `<src dir>/` — training/eval code
- `<configs dir>/` — experiment configs (prefer config changes over code edits)
- `<notebooks dir>/` — exploratory analysis (not the source of truth)
- `<data dir>/` — dataset staging/metadata   ·   `<outputs dir>/` — artefacts
- `<tests dir>/` — regression tests

## Setup & commands
- Environment: `<env setup cmd>`
- Train (help): `<train cmd --help>`   ·   Eval (help): `<eval cmd --help>`
- Test: `<test cmd>`

## Coding conventions
- <style rules>
- Log seed, dataset version, and key hyperparameters for any new experiment path.

## Safety & constraints
- Do not commit raw data, credentials, or large binary artefacts.
- Get approval before downloading new datasets or overwriting `<outputs dir>/`.
- Treat notebooks as exploratory unless explicitly promoted to a supported workflow.

## Verification (definition of done)
Must pass: `<test cmd>`.
If experiment behavior changed, document seed handling, config diff, and expected output artefacts.

## Known failure modes
- Breaking reproducibility by changing defaults silently.
- Editing a notebook without updating the equivalent source code.
- Overwriting output directories without warning.
```
