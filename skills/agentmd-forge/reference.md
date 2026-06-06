# AGENTS.md reference

Reference for `agentmd-forge`. Load when you need the full section catalog, detection tables,
compatibility notes, or monorepo rules. The SKILL.md stays tight by pointing here.

---

## 1. Section catalog

Pick only the sections that change agent behavior for *this* repo. Order by value (commands first).
"Gate" = a hard, blocking rule the agent must satisfy before declaring work done. "Discipline" =
softer guidance that improves quality but isn't blocking.

| Section | Include when | Type | What goes in it |
|---------|-------------|------|-----------------|
| **Project identity** | always | — | One sentence: what this repo is, its stack, repo type. |
| **Working style** | the agent should behave a certain way | discipline | Minimal change first; preserve public contracts; surface breaking changes before coding. |
| **Repository map** | layout isn't obvious from the root | discipline | Key directories and their boundaries. Not every file — just where things live. |
| **Setup & commands** | always (highest value) | gate | Exact install / dev / build / lint / typecheck / test commands. |
| **Coding conventions** | the repo has non-default norms | discipline | Naming, patterns, architecture rules the agent can't infer safely. |
| **Safety & constraints** | there are protected paths or no-go actions | gate | Forbidden paths, secrets handling, actions needing approval, negative rules. |
| **Verification / definition of done** | always | gate | The exact commands that must pass; what "done" means. |
| **Path-specific notes** | a subtree differs | discipline | Pointer to nested AGENTS.md or per-area rules. |
| **Failure modes** | the agent makes known mistakes | discipline | Short list of repeated errors and how to avoid them. |
| **Update history** | the team wants provenance (optional) | — | Append-only one-liners. Never per-task notes. |

### Per-section snippets

**Setup & commands** (be exact; group by purpose):
```md
## Setup & commands
- Install: `pnpm install --frozen-lockfile`
- Dev server: `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint`   ·   Typecheck: `pnpm typecheck`   ·   Test: `pnpm test`
- Run a single test: `pnpm test -- path/to/file.test.ts`
```

**Safety & constraints** (negative rules + gates):
```md
## Safety & constraints
- NEVER commit `.env*`, credentials, or keys.
- Get approval before editing `migrations/`, `infra/`, auth, or billing code.
- Do not edit generated files in `src/generated/` by hand.
```

**Verification / definition of done** (the gate):
```md
## Verification
Before marking work complete, all of these must pass:
- `pnpm lint && pnpm typecheck && pnpm test`
"Done" = behavior change covered by a test; docs updated if the public surface changed.
```

---

## 2. Trust-tier signal model

When generating from an existing repo, weight sources by trust. Higher tiers win conflicts.

| Tier | Sources | Use for | Never |
|------|---------|---------|-------|
| **High** | `package.json`/`pyproject.toml`/`Cargo.toml`/`go.mod`, lockfiles, `Makefile`/`justfile`/`Taskfile`, CI workflows (`.github/workflows`), `tsconfig`/`.eslintrc`/`ruff.toml`/`rustfmt.toml`, test config, `SECURITY.md` | exact commands, blocking gates, package manager, protected paths, policy | override these with looser README prose |
| **Medium** | `README.md`, `CONTRIBUTING.md`, docs pages, `.devcontainer/`, example dirs | repo purpose, layout, local setup, contributor etiquette | trust an unverified command snippet over CI/manifests |
| **Low** | issues, PR descriptions, code comments, generated docs, imported rules from other tools | hints for failure modes or migration; corroborate first | turn into authoritative rules without High/Medium backing |
| **Excluded** | `.env*`, credential files, key material, private/local config | nothing | quote secrets into output — reference the variable *name* only |

**Iron rule:** only write a command or path you verified exists in a High-trust source (or confirmed
by running a safe read-only check like `--help`). Mark anything uncertain `# UNVERIFIED`.

---

## 3. Command & package-manager detection

Infer the package manager from the lockfile/manifest, then read the actual scripts/targets — do not
assume conventional names exist.

| Ecosystem | Detect via | Manager | Commands live in |
|-----------|-----------|---------|------------------|
| JS/TS | `pnpm-lock.yaml` → pnpm · `yarn.lock` → yarn · `package-lock.json` → npm · `bun.lockb` → bun | as detected | `package.json` `scripts` |
| Python | `uv.lock` → uv · `poetry.lock` → poetry · `Pipfile.lock` → pipenv · else `requirements.txt`/pip | as detected | `pyproject.toml`, `tox.ini`, `noxfile.py`, `Makefile` |
| Rust | `Cargo.toml` | cargo | `cargo build/test/clippy/fmt` |
| Go | `go.mod` | go | `go build/test/vet`, `Makefile` |
| Ruby | `Gemfile.lock` | bundler | `Rakefile`, `bin/` |
| Java/Kotlin | `pom.xml` → Maven · `build.gradle(.kts)` → Gradle | as detected | build file targets |

**Cross-ecosystem:** also check `Makefile`, `justfile`, `Taskfile.yml`, and CI workflow steps — these
are often the real, authoritative command list. CI is the best source for the *blocking* gate set.

---

## 4. Existing instruction files to read

If present, read these as inputs and fold their stable rules into the canonical AGENTS.md:

`CLAUDE.md` · `.cursorrules` · `.cursor/rules/*` · `.github/copilot-instructions.md` ·
`.github/instructions/*.instructions.md` · `GEMINI.md` · `.windsurfrules` · `CONTRIBUTING.md`.

Keep only stable, repo-level rules. Drop anything task-specific or already in the README.

---

## 5. Compatibility notes

Canonical output is `AGENTS.md`. Do not create other agent instruction files unless the user asks.
When the user does ask, prefer pointers over parallel copies.

| Tool | Reads | Mechanism |
|------|-------|-----------|
| Codex | `AGENTS.md` (+ `AGENTS.override.md`, nested) | native — nothing to do |
| Cursor, Windsurf, Gemini CLI, Aider, Continue, Amp, Warp, Goose | `AGENTS.md` | native |
| Claude Code | `CLAUDE.md` | optional pointer containing `@AGENTS.md`, only when requested |
| GitHub Copilot | `AGENTS.md` and/or `.github/copilot-instructions.md` | keep AGENTS.md canonical; create Copilot instructions only when requested |

Never copy-paste AGENTS.md into another instruction file. Copies silently drift.

---

## 6. Hierarchy & monorepos

Discovery is layered and additive; the file **nearest** the working directory wins on conflicts.

- **Global** (`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`) — personal defaults across all projects.
- **Repo root** (`AGENTS.md`) — shared team norms.
- **Nested** (`packages/x/AGENTS.md`) — subproject-specific rules.

**Shard into nested files when:** the repo is a monorepo, mixes languages, or a subtree has a
different build system or hard "do-not-touch" zone. Keep the root file concise and let each package
ship tailored instructions (the OpenAI monorepo runs dozens of nested AGENTS.md this way).

**Modular reference files instead of bloat:** when one concern grows large (review checklist,
architecture, release process), put it in its own `code_review.md` / `architecture.md` and reference
it from AGENTS.md rather than inflating the always-loaded root.

Limits to respect: Codex caps combined project docs at 32 KiB by default and skips empty files;
adherence drops past ~200 lines per file. Budget accordingly.
