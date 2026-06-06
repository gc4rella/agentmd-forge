# agentmdforge

Portable skills for coding agents. Each skill is a plain `SKILL.md` folder that works across any
tool supporting the open [Agent Skills](https://agents.md) format — Claude Code, OpenAI Codex, and
others.

## Skills

### `writing-agents-md`

Forges best-in-class **`AGENTS.md`** files — the cross-tool "README for agents." It works in two
modes: scaffold one for a brand-new project (interview), or derive one from an existing repo
(trust-tier codebase scan). It encodes the *writing craft* (right altitude, exact commands, negative
rules, hard-gate verification) distilled from Anthropic's context-engineering guidance, OpenAI's
Codex docs, and strong real-world files — not just a list of sections. Ships an optional validator.

```
skills/writing-agents-md/
  SKILL.md                  # the skill (tight core)
  reference.md              # section catalog, trust-tier + detection tables, adapter matrix, monorepo
  frontmatter-schema.md     # optional machine-readable frontmatter (default OFF)
  EXAMPLE.md                # one fully worked example
  templates/                # cli-tool · web-app · library · service · research-prototype · monorepo-root
  scripts/validate_agents_md.py
```

## Install

Skills are discovered by folder. Symlink (so updates here propagate) or copy each skill into your
agent's skills directory.

**Claude Code** (`~/.claude/skills/`):
```bash
ln -s "$PWD/skills/writing-agents-md" ~/.claude/skills/writing-agents-md
```
Invoke with `/writing-agents-md`, or just describe the task — it triggers on its description.

**OpenAI Codex** (`~/.agents/skills/`, also scanned per-repo at `.agents/skills/`):
```bash
ln -s "$PWD/skills/writing-agents-md" ~/.agents/skills/writing-agents-md
```
Invoke with `$writing-agents-md` or via `/skills`.

Any other SKILL.md-aware agent can point at the same folder.

## Validator (optional)

```bash
python skills/writing-agents-md/scripts/validate_agents_md.py AGENTS.md --repo . --json
```
Checks line/byte budget, required gate sections, secret leaks, and (with `--repo`) that the commands
and paths it references actually exist. Stdlib-only Python 3.8+; CI-friendly (non-zero exit on
`--fail-on` codes).
