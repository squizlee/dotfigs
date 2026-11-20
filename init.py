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
import json
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = Path.home()
CEREBRUM = ROOT / "cerebrum"
SKILLS = CEREBRUM / "skills"
AGENTS_MD = CEREBRUM / "AGENTS.md"

VSCODE_SETTINGS = (
    HOME / ("Library/Application Support" if platform.system() == "Darwin" else ".config")
    / "Code" / "User" / "settings.json"
)

# Agent harnesses that should see every cerebrum skill.
SKILL_DIRS = [HOME / ".claude" / "skills", HOME / ".codex" / "skills"]

# Plain one-to-one links: repo path -> home path.
LINKS = {
    ROOT / "emacs" / "init.el": HOME / ".config" / "emacs" / "init.el",
    AGENTS_MD: HOME / ".codex" / "AGENTS.md",
    ROOT / "shell" / "starship.toml": HOME / ".config" / "starship.toml",
    ROOT / "ghostty" / "config": HOME / ".config" / "ghostty" / "config",
    ROOT / "ghostty" / "shaders": HOME / ".config" / "ghostty" / "shaders",
    ROOT / "vscode" / "settings.json": VSCODE_SETTINGS,
}

# Links that only make sense on macOS.
MACOS_LINKS = {
    ROOT / "hammerspoon" / "init.lua": HOME / ".hammerspoon" / "init.lua",
}

# ~/.zshrc sources the repo's zshrc rather than being a symlink, so secrets and
# machine-local setup stay out of git. Appended so it runs after oh-my-zsh.
ZSHRC = HOME / ".zshrc"
ZSHRC_SOURCE = f'source "{ROOT / "shell" / "zshrc"}"'

# ~/.claude/CLAUDE.md imports AGENTS.md rather than being a symlink, so it can
# still hold machine-local notes below the import.
CLAUDE_MD = HOME / ".claude" / "CLAUDE.md"
CLAUDE_IMPORT = f"@{AGENTS_MD}"

# vscode/settings.json is linked in like the other dotfiles; a generated block at
# its top mirrors the Ghostty colors onto the integrated terminal.
GHOSTTY_CONFIG = ROOT / "ghostty" / "config"
VSCODE_BLOCK_START = "// >>> dotfigs: terminal colors from ghostty/config (init.py rewrites this block)"
VSCODE_BLOCK_END = "// <<< dotfigs"
ANSI_NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]

# Extensions to install if missing; ones not listed are left alone.
VSCODE_EXTENSIONS = ROOT / "vscode" / "extensions.txt"

# macOS default apps per file type, one `duti -s` per line.
DUTI = ROOT / "macos" / "duti"

DRY_RUN = False


def say(mark: str, msg: str) -> None:
    print(f"  {mark} {msg}")


def tilde(p: Path) -> str:
    return str(p).replace(str(HOME), "~", 1)


def link(src: Path, dst: Path, *, quiet_if_current: bool = False) -> bool:
    if dst.is_symlink() and dst.resolve() == src.resolve():
        if not quiet_if_current:
            say("·", tilde(dst))
        return False

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
    return True


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


def ghostty_terminal_colors() -> dict[str, str]:
    conf: dict[str, str] = {}
    palette: dict[int, str] = {}
    for line in GHOSTTY_CONFIG.read_text().splitlines():
        key, sep, value = line.partition("=")
        if not sep or line.lstrip().startswith("#"):
            continue
        key, value = key.strip(), value.strip()
        if key == "palette":
            index, _, color = value.partition("=")
            palette[int(index)] = color.strip()
        else:
            conf[key] = value

    colors = {
        "terminal.background": conf["background"],
        "terminal.foreground": conf["foreground"],
        "terminalCursor.foreground": conf["cursor-color"],
        "terminal.selectionBackground": conf["selection-background"],
        "terminal.selectionForeground": conf["selection-foreground"],
    }
    for i, name in enumerate(ANSI_NAMES):
        colors[f"terminal.ansi{name}"] = palette[i]
        colors[f"terminal.ansiBright{name}"] = palette[i + 8]
    return colors


