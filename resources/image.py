import sdl3, ctypes, sdlg


def load(renderer, fileName):
    return sdlg.Surface(sdl3.IMG_LoadTexture(renderer, fileName.encode()))