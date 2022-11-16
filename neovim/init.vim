" Space is leader key
nmap <Space> <leader>

"----- Key Bindings -----
imap jk <Esc> 
""--- Window manipulation
nmap <leader>ws :split<CR>
nmap <leader>wj <C-w>j
nmap <leader>wk <C-w>k

nmap <leader>p "+p
vmap <leader>y "+y
"----- End Key Bindings -----

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

