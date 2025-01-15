import sdl3
import ctypes
import time as t
import resources.time as time

cache = None
startup_time = t.time()

class Display:
    def __init__(self):
        self.window = sdl3.SDL_Window
        self.renderer = sdl3.SDL_Renderer
        self.draw_system = 0
        self.innerSize = (0, 0)
        self.scale = False
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.lastSize = (0, 0)
    def set_mode(self, size, flags = 0):
        self.window: sdl3.SDL_Window = sdl3.SDL_CreateWindow(b"Title", ctypes.c_long(size[0]), ctypes.c_long(size[1]), ctypes.c_ulonglong(flags))
        self.renderDriver = ctypes.c_char_p(b"software")
        self.renderHint = ctypes.c_char_p(sdl3.SDL_HINT_RENDER_DRIVER.encode('utf-8'))
        sdl3.SDL_SetHint(self.renderHint, self.renderDriver)
        self.renderer: sdl3.SDL_Renderer = sdl3.SDL_CreateRenderer(self.window, None)
        self.innerSize = size
        return self
    def fill(self, rgba):
        sdl3.SDL_SetRenderDrawColor(self.renderer, ctypes.c_ubyte(rgba[0]), ctypes.c_ubyte(rgba[1]), ctypes.c_ubyte(rgba[2]), ctypes.c_ubyte(rgba[3]))
        sdl3.SDL_RenderClear(self.renderer)
    def flip(self):
        sdl3.SDL_RenderPresent(self.renderer)
    def update(self):
        sdl3.SDL_RenderPresent(self.renderer)
    def get_fps(self):
        return sdl3.SDL_GetPerformanceFrequency()
    def cartesian_coordinate_system(self, bool):
        if bool:
            self.draw_system = 1
        else:
            self.draw_system = 0

    def scaleWindow(self, scale: bool):
        self.scale: bool = scale
        if scale:
                            
            width = ctypes.c_int()
            height = ctypes.c_int()
            sdl3.SDL_GetWindowSizeInPixels(self.window, ctypes.byref(width), ctypes.byref(height))
            self.innerSize = (width.value, height.value)
            self.scaleX = 1
            self.scaleY = 1

    def setInnerSize(self, size: tuple):
        self.innerSize: tuple = size
        width = ctypes.c_int()
        height = ctypes.c_int()
        sdl3.SDL_GetWindowSizeInPixels(self.window, ctypes.byref(width), ctypes.byref(height))
        if self.scale:
            self.scaleX = width.value / self.innerSize[0]
            self.scaleY = height.value / self.innerSize[1]


    
class Draw:
    def __init__(self):
        pass
    def rect(self, screen: Display, color, rect_values, width = 0):
        global cache
        sdl3.SDL_SetRenderDrawColor(screen.renderer, ctypes.c_ubyte(color[0]), ctypes.c_ubyte(color[1]), ctypes.c_ubyte(color[2]), ctypes.c_ubyte(color[3]))
        if width == 0:
            if screen.draw_system == 0:
                rect = sdl3.SDL_FRect(ctypes.c_float((rect_values[0] * screen.scaleX)), ctypes.c_float((rect_values[1] * screen.scaleY)), ctypes.c_float((rect_values[2] * screen.scaleX)), ctypes.c_float((rect_values[3] * screen.scaleY)))
            else:
                width = ctypes.c_int()
                height = ctypes.c_int()
                sdl3.SDL_GetWindowSizeInPixels(screen.window, ctypes.byref(width), ctypes.byref(height))
                if screen.scale == False:
                    rect = sdl3.SDL_FRect(ctypes.c_float(rect_values[0] + width.value / 2 - rect_values[2] / 2), ctypes.c_float(-rect_values[1] + height.value / 2 - rect_values[3] / 2), ctypes.c_float(rect_values[2]), ctypes.c_float(rect_values[3]))
                else:
                    if cache != None and startup_time < t.time() - 1:
                        rect = cache
                        cache = None
                    else:
                        if cache != None:
                            cache = None
                        if screen.lastSize != (width.value, height.value):
                            screen.scaleX = width.value / screen.innerSize[0]
                            screen.scaleY = height.value / screen.innerSize[1]
                            screen.lastSize = (width.value, height.value)

                        x = ( rect_values[0] / screen.innerSize[0] + 0.5) * width.value  - (rect_values[2] * screen.scaleX / 2)
                        y = (-rect_values[1] / screen.innerSize[1] + 0.5) * height.value - (rect_values[3] * screen.scaleY / 2)

                        rect = sdl3.SDL_FRect(ctypes.c_float(x), ctypes.c_float(y), ctypes.c_float((rect_values[2] * screen.scaleX)), ctypes.c_float((rect_values[3] * screen.scaleY)))  
            error = sdl3.SDL_GetError()
            if error: print(error)
            sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect))
            error = sdl3.SDL_GetError()
            if error: print(error)

            return rect

        else:
            rect = sdl3.SDL_FRect(ctypes.c_float(rect_values[0]), ctypes.c_float(rect_values[1]), ctypes.c_float(rect_values[2]), ctypes.c_float(width))
            sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect))

            rect = sdl3.SDL_FRect(ctypes.c_float(rect_values[0]) + ctypes.c_float(rect_values[2]) - ctypes.c_float(width), ctypes.c_float(rect_values[1]), ctypes.c_float(width), ctypes.c_float(rect_values[3]))
            sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect))

            rect = sdl3.SDL_FRect(ctypes.c_float(rect_values[0]), ctypes.c_float(rect_values[1]) + ctypes.c_float(rect_values[3]) - ctypes.c_float(width), ctypes.c_float(rect_values[2]), ctypes.c_float(width))
            sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect))

            rect = sdl3.SDL_FRect(ctypes.c_float(rect_values[0]), ctypes.c_float(rect_values[1]), ctypes.c_float(width), ctypes.c_float(rect_values[3]))
            sdl3.SDL_RenderFillRect(screen.renderer, ctypes.byref(rect))


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

    def get(self):
        """
        Retrieves all SDL events and returns them as Event objects.

        Returns:
            list[Event]: A list of Event objects.
        """
        sdl3.SDL_PumpEvents()
        event_list = []
        event_count = sdl3.SDL_PeepEvents(ctypes.byref(self.sdl_event), ctypes.sizeof(self.sdl_event), sdl3.SDL_GETEVENT, sdl3.SDL_EVENT_FIRST, sdl3.SDL_EVENT_LAST)

        for x in range(event_count):
            try:
                event_type = Event(self.sdl_event.type)
                event_list.append(event_type)
            except Exception:
                pass
        return event_list



class Key:
    def __init__(self):
        pass

    def get_pressed(self):
        return sdl3.SDL_GetKeyboardState(None)
    





def init():
    sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS | sdl3.SDL_INIT_AUDIO)

def quit():
    sdl3.SDL_DestroyRenderer(display.renderer)
    sdl3.SDL_DestroyWindow(display.window)
    sdl3.SDL_Quit()

display = Display()
event = Events()
draw = Draw()
key = Key()

RESIZABLE = sdl3.SDL_WINDOW_RESIZABLE
QUIT = 528
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