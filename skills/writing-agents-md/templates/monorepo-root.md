<!--
TEMPLATE: monorepo ROOT. Copy the fenced block to the repo-root AGENTS.md.
The root file stays SHORT: shared norms + a map of where the per-package rules live.
Put package-specific commands/conventions in nested AGENTS.md files (the nearest one wins).
Pick the matching archetype (web-app, service, library, cli-tool) for each package's own file.
-->

```md
# AGENTS.md

<name> is a <language(s)> monorepo managed with <tool, e.g. pnpm/turbo/nx/cargo workspaces>.
Each package has its own AGENTS.md with package-specific rules — the nearest file wins.

## Working style
- Work within one package per change where possible; flag cross-package/breaking changes first.
- Shared code lives in `<shared packages>`; reuse before adding new packages.

## Repository map (where the rules live)
- `<apps/* or packages/*>` — each subproject; see its local `AGENTS.md`
- `<shared dir>/` — shared libraries
- Root configs: `<root build/lint/CI config>`

## Setup & commands (workspace-wide)
- Install: `<install cmd>`
- Build all: `<build cmd>`   ·   Lint all: `<lint cmd>`   ·   Test all: `<test cmd>`
- Scope to one package: `<scoped cmd, e.g. pnpm --filter @acme/web test>`

## Conventions (shared)
- <repo-wide style/naming rules that apply everywhere>
- Package-specific conventions belong in that package's AGENTS.md, not here.

## Safety & constraints (shared)
- NEVER commit `.env*`, secrets, or keys anywhere in the workspace.
- Get approval before changing root build/CI config or release tooling.

## Verification (definition of done)
Workspace gate: `<lint cmd>`, `<test cmd>` (or the affected-package subset).
Each package may add stricter gates in its own AGENTS.md.
```
