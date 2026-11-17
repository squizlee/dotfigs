#!/usr/bin/env python3
"""Idempotently wire this repo into $HOME.

Safe to run any number of times:
  * symlinks that already point at the right place are left alone
  * real files in the way are moved aside to `<name>.bak-<timestamp>`, never deleted
  * stale links into this repo (e.g. a renamed skill) are pruned

Usage: ./init.py [--dry-run]
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = Path.home()
CEREBRUM = ROOT / "cerebrum"
SKILLS = CEREBRUM / "skills"
AGENTS_MD = CEREBRUM / "AGENTS.md"

# Agent harnesses that should see every cerebrum skill.
SKILL_DIRS = [HOME / ".claude" / "skills", HOME / ".codex" / "skills"]

# Plain one-to-one links: repo path -> home path.
LINKS = {
    ROOT / "emacs" / "init.el": HOME / ".config" / "emacs" / "init.el",
    AGENTS_MD: HOME / ".codex" / "AGENTS.md",
    ROOT / "shell" / "starship.toml": HOME / ".config" / "starship.toml",
    ROOT / "ghostty" / "config": HOME / ".config" / "ghostty" / "config",
}

# ~/.zshrc sources the repo's zshrc rather than being a symlink, so secrets and
# machine-local setup stay out of git. Appended so it runs after oh-my-zsh.
ZSHRC = HOME / ".zshrc"
ZSHRC_SOURCE = f'source "{ROOT / "shell" / "zshrc"}"'

# ~/.claude/CLAUDE.md imports AGENTS.md rather than being a symlink, so it can
# still hold machine-local notes below the import.
CLAUDE_MD = HOME / ".claude" / "CLAUDE.md"
CLAUDE_IMPORT = f"@{AGENTS_MD}"

DRY_RUN = False


def say(mark: str, msg: str) -> None:
    print(f"  {mark} {msg}")


def tilde(p: Path) -> str:
    return str(p).replace(str(HOME), "~", 1)


def link(src: Path, dst: Path) -> None:
    if dst.is_symlink() and dst.resolve() == src.resolve():
        return say("·", tilde(dst))

    if dst.is_symlink():
        say("↻", f"{tilde(dst)} (relinked)")
        if not DRY_RUN:
            dst.unlink()
    elif dst.exists():
        backup = dst.with_name(f"{dst.name}.bak-{time.strftime('%Y%m%d%H%M%S')}")
        say("⤳", f"{tilde(dst)} existed, moved to {backup.name}")
        if not DRY_RUN:
            dst.rename(backup)
    else:
        say("+", tilde(dst))

    if not DRY_RUN:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(src)


def prune(directory: Path) -> None:
    """Remove links in `directory` that point into this repo but no longer resolve."""
    if not directory.is_dir():
        return
    for entry in directory.iterdir():
        if entry.is_symlink() and not entry.exists():
            if (entry.parent / entry.readlink()).is_relative_to(ROOT):
                say("-", f"{tilde(entry)} (stale)")
                if not DRY_RUN:
                    entry.unlink()


def ensure_line(path: Path, line: str, *, append: bool = False) -> None:
    text = path.read_text() if path.exists() else ""
    if line in text.splitlines():
        return say("·", f"{tilde(path)} has {line}")
    say("+", f"{tilde(path)} ← {line}")
    if not DRY_RUN:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not text:
            path.write_text(f"{line}\n")
        elif append:
            path.write_text(f"{text.rstrip()}\n\n{line}\n")
        else:
            path.write_text(f"{line}\n\n{text}")


def section(title: str) -> None:
    print(f"\n▸ {title}")


def main() -> int:
    global DRY_RUN
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-n", "--dry-run", action="store_true", help="show what would change")
    DRY_RUN = parser.parse_args().dry_run

    if platform.system() not in ("Linux", "Darwin"):
        print(f"unsupported platform: {platform.system()}", file=sys.stderr)
        return 1

    print(f"(.)figs → {tilde(HOME)}" + ("  [dry run]" if DRY_RUN else ""))

    section("dotfiles")
    for src, dst in LINKS.items():
        link(src, dst)

    section("shell")
    ensure_line(ZSHRC, ZSHRC_SOURCE, append=True)

    section("cerebrum")
    ensure_line(CLAUDE_MD, CLAUDE_IMPORT)
    skills = sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    for target in SKILL_DIRS:
        prune(target)
        for skill in skills:
            link(skill, target / skill.name)
    if not skills:
        say("·", "no skills yet; add cerebrum/skills/<name>/SKILL.md")

    print("\n✓ done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
