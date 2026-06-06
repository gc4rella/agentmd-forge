<!--
TEMPLATE: web-app. Copy the fenced block to AGENTS.md and fill it in.
Replace <…>. Use EXACT commands you verified. Keep under ~150 lines. Delete non-behavioral lines.
A fully worked version of this archetype lives in ../EXAMPLE.md.
-->

```md
# AGENTS.md

<name> is a <web app description>: frontend in `<frontend dir>`, backend in `<backend dir>`.
See README.md for product context and architecture.

## Working style
- Make the smallest change that satisfies the request; don't refactor opportunistically.
- Preserve API contracts and component props; flag breaking changes before coding.
- Reuse shared components/utilities before creating new ones.

## Repository map
- `<frontend dir>/` — UI
- `<backend dir>/` — API/services
- `<shared dir>/` — shared components/utilities
- `<migrations dir>/` — DB migrations (do not hand-edit)

## Setup & commands
- Install: `<install cmd>`
- Dev: `<dev cmd>`   ·   Build: `<build cmd>`
- Lint: `<lint cmd>`   ·   Typecheck: `<typecheck cmd>`   ·   Test: `<test cmd>`

## Coding conventions
- <type/style rules, e.g. TS strict, no `any`>
- <data-access rule, e.g. fetch only via the shared client>
- New endpoints need a validation schema and a test.

## Safety & constraints
- NEVER commit `.env*`, secrets, or real user data (incl. fixtures/screenshots).
- Get approval before touching auth, billing, `<migrations dir>/`, or deployment.
- Do not hand-edit generated files in `<generated dir>/`.

## Verification (definition of done)
All must pass: `<lint cmd>`, `<typecheck cmd>`, `<test cmd>`.
If UI behavior changed, state how you verified it. "Done" = covered by a test; docs updated if the
public API changed.

## Known failure modes
- Changing an API response shape without updating consumers.
- Duplicating UI primitives instead of reusing shared ones.
- Skipping typecheck after editing shared types.
```
