# Worked example

A realistic, tight AGENTS.md for a TypeScript/pnpm web app. It shows the principles in action:
exact commands, a clear repo map, negative rules, a hard-gate definition of done, and nothing the
README already covers. ~70 lines. This is the bar to aim for, not a section checklist to fill.

Everything between the rulers is the file you'd write as `AGENTS.md`.

---

```md
# AGENTS.md

Acme Web is a customer dashboard: a React frontend (`apps/web`) backed by a Node API (`apps/api`),
in a pnpm monorepo. See README.md for product context and architecture diagrams.

## Working style
- Make the smallest change that satisfies the request; don't refactor opportunistically.
- Preserve API contracts and component props. If a change is breaking, say so before writing code.
- Reuse components from `packages/ui` before creating new ones.

## Repository map
- `apps/web` — React UI (Vite, TanStack Router)
- `apps/api` — Node API (Fastify, Drizzle ORM)
- `packages/ui` — shared components
- `packages/lib` — shared utilities
- `migrations/` — DB migrations (generated; do not hand-edit)

## Setup & commands
- Install: `pnpm install --frozen-lockfile`
- Dev (all apps): `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint`   ·   Typecheck: `pnpm typecheck`   ·   Test: `pnpm test`
- One test file: `pnpm test -- apps/web/src/foo.test.tsx`

## Coding conventions
- TypeScript strict mode; no `any` — use `unknown` and narrow.
- Data fetching goes through `packages/lib/api-client`; never call `fetch` directly in components.
- New API routes need a Zod schema and a test.

## Safety & constraints
- NEVER commit `.env*`, secrets, or real customer data (including in test fixtures or screenshots).
- Get human approval before touching `apps/api/src/auth`, `apps/api/src/billing`, or `migrations/`.
- Generate migrations with `pnpm db:generate`; do not write SQL in `migrations/` by hand.

## Verification (definition of done)
Before marking work complete, ALL must pass:
- `pnpm lint && pnpm typecheck && pnpm test`
- If you changed UI behavior, state how you verified it (which screen/flow you exercised).
"Done" means: change is covered by a test, gates pass, and docs are updated if the public API changed.

## Known failure modes
- Changing an API response shape without updating its consumers in `apps/web`.
- Adding a duplicate button/input instead of reusing `packages/ui`.
- Skipping `pnpm typecheck` after editing shared types.
```

---

## Why this works

- **Commands are exact and runnable** — no "run the tests."
- **Negative rules are explicit** — the `NEVER`/approval lines are the highest-leverage content.
- **Hard gate is unambiguous** — one command line defines "done."
- **No README duplication** — it links out for product/architecture context.
- **No bloat** — no generic "write clean, readable code" filler; every line is checkable.
- **Stable only** — no task notes, no changelog, nothing that rots.
