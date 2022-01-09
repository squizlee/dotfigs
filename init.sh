#!/usr/bin/env bash
# Setup by installing and symlinking packages

# INSTALL PACKAGES
pacman -S fish emacs neovim kitty

# CONFIGURE FISHER
curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher

# SYMLINK CONFIG FILES


# DONE
echo "Make sure to run chsh -s /usr/bin/fish"
