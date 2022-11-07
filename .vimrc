# Скачиваем VimPlug 
# curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
#   https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
# Загружаем данный файл в домашний каталог и вводим :PlugInstall
# Для запуска встроеной обучалки набрать :help tutor

:set number
call plug#begin()
Plug 'vim-airline/vim-airline'
Plug 'scrooloose/nerdtree'
Plug 'sheerun/vim-polyglot'
Plug 'dracula/vim'
call plug#end()
syntax enable
colorscheme dracula
autocmd VimEnter * NERDTree | wincmd p
