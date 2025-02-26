from __future__ import division

import ctypes
import os
import platform
import time as t

import psutil
import sdl3

from sdlg._display import _Display
from sdlg._draw import _Draw
from sdlg._key import _Key
from sdlg.event import _Events

p = psutil.Process(os.getpid())
p.cpu_affinity([0, 1])

startup_time = t.time()


_start_perf_count = None  # arbitrary frequency, see get_seconds
_perf_to_ms_divisor = None  # Fixed after SDL_Init


if platform.system() == "Windows":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)  # HIGH_PRIORITY_CLASS


# Can't be None, otherwise can't be imported by reference, so:
def perf_to_ms_divisor():
    return _perf_to_ms_divisor


def start_perf_count():
    return _start_perf_count


def init():
    global _start_perf_count
    global _perf_to_ms_divisor
    sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS | sdl3.SDL_INIT_AUDIO)
    _perf_to_ms_divisor = sdl3.SDL_GetPerformanceFrequency() / 1000
    _start_perf_count = sdl3.SDL_GetPerformanceCounter()


def quit():
    sdl3.SDL_DestroyRenderer(display.renderer)
    sdl3.SDL_DestroyWindow(display.window)
    sdl3.SDL_Quit()


display = _Display()
event = _Events()
draw = _Draw()
key = _Key()

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
