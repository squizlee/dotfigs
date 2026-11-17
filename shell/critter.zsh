# Prompt critter: a little face at the start of the prompt that reacts to
# what's going on. Starship draws it from $CRITTER via its env_var module
# (shell/starship.toml), which is why the variable is exported.

zmodload zsh/datetime              # EPOCHREALTIME, EPOCHSECONDS, strftime
autoload -Uz add-zsh-hook add-zle-hook-widget

typeset -g CRITTER_LONG_SECS=10    # a command at least this long earns a flex
typeset -g CRITTER_DOZE_SECS=300   # idle this long at the prompt and it dozes off

typeset -g _critter_started=0      # when the running command began (0 = none)
typeset -g _critter_awake=''       # the face to return to when woken
typeset -g _critter_asleep=0
typeset -g _critter_seen=''        # line + cursor at the last timer tick
export CRITTER='(•ᴗ•)'

_critter_preexec() { _critter_started=$EPOCHREALTIME }

# First match wins, so the most useful news shows.
_critter_precmd() {
  local last=$? hour
  local -F took=0
  (( _critter_started )) && took=$(( EPOCHREALTIME - _critter_started ))
  _critter_started=0
  _critter_asleep=0
  _critter_seen='0'                # empty line, cursor at 0
  strftime -s hour %H $EPOCHSECONDS

  if (( last != 0 )); then
    CRITTER='(×_×)'
  elif (( took >= CRITTER_LONG_SECS )); then
    CRITTER='(•̀ᴗ•́)و'
  elif (( EUID == 0 )) || [[ -n $SSH_CONNECTION ]]; then
    CRITTER='(◉_◉)'
  elif [[ -n $(command git --no-optional-locks status --porcelain 2>/dev/null | head -c1) ]]; then
    CRITTER='(•_•)?'
  elif (( 10#$hour < 5 )); then
    CRITTER='(-_-)zᶻ'
  elif (( 10#$hour >= 6 && 10#$hour < 10 )); then
    CRITTER='(•ᴗ•)☕'
  else
    CRITTER='(•ᴗ•)'
  fi
  _critter_awake=$CRITTER
}

add-zsh-hook preexec _critter_preexec
add-zsh-hook precmd _critter_precmd

# Dozing: while the prompt waits, zsh raises SIGALRM every TMOUT seconds
# (counted from the prompt, not the last keypress). Because TRAPALRM is
# defined, that only runs this; without it, TMOUT would log the shell out, so
# keep the two together. It dozes only if the line hasn't changed since the
# previous tick, so it never nods off mid-typing.
TMOUT=$CRITTER_DOZE_SECS
TRAPALRM() {
  (( _critter_asleep )) && return
  if [[ "$BUFFER$CURSOR" != "$_critter_seen" ]]; then
    _critter_seen="$BUFFER$CURSOR"
    return
  fi
  _critter_asleep=1
  CRITTER='(-_-)zᶻ'
  zle && zle reset-prompt
}

# Wake on the first keypress that changes the line or moves the cursor.
_critter_wake() {
  (( _critter_asleep )) || return
  [[ "$BUFFER$CURSOR" == "$_critter_seen" ]] && return
  _critter_seen="$BUFFER$CURSOR"
  _critter_asleep=0
  CRITTER=$_critter_awake
  zle reset-prompt
}
add-zle-hook-widget line-pre-redraw _critter_wake
