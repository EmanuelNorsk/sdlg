import sdl3
import ctypes
import time as t
import resources.time as time

import psutil, os
import numpy as np
import encache
import sys
import math

import resources.rect as rect
import resources.font as font

import resources.image as sdlg_image

def sin_and_cos():


    angles = np.arange(360)  # Array of angles from 0 to 359
    radians = np.deg2rad(angles)  # Convert degrees to radians

    return np.sin(radians), np.cos(radians)


def bresenham_ellipse(radius_x, radius_y):
    x, y = 0, radius_y
    d = 3 - 2 * radius_y
    edge_points = []
    
    # Step 1: Generate the ellipse edge points
    while y >= x:
        edge_points.extend([
            (x * radius_x // radius_y, y), (-x * radius_x // radius_y, y),
            (x * radius_x // radius_y, -y), (-x * radius_x // radius_y, -y),
            (y * radius_x // radius_y, x), (-y * radius_x // radius_y, x),
            (y * radius_x // radius_y, -x), (-y * radius_x // radius_y, -x)
        ])
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
    
    # Step 2: Sort points by angle to ensure correct order
    edge_points = sorted(edge_points, key=lambda p: np.arctan2(p[1], p[0]))
    
    # Step 3: Generate triangle points
    triangles = []
    center = (0, 0)
    
    for i in range(len(edge_points)):
        p1 = edge_points[i]
        p2 = edge_points[(i + 1) % len(edge_points)]  # Wrap around to close the ellipse
        triangles.extend([center, p1, p2])  # Flattened list instead of tuples
    
    return triangles

def bresenham_ellipse_with_border(radius_x, radius_y, border_width):
    x, y = 0, radius_y
    d = 3 - 2 * radius_y
    edge_points = []
    
    # Step 1: Generate the ellipse edge points
    while y >= x:
        edge_points.extend([
            (x * radius_x // radius_y, y), (-x * radius_x // radius_y, y),
            (x * radius_x // radius_y, -y), (-x * radius_x // radius_y, -y),
            (y * radius_x // radius_y, x), (-y * radius_x // radius_y, x),
            (y * radius_x // radius_y, -x), (-y * radius_x // radius_y, -x)
        ])
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
    
    # Step 2: Sort points by angle to ensure correct order
    edge_points = sorted(edge_points, key=lambda p: np.arctan2(p[1], p[0]))

    small_radius_x = radius_x - border_width
    small_radius_y = radius_y - border_width

    x, y = 0, small_radius_y
    d = 3 - 2 * small_radius_y
    inner_points = []
    
    # Step 3: Generate the ellipse inner points
    while y >= x:
        inner_points.extend([
            (x * small_radius_x // small_radius_y, y), (-x * small_radius_x // small_radius_y, y),
            (x * small_radius_x // small_radius_y, -y), (-x * small_radius_x // small_radius_y, -y),
            (y * small_radius_x // small_radius_y, x), (-y * small_radius_x // small_radius_y, x),
            (y * small_radius_x // small_radius_y, -x), (-y * small_radius_x // small_radius_y, -x)
        ])
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6
    
    # Step 4: Sort points by angle to ensure correct order
    inner_points = sorted(inner_points, key=lambda p: np.arctan2(p[1], p[0]))


    # Step 5: Generate triangle points
    triangles = []

    ratio = len(inner_points) / len(edge_points)
    
    for i in range(len(edge_points)):
        p1 = edge_points[i]
        p2 = edge_points[(i + 1) % len(edge_points)]  # Wrap around to close the ellipse

        scale_i = int(i * ratio)

        p3 = inner_points[scale_i]
        p4 = inner_points[(scale_i + 1) % len(inner_points)]  # Wrap around to close the ellipse

        triangles.extend([p1, p2, p3, p2, p3, p4])  # Flattened list instead of tuples
    
    return triangles



sin_values, cos_values = sin_and_cos()


p = psutil.Process(os.getpid())
p.cpu_affinity([0, 1])

startup_time = t.time()

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)  # HIGH_PRIORITY_CLASS

def destroy_texture(texture):
    sdl3.SDL_DestroyTexture(texture)

cache = encache.Cache()

            

class Surface:
    def __init__(self, texture: sdl3.SDL_Texture):
        self.texture = texture
        width, height = ctypes.c_float(0), ctypes.c_float(0)
        sdl3.SDL_GetTextureSize(self.texture, ctypes.byref(width), ctypes.byref(height))
        self.rect = rect.Rect(0, 0, width.value, height.value)

        self.size = (width, height)

        self.textureRect = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), width, height)


    def get_rect(self, **kwargs):
        if kwargs.get("center", None):
            hWidth, hHeight = self.size[0].value / 2, self.size[1].value / 2
            self.rect = rect.Rect(kwargs["center"][0] - hWidth, kwargs["center"][1] - hHeight, self.size[0].value, self.size[1].value)
        return self.rect

class Font:
    def __init__(self, fileArg: str, size: int):
        global display
        self.file = fileArg
        self.size = size
        self.font = sdl3.TTF_OpenFont(self.file.encode(), ctypes.c_float(size))
        self.renderer = display.renderer


    def render(self, text: str, antialiasing, color, backgroundColor) -> Surface:
        textEncoded = text.encode()
        surface = sdl3.TTF_RenderText_Shaded(self.font, textEncoded, len(textEncoded), sdl3.SDL_Color(*color), sdl3.SDL_Color(*backgroundColor))
        texture = sdl3.SDL_CreateTextureFromSurface(self.renderer, surface)
        error = sdl3.SDL_GetError()
        if error:
            print(f"ERROR OVER HERE: {error}")
        return Surface(texture)

class Display:
    def __init__(self):
        self.window = sdl3.SDL_Window
        self.renderer = sdl3.SDL_Renderer
        self.draw_system = 0
        self.scale = False
        self.size = (0, 0)
        self.innerSize = (0, 0)
        self.image: Image = Image()

    def set_mode(self, size, flags = 0):
        self.window: sdl3.SDL_Window = sdl3.SDL_CreateWindow(b"Title", ctypes.c_long(size[0]), ctypes.c_long(size[1]), flags)
        print([sdl3.SDL_GetRenderDriver(x) for x in range(sdl3.SDL_GetNumRenderDrivers())])
        self.renderer: sdl3.SDL_Renderer = sdl3.SDL_CreateRenderer(self.window, b"vulkan")
        self.image.renderer = self.renderer
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
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, ctypes.c_long(self.size[0]), ctypes.c_long(self.size[1]), sdl3.SDL_LOGICAL_PRESENTATION_STRETCH)  
        else:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, ctypes.c_long(self.size[0]), ctypes.c_long(self.size[1]), sdl3.SDL_LOGICAL_PRESENTATION_DISABLED)                

    def setInnerSize(self, size: tuple):  
        self.innerSize = size
        if self.scale:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, ctypes.c_long(size[0]), ctypes.c_long(size[1]), sdl3.SDL_LOGICAL_PRESENTATION_STRETCH)  
        else:
            sdl3.SDL_SetRenderLogicalPresentation(self.renderer, ctypes.c_long(size[0]), ctypes.c_long(size[1]), sdl3.SDL_LOGICAL_PRESENTATION_DISABLED)   

    def blit(self, surface: Surface, rect: rect.Rect):
        if isinstance(rect, tuple) or isinstance(rect, list):
            sdl3.SDL_RenderTexture(self.renderer, surface.texture, surface.textureRect, sdl3.SDL_FRect(ctypes.c_float(rect[0]), ctypes.c_float(rect[1]), surface.size[0], surface.size[1]))
        else:
            sdl3.SDL_RenderTexture(self.renderer, surface.texture, surface.textureRect, rect.frect)


    
class Image:
    def __init__(self):
        pass

    def load(self, fileName) -> Surface:
        return sdlg_image.load(display.renderer, fileName)




    
class Draw:
    def __init__(self):
        pass

    def point(self, screen: Display):
        sdl3.SDL_RenderPoint(screen.renderer, ctypes.c_float(100), ctypes.c_float(100))

    def ellipse(self, screen: Display, color, rect_values, width = 0):

        cached_texture = cache.get(f"ellipse:{rect_values[2]}:{rect_values[3]}:{width}:{color}")

        sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]), ctypes.c_ubyte(color[3]))

        rectXInt = int(rect_values[0])
        rectYInt = int(rect_values[1])
        rect = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float((rect_values[2] * 2 + width)), ctypes.c_float((rect_values[3] * 2 + width)))
        if screen.draw_system == 0:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt)), ctypes.c_float((rectYInt)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        else:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt - rect_values[2] / 2 + screen.innerSize[0] / 2)), ctypes.c_float((-rectYInt - rect_values[3] / 2 + screen.innerSize[1] / 2)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        

        if cached_texture:
            sdl3.SDL_RenderTexture(screen.renderer, cached_texture, rect, rectFinal)
            error = sdl3.SDL_GetError()
            if error: print(error)
            return None
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

            

            #num_vertices = 3
            #vertices = (sdl3.SDL_Vertex * 3)(
            #    sdl3.SDL_Vertex(sdl3.SDL_FPoint(0, 0), sdl3.SDL_FColor(1, 0, 0, 1)),
            #    sdl3.SDL_Vertex(sdl3.SDL_FPoint(200, 100), sdl3.SDL_FColor(0, 1, 0, 1)),
            #    sdl3.SDL_Vertex(sdl3.SDL_FPoint(0, 200), sdl3.SDL_FColor(0, 0, 1, 1)),
            #)
            #
            #sdl3.SDL_RenderGeometry(screen.renderer, None, vertices, num_vertices, None, 0)

            center_x = rect_values[2] / 2
            center_y = rect_values[3] / 2

            if width > 0:
                points = bresenham_ellipse_with_border(center_x, center_y, width)
            else:
                points = bresenham_ellipse(center_x, center_y)

            #points = []

            #for x in range(0, 360, 1):
            #    points.append((sin_values[x] * center_x, cos_values[x] * center_y))
            #    points.append((sin_values[(x+1) % 360] * center_x, cos_values[(x+1) % 360] * center_y))
            #    points.append((0, 0))


            fcolor = sdl3.SDL_FColor(color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255 if len(color) > 3 else 1)




            vertexes = [sdl3.SDL_Vertex(sdl3.SDL_FPoint((point[0] + center_x), (point[1] + center_y)), fcolor) for point in points]

            

            num_vertices = len(vertexes)
            vertices = (sdl3.SDL_Vertex * num_vertices)(
                *vertexes
            )


            sdl3.SDL_RenderGeometry(screen.renderer, None, vertices, num_vertices, None, 0)
                
            sdl3.SDL_SetRenderTarget(screen.renderer, None)

            
            sdl3.SDL_RenderTexture(screen.renderer, texture, rect, rectFinal)


            cache.store(f"ellipse:{rect_values[2]}:{rect_values[3]}:{width}:{color}", texture, callback=destroy_texture)

            #sdl3.SDL_DestroyTexture(texture)



    def rect(self, screen: Display, color, rect_values, width = 0):
        sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]), ctypes.c_ubyte(color[3]))

        cached_texture = cache.get(f"rect:{rect_values[2]}:{rect_values[3]}:{width}:{color}")

        #print(cached_texture)

        rectXInt = int(rect_values[0])
        rectYInt = int(rect_values[1])
        rect = sdl3.SDL_FRect(ctypes.c_float(0), ctypes.c_float(0), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        if screen.draw_system == 0:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt)), ctypes.c_float((rectYInt)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))
        else:
            rectFinal = sdl3.SDL_FRect(ctypes.c_float((rectXInt - rect_values[2] / 2 + screen.innerSize[0] / 2)), ctypes.c_float((-rectYInt - rect_values[3] / 2 + screen.innerSize[1] / 2)), ctypes.c_float((rect_values[2])), ctypes.c_float((rect_values[3])))

        if cached_texture:
            sdl3.SDL_RenderTexture(screen.renderer, cached_texture, rect, rectFinal)
            error = sdl3.SDL_GetError()
            if error: print(error)
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

            cache.store(f"rect:{rect_values[2]}:{rect_values[3]}:{width}:{color}", texture, callback=destroy_texture)

            #sdl3.SDL_DestroyTexture(texture)

        return None
        