def sync_vscode_terminal() -> None:
    """Write the Ghostty colors into a marked block at the top of VS Code's settings.json."""
    if not VSCODE_SETTINGS.exists():
        return say("·", f"{tilde(VSCODE_SETTINGS)} not found, skipped")

    settings = {
        "workbench.colorCustomizations": ghostty_terminal_colors(),
        # VS Code otherwise nudges low-contrast colors, so the greens drift from Ghostty's.
        "terminal.integrated.minimumContrastRatio": 1,
    }
    body = json.dumps(settings, indent=2).splitlines()[1:-1]
    block = "\n".join([f"  {VSCODE_BLOCK_START}", *body[:-1], body[-1] + ",", f"  {VSCODE_BLOCK_END}"])

    text = VSCODE_SETTINGS.read_text()
    pattern = re.compile(rf"^[ \t]*{re.escape(VSCODE_BLOCK_START)}\n.*?^[ \t]*{re.escape(VSCODE_BLOCK_END)}$", re.S | re.M)
    outside = pattern.sub("", text)
    clashes = [k for k in settings if f'"{k}"' in outside]
    if clashes:
        return say("!", f"{tilde(VSCODE_SETTINGS)} already sets {', '.join(clashes)}; remove it and rerun")

    if pattern.search(text):
        new = pattern.sub(lambda _: block, text)
    else:
        new = re.sub(r"^\s*\{", lambda m: f"{m.group(0)}\n{block}", text, count=1)
    if new == text:
        return say("·", "terminal colors match ghostty/config")
    say("+", "terminal colors ← ghostty/config")
    if not DRY_RUN:
        VSCODE_SETTINGS.write_text(new)


def install_vscode_extensions() -> None:
    """Install each extension in vscode/extensions.txt that isn't already installed."""
    if not shutil.which("code"):
        return say("!", "`code` not on PATH (VS Code: Shell Command: Install 'code'), extensions skipped")
    wanted = [
        line.strip() for line in VSCODE_EXTENSIONS.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    listed = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True).stdout
    installed = {ext.lower() for ext in listed.split()}
    missing = [ext for ext in wanted if ext.lower() not in installed]
    if not missing:
        return say("·", f"{len(wanted)} extensions")
    for ext in missing:
        if DRY_RUN:
            say("+", ext)
            continue
        result = subprocess.run(["code", "--install-extension", ext], capture_output=True, text=True)
        if result.returncode == 0:
            say("+", ext)
        else:
            say("!", f"{ext} failed: {(result.stderr or result.stdout).strip()}")


def apply_default_apps() -> None:
    """Point each file type in macos/duti at its app, skipping ones already set."""
    if not shutil.which("duti"):
        return say("!", "duti not installed (brew install duti), default apps skipped")
    current_types: dict[str, list[str]] = {}
    for line in DUTI.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        bundle, kind, role = line.split()
        if kind.startswith("."):
            # `duti -x ext` prints the current handler's name, path, then bundle id.
            current = subprocess.run(["duti", "-x", kind[1:]], capture_output=True, text=True).stdout.split("\n")
            if len(current) > 2 and current[2].strip().lower() == bundle.lower():
                current_types.setdefault(bundle, []).append(kind)
                continue
        if DRY_RUN:
            say("+", f"{kind} → {bundle}")
            continue
        result = subprocess.run(["duti", "-s", bundle, kind, role], capture_output=True, text=True)
        if result.returncode == 0:
            say("+", f"{kind} → {bundle}")
        else:
            say("!", f"{kind} → {bundle} failed: {result.stderr.strip()}")
    for bundle, kinds in current_types.items():
        say("·", f"{', '.join(kinds)} → {bundle}")


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
    if platform.system() == "Darwin":
        for src, dst in MACOS_LINKS.items():
            link(src, dst)

    section("vscode")
    sync_vscode_terminal()
    install_vscode_extensions()

    if platform.system() == "Darwin":
        section("default apps")
        apply_default_apps()

    section("shell")
    ensure_line(ZSHRC, ZSHRC_SOURCE, append=True)

    section("cerebrum")
    ensure_line(CLAUDE_MD, CLAUDE_IMPORT)
    skills = sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    for target in SKILL_DIRS:
        prune(target)
        current = 0
        for skill in skills:
            if not link(skill, target / skill.name, quiet_if_current=True):
                current += 1
        if current:
            say("·", f"{current} skill link{'s' if current != 1 else ''} up to date in {tilde(target)}")
    if not skills:
        say("·", "no skills yet; add cerebrum/skills/<name>/SKILL.md")

    print("\n✓ done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
