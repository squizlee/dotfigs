# (.)figs

My dotfiles. `./init.py` sets everything up and is safe to rerun (`-n` for a dry run).

- `cerebrum/`: AGENTS.md and LLM skills ([details](cerebrum/README.md))
- `emacs/`: org-mode Emacs config
- `ghostty/`: Ghostty terminal config (green theme, cmd+j/k to switch tabs). `init.py` also copies its colors into VS Code's integrated terminal (a marked block in `vscode/settings.json`)
- `vscode/`: VS Code user settings (linked into VS Code's user dir) and `extensions.txt`, which `init.py` installs if missing (it never uninstalls)
- `macos/duti`: default apps per file type (`.md`, `.py`, … open in VS Code). Needs `brew install duti`
- `hammerspoon/`: macOS-only hotkeys (ctrl+option+t opens or focuses Ghostty)
- `shell/`: zsh config and Starship prompt. `~/.zshrc` stays local (secrets, machine setup) and sources `shell/zshrc` from its last line