class Event:
    def __init__(self, type):
        self.type = type

class Events:
    def __init__(self):
        """
        Handles SDL events by wrapping them in Python-friendly objects.
        """
        # Create an SDL_Event structure
        self.sdl_event = sdl3.SDL_Event()
        self.started = t.time() + 0.1

    def get(self):
        """
        Retrieves all SDL events and returns them as Event objects.

        Returns:
            list[Event]: A list of Event objects.
        """
        sdl3.SDL_PumpEvents()
        event_list = []
        while sdl3.SDL_PollEvent(self.sdl_event):
            event = Event(self.sdl_event.type)
            event_list.append(event)
        return event_list




class Key:
    def __init__(self):
        pass

    def get_pressed(self):
        return sdl3.SDL_GetKeyboardState(None)
    






def init():
    sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS | sdl3.SDL_INIT_AUDIO)
    sdl3.TTF_Init()

def quit():
    sdl3.SDL_DestroyRenderer(display.renderer)
    sdl3.SDL_DestroyWindow(display.window)
    sdl3.SDL_Quit()

display = Display()
image: Image = display.image
event = Events()
draw = Draw()
key = Key()

RESIZABLE = sdl3.SDL_WINDOW_RESIZABLE
QUIT = sdl3.SDL_EVENT_QUIT
VIDEORESIZE = sdl3.SDL_EVENT_WINDOW_RESIZED




