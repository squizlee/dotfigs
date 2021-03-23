" Space is leader key
nmap <Space> <leader>


"----- Plugins -----
"
if ! filereadable(system('echo -n "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/plug.vim"'))
	echo "Downloading junegunn/vim-plug to manage plugins..."
	silent !mkdir -p ${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/
	silent !curl "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim" > ${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/plug.vim
	autocmd VimEnter * PlugInstall
endif

call plug#begin(system('echo -n "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/plugged"'))
Plug 'junegunn/goyo.vim'
Plug 'sheerun/vim-polyglot'
Plug 'dracula/vim'
Plug 'lervag/vimtex'
call plug#end()
"----- End Plugins -----

" plugin options
" Vim markdown has a nasty habit of auto indenting on lists when you don't want it to
let g:vim_markdown_auto_insert_bullets = 0
let g:vim_markdown_new_list_item_indent = 0

"----- Key Bindings -----
imap jj <Esc>
nmap <leader>g :Goyo<CR>
nmap <leader>p "+p
vmap <leader>y "+y
"----- End Key Bindings -----

"----- Colour scheme -----
colorscheme dracula
"----- End Color scheme -----

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

" Indentation options
set shiftwidth=4
set tabstop=4

" Remove annoying comment insertion
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Visualize blank characters
":set listchars=tab:->,trail:~,extends:>,precedes:<
":set list

