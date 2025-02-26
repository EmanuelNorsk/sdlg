import ctypes

import sdl3

from sdlg._display import _Display
from sdlg._cache import _Cache

_cache = _Cache()


def destroy_texture(texture):
    sdl3.SDL_DestroyTexture(texture)


class _Draw:
    def __init__(self):
        pass

    def rect(self, screen: _Display, color, rect_values, width = 0):

        global _cache
        sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]), ctypes.c_ubyte(color[3]))

        cached_texture = _cache.get(f"rect:{rect_values[2]}:{rect_values[3]}:{width}:{color}")

        #print(cached_texture)

        rectXInt = int(rect_values[0])
        rectYInt = int(rect_values[1])
        rect = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        if screen.draw_system == 0:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt)), ctypes.c_float((rectYInt)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        else:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt - rect_values[2] / 2 + screen.innerSize[0] / 2)), ctypes.c_float((-rectYInt - rect_values[3] / 2 + screen.innerSize[1] / 2)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))

        if cached_texture:

            sdl3.SDL_SetTextureColorMod(cached_texture, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]))
            sdl3.SDL_RenderTexture(screen.renderer, cached_texture, rect, rectFinal)
            error = sdl3.SDL_GetError()
            if error:
                print(error)
        else:

            texture = sdl3.SDL_CreateTexture(
                screen.renderer,
                sdl3.SDL_PIXELFORMAT_RGBA8888,
                sdl3.SDL_TEXTUREACCESS_TARGET,
                rect_values[2], rect_values[3]
            )

            sdl3.SDL_SetRenderTarget(screen.renderer, texture)
            sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(0), ctypes.c_ubyte(0), ctypes.c_ubyte(0), ctypes.c_ubyte(0))
            sdl3.SDL_RenderClear(screen.renderer)

            sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]), ctypes.c_ubyte(color[3]))

            if width == 0:
                rect1 = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float(rect_values[2]), ctypes.c_float(rect_values[3]))

                sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect1))
            else:
                rect1 = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float(width), ctypes.c_float(rect_values[3]))
                rect2 = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float(rect_values[2]), ctypes.c_float(width))
                rect3 = sdl3.SDL_FRect(ctypes.c_float((rect_values[2] - width)), ctypes.c_float(0), ctypes.c_float(width), ctypes.c_float(rect_values[3]))
                rect4 = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float((rect_values[3] - width)), ctypes.c_float(rect_values[2]), ctypes.c_float(width))

                sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect1))
                sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect2))
                sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect3))
                sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect4))

            sdl3.SDL_SetRenderTarget(screen.renderer, None)
            sdl3.SDL_RenderTexture(screen.renderer, texture, rect, rectFinal)

            _cache.set(f"rect:{rect_values[2]}:{rect_values[3]}:{width}:{color}", texture, callback=destroy_texture)

            #sdl3.SDL_DestroyTexture(texture)

        return None
