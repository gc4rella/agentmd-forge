#!/usr/bin/env python3
"""Optional deterministic validator for AGENTS.md files.

This is a convenience, not a gate: the agent writing the file should already have verified its
commands and paths. The script catches regressions in CI and obvious mistakes (bloat, secret
leaks, missing gate sections, commands that don't exist).

Stdlib only (Python 3.8+). No third-party dependencies.

Usage:
    python validate_agents_md.py AGENTS.md
    python validate_agents_md.py AGENTS.md --repo . --json
    python validate_agents_md.py AGENTS.md --repo . --fail-on secret_leak,invalid_commands

Exit code is non-zero when any finding whose `code` is listed in --fail-on is present.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# --- check codes -----------------------------------------------------------------------------
LINE_BUDGET = "line_budget"
BYTE_BUDGET = "byte_budget"
MISSING_REQUIRED_SECTIONS = "missing_required_sections"
MISSING_RECOMMENDED_SECTIONS = "missing_recommended_sections"
SECRET_LEAK = "secret_leak"
INVALID_COMMANDS = "invalid_commands"
INVALID_PATHS = "invalid_paths"

DEFAULT_FAIL_ON = {MISSING_REQUIRED_SECTIONS, SECRET_LEAK, INVALID_COMMANDS}

# Required = the blocking gates a useful AGENTS.md must answer. Detected by heading keywords.
REQUIRED_SECTIONS = {
    "setup/commands": ["setup", "command", "build", "install", "run", "test"],
    "verification": ["verif", "definition of done", "done", "checklist", "before"],
}
RECOMMENDED_SECTIONS = {
    "safety/constraints": ["safety", "constraint", "guardrail", "do not", "don't", "never"],
    "repository map": ["repository map", "repo map", "project structure", "layout", "directories"],
}

# Secret patterns. Conservative but real — AGENTS.md should contain no secrets at all.
SECRET_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{36,}\b|\bgithub_pat_[0-9A-Za-z_]{22,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("OpenAI/Anthropic key", re.compile(r"\b(?:sk|sk-ant)-[0-9A-Za-z_\-]{20,}\b")),
    ("bearer token", re.compile(r"(?i)\bbearer\s+[0-9A-Za-z_\-\.]{16,}")),
]
# Generic `key = value` secret assignment, excluding obvious placeholders / env-var references.
SECRET_ASSIGN = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password|passwd|client[_-]?secret|access[_-]?token)\b"
    r"\s*[:=]\s*['\"]?([^\s'\"]{12,})"
)
PLACEHOLDER = re.compile(r"<|>|\$\{?[A-Za-z_]|x{4,}|your[_-]|example|placeholder|redacted|\*{3,}|\.\.\.|^[A-Z][A-Z0-9_]+$")

BACKTICK = re.compile(r"`([^`]+)`")
HEADING = re.compile(r"^#{1,6}\s+(.*\S)\s*$")
PM_RUN = re.compile(r"\b(npm|pnpm|yarn|bun)\s+(?:run\s+)?([A-Za-z0-9_:.-]+)")
MAKE_TARGET = re.compile(r"\bmake\s+([A-Za-z0-9_.-]+)")
JUST_RECIPE = re.compile(r"\bjust\s+([A-Za-z0-9_-]+)")

PM_BUILTINS = {
    "install", "i", "ci", "add", "remove", "rm", "up", "update", "upgrade", "dev", "build",
    "start", "test", "run", "exec", "dlx", "create", "lint", "format", "fmt", "typecheck",
    "why", "audit", "list", "ls", "link", "unlink", "publish", "pack", "init", "store",
    "prune", "outdated", "info", "x", "check",
}


class Finding:
    def __init__(self, code: str, severity: str, message: str, detail: str = "") -> None:
        self.code = code
        self.severity = severity  # "error" | "warning" | "info"
        self.message = message
        self.detail = detail

    def to_dict(self) -> Dict[str, str]:
        return {"code": self.code, "severity": self.severity, "message": self.message, "detail": self.detail}


def parse_headings(text: str) -> List[str]:
    return [m.group(1).lower() for line in text.splitlines() for m in [HEADING.match(line)] if m]


def check_budget(text: str, max_lines: int, max_bytes: int) -> List[Finding]:
    out: List[Finding] = []
    n_lines = len(text.splitlines())
    n_bytes = len(text.encode("utf-8"))
    if n_lines > max_lines:
        out.append(Finding(LINE_BUDGET, "warning",
                           f"{n_lines} lines exceeds target of {max_lines}",
                           "Cut to high-signal rules, or shard into nested/reference files."))
    if n_bytes > max_bytes:
        out.append(Finding(BYTE_BUDGET, "warning",
                           f"{n_bytes} bytes exceeds {max_bytes} (Codex default project-doc cap)",
                           "Trim or split; oversized docs get truncated."))
    return out


def check_sections(headings: List[str]) -> List[Finding]:
    out: List[Finding] = []
    joined = " | ".join(headings)
    for label, keywords in REQUIRED_SECTIONS.items():
        if not any(k in joined for k in keywords):
            out.append(Finding(MISSING_REQUIRED_SECTIONS, "error",
                               f"missing required section: {label}",
                               "A useful AGENTS.md must state how to build/test and what 'done' means."))
    for label, keywords in RECOMMENDED_SECTIONS.items():
        if not any(k in joined for k in keywords):
            out.append(Finding(MISSING_RECOMMENDED_SECTIONS, "warning",
                               f"missing recommended section: {label}"))
    return out


def check_secrets(text: str) -> List[Finding]:
    out: List[Finding] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for name, pat in SECRET_PATTERNS:
            if pat.search(line):
                out.append(Finding(SECRET_LEAK, "error", f"possible {name} on line {line_no}",
                                   line.strip()[:120]))
        m = SECRET_ASSIGN.search(line)
        if m and not PLACEHOLDER.search(m.group(2)):
            out.append(Finding(SECRET_LEAK, "error",
                               f"possible hardcoded {m.group(1)} on line {line_no}",
                               "Reference the variable name only; never paste a value."))
    return out


def _load_pkg_scripts(repo: Path) -> Optional[set]:
    pkg = repo / "package.json"
    if not pkg.is_file():
        return None
    try:
        return set(json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {}).keys())
    except (ValueError, OSError):
        return set()


def _load_targets(path: Path, pattern: re.Pattern) -> set:
    if not path.is_file():
        return set()
    try:
        return {m.group(1) for line in path.read_text(encoding="utf-8").splitlines()
                for m in [pattern.match(line)] if m}
    except OSError:
        return set()


def check_commands(text: str, repo: Path) -> List[Finding]:
    out: List[Finding] = []
    scripts = _load_pkg_scripts(repo)
    make_targets = _load_targets(repo / "Makefile", re.compile(r"^([A-Za-z0-9_.-]+):"))
    just_recipes = _load_targets(repo / "justfile", re.compile(r"^([a-z0-9_-]+):"))
    if just_recipes == set():
        just_recipes = _load_targets(repo / ".justfile", re.compile(r"^([a-z0-9_-]+):"))

    for token in BACKTICK.findall(text):
        if "<" in token or ">" in token:
            continue  # template placeholder
        if scripts is not None:
            for _pm, name in PM_RUN.findall(token):
                if name in PM_BUILTINS or name in scripts:
                    continue
                out.append(Finding(INVALID_COMMANDS, "warning",
                                   f"`{name}` not found in package.json scripts",
                                   token.strip()))
        for name in MAKE_TARGET.findall(token):
            if make_targets and name not in make_targets:
                out.append(Finding(INVALID_COMMANDS, "warning",
                                   f"make target `{name}` not found in Makefile", token.strip()))
        for name in JUST_RECIPE.findall(token):
            if just_recipes and name not in just_recipes:
                out.append(Finding(INVALID_COMMANDS, "warning",
                                   f"just recipe `{name}` not found in justfile", token.strip()))
    return out


def check_paths(text: str, repo: Path) -> List[Finding]:
    out: List[Finding] = []
    seen = set()
    for token in BACKTICK.findall(text):
        token = token.strip()
        if " " in token or "://" in token or "<" in token or ">" in token:
            continue
        if "/" not in token:
            continue  # only check things that clearly look like repo paths
        if not re.fullmatch(r"[A-Za-z0-9_./*@-]+", token):
            continue
        if token in seen:
            continue
        seen.add(token)
        clean = token.rstrip("/").replace("/**", "").rstrip("*").rstrip("/")
        if not clean:
            continue
        if "*" in token:
            try:
                if next(iter(repo.glob(token)), None) is not None:
                    continue
            except (ValueError, OSError):
                continue
        if (repo / clean).exists():
            continue
        # Don't cry wolf on globs we couldn't expand; report only concrete missing paths.
        if "*" not in token:
            out.append(Finding(INVALID_PATHS, "warning", f"path `{token}` not found in repo",
                               "Confirm the path or remove it."))
    return out


def validate(agents_path: Path, repo: Optional[Path], max_lines: int, max_bytes: int) -> List[Finding]:
    text = agents_path.read_text(encoding="utf-8")
    headings = parse_headings(text)
    findings: List[Finding] = []
    findings += check_budget(text, max_lines, max_bytes)
    findings += check_sections(headings)
    findings += check_secrets(text)
    if repo is not None:
        findings += check_commands(text, repo)
        findings += check_paths(text, repo)
    return findings


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Validate an AGENTS.md file.")
    p.add_argument("agents_md", help="path to the AGENTS.md file")
    p.add_argument("--repo", help="repo root for command/path grounding", default=None)
    p.add_argument("--max-lines", type=int, default=180)
    p.add_argument("--max-bytes", type=int, default=32768)
    p.add_argument("--json", action="store_true", help="emit a JSON report")
    p.add_argument("--fail-on", default=",".join(sorted(DEFAULT_FAIL_ON)),
                   help="comma-separated check codes that cause a non-zero exit")
    args = p.parse_args(argv)

    agents_path = Path(args.agents_md)
    if not agents_path.is_file():
        print(f"error: file not found: {agents_path}", file=sys.stderr)
        return 2
    repo = Path(args.repo) if args.repo else None
    fail_on = {c.strip() for c in args.fail_on.split(",") if c.strip()}

    findings = validate(agents_path, repo, args.max_lines, args.max_bytes)
    failed = any(f.code in fail_on for f in findings)

    if args.json:
        print(json.dumps({
            "file": str(agents_path),
            "ok": not failed,
            "findings": [f.to_dict() for f in findings],
        }, indent=2))
        return 1 if failed else 0

    if not findings:
        print(f"OK: {agents_path} passed all checks.")
        return 0
    icon = {"error": "✗", "warning": "!", "info": "·"}
    for f in findings:
        line = f"{icon.get(f.severity, '·')} [{f.code}] {f.message}"
        print(line)
        if f.detail:
            print(f"    {f.detail}")
    n_err = sum(1 for f in findings if f.severity == "error")
    n_warn = sum(1 for f in findings if f.severity == "warning")
    print(f"\n{n_err} error(s), {n_warn} warning(s). {'FAIL' if failed else 'PASS'} "
          f"(fail-on: {', '.join(sorted(fail_on)) or 'none'})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