# Letters
K_a = sdl3.SDL_SCANCODE_A
K_b = sdl3.SDL_SCANCODE_B
K_c = sdl3.SDL_SCANCODE_C
K_d = sdl3.SDL_SCANCODE_D
K_e = sdl3.SDL_SCANCODE_E
K_f = sdl3.SDL_SCANCODE_F
K_g = sdl3.SDL_SCANCODE_G
K_h = sdl3.SDL_SCANCODE_H
K_i = sdl3.SDL_SCANCODE_I
K_j = sdl3.SDL_SCANCODE_J
K_k = sdl3.SDL_SCANCODE_K
K_l = sdl3.SDL_SCANCODE_L
K_m = sdl3.SDL_SCANCODE_M
K_n = sdl3.SDL_SCANCODE_N
K_o = sdl3.SDL_SCANCODE_O
K_p = sdl3.SDL_SCANCODE_P
K_q = sdl3.SDL_SCANCODE_Q
K_r = sdl3.SDL_SCANCODE_R
K_s = sdl3.SDL_SCANCODE_S
K_t = sdl3.SDL_SCANCODE_T
K_u = sdl3.SDL_SCANCODE_U
K_v = sdl3.SDL_SCANCODE_V
K_w = sdl3.SDL_SCANCODE_W
K_x = sdl3.SDL_SCANCODE_X
K_y = sdl3.SDL_SCANCODE_Y
K_z = sdl3.SDL_SCANCODE_Z

