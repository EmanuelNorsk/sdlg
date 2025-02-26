import ctypes
import platform

import sdl3


SDL_int = int
if platform.system() == "Windows":
    pass
    # SDL_int = ctypes.c_long  # Not sure why this was being used, so sticking it here


class _Display:
    def __init__(self):
        self.window = sdl3.SDL_Window
        self.renderer = sdl3.SDL_Renderer
        self.draw_system = 0
        self.scale = False
        self.size = (0, 0)
        self.innerSize = (0, 0)

    def set_mode(self, size, flags = 0):
        self.window: sdl3.SDL_Window = sdl3.SDL_CreateWindow(b"Title", SDL_int(size[0]), SDL_int(size[1]), ctypes.c_ulonglong(flags))
        print([sdl3.SDL_GetRenderDriver(x) for x in range(sdl3.SDL_GetNumRenderDrivers())])
        self.renderer: sdl3.SDL_Renderer = sdl3.SDL_CreateRenderer(self.window, b"opengl")
        self.size = size
        self.innerSize = size
        return self
    def fill(self, rgba):
        sdl3.SDL_SetRenderDrawColor(self.renderer, ctypes.c_ubyte(rgba[0]), ctypes.c_ubyte(rgba[1]), ctypes.c_ubyte(rgba[2]), ctypes.c_ubyte(rgba[3]))
        sdl3.SDL_RenderClear(self.renderer)
    def flip(self):
        sdl3.SDL_RenderPresent(self.renderer)
    def update(self):
        sdl3.SDL_RenderPresent(self.renderer)
    def cartesian_coordinate_system(self, bool):
        if bool:
            self.draw_system = 1
        else:
            self.draw_system = 0

    def scaleWindow(self, scale: bool):
        self.scale: bool = scale
        if scale:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, SDL_int(self.size[0]), SDL_int(self.size[1]), sdl3.SDL_LOGICAL_PRESENTATION_STRETCH)
        else:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, SDL_int(self.size[0]), SDL_int(self.size[1]), sdl3.SDL_LOGICAL_PRESENTATION_DISABLED)

    def setInnerSize(self, size: tuple):
        self.innerSize = size
        if self.scale:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, SDL_int(size[0]), SDL_int(size[1]), sdl3.SDL_LOGICAL_PRESENTATION_STRETCH)
        else:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, SDL_int(size[0]), SDL_int(size[1]), sdl3.SDL_LOGICAL_PRESENTATION_DISABLED)
