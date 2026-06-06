<!--
TEMPLATE: library/package. Copy the fenced block to AGENTS.md and fill it in.
Replace <…>. Use EXACT commands you verified. Keep under ~150 lines. Delete non-behavioral lines.
Emphasis for a library: public API stability, semver, docs/changelog discipline.
-->

```md
# AGENTS.md

<name> is a <language> library that <one-sentence purpose>. See README.md for the public API.

## Working style
- The public API is a contract. Do NOT change exported signatures without an explicit task to do so.
- Breaking changes require a semver major and a changelog entry — call them out before coding.
- Keep the dependency footprint minimal; justify any new runtime dependency.

## Repository map
- `<src dir>/` — library source (public exports in `<entry file>`)
- `<tests dir>/` — tests
- `<examples dir>/` — usage examples (must stay runnable)

## Setup & commands
- Install: `<install cmd>`
- Build: `<build cmd>`   ·   Lint: `<lint cmd>`   ·   Typecheck: `<typecheck cmd>`
- Test: `<test cmd>`   ·   One test: `<single-test cmd>`

## Coding conventions
- <style/naming rules>
- Public functions need doc comments and tests; cover error paths, not just happy paths.

## Safety & constraints
- Do not export internal/unstable APIs from `<entry file>`.
- Do not break backward compatibility on a minor/patch release.

## Verification (definition of done)
All must pass: `<build cmd>`, `<lint cmd>`, `<typecheck cmd>`, `<test cmd>`.
"Done" = public behavior tested, docs/changelog updated for any API change.

## Known failure modes
- Silently widening or changing a public signature.
- Adding a heavy dependency for a small helper.
- Leaving examples broken after an API change.
```
