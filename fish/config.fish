# Setup prompt
starship init fish | source

# Aliases
alias cg="cd ~/garden"
alias cl="clear"
alias vim="nvim"
alias ssh="kitty +kitten ssh"
alias scheme="rlwrap mit-scheme"
alias gscheme="rlwrap guile"

fish_add_path ~/bin

# Variables
set -U XDG_CONFIG_HOME "~/.config"

# Remove default fish greeting message
function fish_greeting
	set rules "1. The world is full of fascinating problems waiting to be solved"
	set -a rules "2. No problem should ever have to be solved twice."
	set -a rules "3. Boredom and drudgery are evil."
	set -a rules "4. Freedom is good."
	set -a rules "5. Attitude is no substitute for competence"
	echo $rules[(random 1 5)]
	echo The time is (date)
end

function za
	zathura $argv &
end

function mcd
	mkdir $argv
	cd $argv
end

