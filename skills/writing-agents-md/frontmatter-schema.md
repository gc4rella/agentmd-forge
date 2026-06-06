# Optional machine-readable frontmatter

**Default: OFF.** The best AGENTS.md files (OpenAI's, Apache's) are clean prose with no frontmatter,
and there is **no ratified cross-vendor schema** today. Only add this when a team explicitly wants
CI tooling to read structured fields. Frontmatter spends line budget — keep it lean.

When enabled, prepend a YAML block to `AGENTS.md` and optionally mirror it as `agents.manifest.json`
for CI. The **Markdown body remains authoritative**; frontmatter is a convenience for tooling.

## Fields (lean set)

| Field | Required | Notes |
|-------|----------|-------|
| `schema_version` | yes | `"1.0"` |
| `name` | yes | repo name |
| `purpose` | yes | one sentence |
| `project_type` | yes | `cli-tool` \| `web-app` \| `library` \| `service` \| `research-prototype` \| `monorepo` |
| `tools.package_manager` | yes | e.g. `pnpm` |
| `tools.commands` | yes | map of install/dev/build/lint/typecheck/test → exact command |
| `safety.forbidden_paths` | recommended | globs that must not be edited/committed |
| `safety.approval_required_for` | recommended | actions needing human approval |
| `verification.required_commands` | yes | the blocking gate set; must be non-empty |
| `source_of_truth` | yes | files the content was derived from |
| `update_history` | yes | append-only `{date, actor, summary}` entries |

Deliberately omitted (speculative, not worth the budget): `context_budget`, `evaluation_metrics`,
`persona`, `system_prompt_policy`. Add them only if a concrete tool consumes them.

## Example

```yaml
---
schema_version: "1.0"
name: "acme-web"
purpose: "Browser dashboard with an API backend."
project_type: "web-app"
tools:
  package_manager: "pnpm"
  commands:
    install: "pnpm install --frozen-lockfile"
    dev: "pnpm dev"
    build: "pnpm build"
    lint: "pnpm lint"
    typecheck: "pnpm typecheck"
    test: "pnpm test"
safety:
  forbidden_paths: [".env*", "src/generated/**"]
  approval_required_for: ["auth", "billing", "migrations", "deployment"]
verification:
  required_commands: ["pnpm lint", "pnpm typecheck", "pnpm test"]
source_of_truth: ["package.json", ".github/workflows/ci.yml", "README.md"]
update_history:
  - { date: "2026-06-06", actor: "writing-agents-md", summary: "Initial generation" }
---
```

The JSON sidecar (`agents.manifest.json`) is the same structure in JSON. `validate_agents_md.py`
validates this block when it is present and ignores its absence otherwise.
