" remapping keys
let mapleader = " "

imap jj <Esc>

" Unbind useless bindings
nmap Q <Nop> 

" enable useful features
set nocompatible

" Turn on syntax highlighting
syntax on

" Show line numbers and relative numbers
set number
set relativenumber

" Always show the status line at the bottome
set laststatus=2

" allow backspace to delete over indentation, end-of-lines, and insert mode
" start
set backspace=indent,eol,start

" case-insensitive searching 
set ignorecase
set smartcase

" searching as you type
set incsearch

" Disable annoying audible bell
set noerrorbells visualbell t_vb=

" Better command-line completion
set wildmenu

" show partial commands in the last line of the screen
set showcmd

" auto indentation
set autoindent

" Indentation options
set shiftwidth=4
set softtabstop=4
