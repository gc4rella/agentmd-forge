<!--
TEMPLATE: backend service / API. Copy the fenced block to AGENTS.md and fill it in.
Replace <…>. Use EXACT commands you verified. Keep under ~150 lines. Delete non-behavioral lines.
Emphasis for a service: API/contract stability, migrations, observability, secrets, deploy safety.
-->

```md
# AGENTS.md

<name> is a <service description> exposing <API style, e.g. REST/gRPC>. See README.md for setup
and architecture.

## Working style
- Preserve API contracts and DB schema compatibility; flag breaking changes before coding.
- Every new endpoint: input validation, error handling, a test, and a log/metric where relevant.
- Keep changes scoped; avoid cross-cutting refactors without a task.

## Repository map
- `<src dir>/` — service code (entrypoint: `<entrypoint>`)
- `<migrations dir>/` — DB migrations (generated; do not hand-edit)
- `<tests dir>/` — unit + integration tests
- `<infra dir>/` — deployment/infra config

## Setup & commands
- Install: `<install cmd>`   ·   Run locally: `<run cmd>`
- Lint: `<lint cmd>`   ·   Typecheck: `<typecheck cmd>`   ·   Test: `<test cmd>`
- Generate a migration: `<migration cmd>`

## Coding conventions
- <style/naming rules>
- Validate all external input; never trust request bodies or query params.

## Safety & constraints
- NEVER commit `.env*`, secrets, connection strings, or keys — reference variable names only.
- Get approval before editing auth, billing, `<migrations dir>/`, or `<infra dir>/`.
- Do not run destructive commands (drops, prod migrations, deploys) without explicit approval.

## Verification (definition of done)
All must pass: `<lint cmd>`, `<typecheck cmd>`, `<test cmd>`.
"Done" = endpoint covered by an integration test, migrations reversible, no secret in the diff.

## Known failure modes
- Backward-incompatible schema/API change without a migration path.
- Logging secrets or PII.
- Skipping integration tests for new endpoints.
```
