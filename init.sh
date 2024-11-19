#!/usr/bin/env bash

echo "COPYING SHELL SCRIPTS"
mkdir -p "$HOME/.local/bin"
cp -r shell/. "$HOME/.local/bin"

echo "COPYING CONFIGURATIONS"
mkdir -p "$HOME/.config"
mkdir -p "$HOME/.config/nvim"
cp neovim/init.vim "$HOME/.config/nvim"