# Numbers
K_1 = sdl3.SDL_SCANCODE_1
K_2 = sdl3.SDL_SCANCODE_2
K_3 = sdl3.SDL_SCANCODE_3
K_4 = sdl3.SDL_SCANCODE_4
K_5 = sdl3.SDL_SCANCODE_5
K_6 = sdl3.SDL_SCANCODE_6
K_7 = sdl3.SDL_SCANCODE_7
K_8 = sdl3.SDL_SCANCODE_8
K_9 = sdl3.SDL_SCANCODE_9
K_0 = sdl3.SDL_SCANCODE_0

# Symbols
K_MINUS = sdl3.SDL_SCANCODE_MINUS          # '-'
K_EQUALS = sdl3.SDL_SCANCODE_EQUALS        # '='
K_LEFTBRACKET = sdl3.SDL_SCANCODE_LEFTBRACKET  # '['
K_RIGHTBRACKET = sdl3.SDL_SCANCODE_RIGHTBRACKET # ']'
K_BACKSLASH = sdl3.SDL_SCANCODE_BACKSLASH  # '\'
K_SEMICOLON = sdl3.SDL_SCANCODE_SEMICOLON  # ';'
K_APOSTROPHE = sdl3.SDL_SCANCODE_APOSTROPHE # '
K_COMMA = sdl3.SDL_SCANCODE_COMMA          # ''
K_PERIOD = sdl3.SDL_SCANCODE_PERIOD        # '.'
K_SLASH = sdl3.SDL_SCANCODE_SLASH          # '/'

