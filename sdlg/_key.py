import sdl3

class _Key:
    def __init__(self):
        pass

    def get_pressed(self):
        return sdl3.SDL_GetKeyboardState(None)