# Function Keys
K_F1 = sdl3.SDL_SCANCODE_F1
K_F2 = sdl3.SDL_SCANCODE_F2
K_F3 = sdl3.SDL_SCANCODE_F3
K_F4 = sdl3.SDL_SCANCODE_F4
K_F5 = sdl3.SDL_SCANCODE_F5
K_F6 = sdl3.SDL_SCANCODE_F6
K_F7 = sdl3.SDL_SCANCODE_F7
K_F8 = sdl3.SDL_SCANCODE_F8
K_F9 = sdl3.SDL_SCANCODE_F9
K_F10 = sdl3.SDL_SCANCODE_F10
K_F11 = sdl3.SDL_SCANCODE_F11
K_F12 = sdl3.SDL_SCANCODE_F12

# Navigation Keys
K_UP = sdl3.SDL_SCANCODE_UP
K_DOWN = sdl3.SDL_SCANCODE_DOWN
K_LEFT = sdl3.SDL_SCANCODE_LEFT
K_RIGHT = sdl3.SDL_SCANCODE_RIGHT

# Control Keys
K_TAB = sdl3.SDL_SCANCODE_TAB
K_CAPSLOCK = sdl3.SDL_SCANCODE_CAPSLOCK
K_LSHIFT = sdl3.SDL_SCANCODE_LSHIFT
K_RSHIFT = sdl3.SDL_SCANCODE_RSHIFT
K_LCTRL = sdl3.SDL_SCANCODE_LCTRL
K_RCTRL = sdl3.SDL_SCANCODE_RCTRL
K_LALT = sdl3.SDL_SCANCODE_LALT
K_RALT = sdl3.SDL_SCANCODE_RALT
K_SPACE = sdl3.SDL_SCANCODE_SPACE
K_RETURN = sdl3.SDL_SCANCODE_RETURN
K_BACKSPACE = sdl3.SDL_SCANCODE_BACKSPACE
K_ESCAPE = sdl3.SDL_SCANCODE_ESCAPE





# init()
# Screen = display.set_mode((640, 480), RESIZABLE)
# started = t.perf_counter()
# running = True

# fps = 0
# fps_per_second = 0
# last_fps_per_second = t.perf_counter()

# while running:

#     for e in event.get():
#         if e.type == QUIT:
#             running = False

#     Screen.fill((255,255,255,255))
#     draw.rect(Screen, (0,0,0,255), (100, 100, 100, 100))


#     fps += 1
#     if last_fps_per_second + 1 <= t.perf_counter():
#         last_fps_per_second += 1
#         fps_per_second = fps
#         fps = 0
#         print(f"FPS: {fps_per_second}")

#     keys = key.get_pressed()
#     if keys[K_w]:
#         print("Key W Pressed!")

#     display.update()

# quit()


