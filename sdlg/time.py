from __future__ import division

# import time as t
import sdl3

from sdlg import (
    _perf_to_ms_divisor,
    _start_perf_count,
)


def get_ticks():
    if _start_perf_count is None:
        return 0  # 0 until init as per Pygame
    return (sdl3.SDL_GetPerformanceCounter() - _start_perf_count) / _perf_to_ms_divisor


def get_seconds():
    if _start_perf_count is None:
        return 0  # 0 until init as per Pygame
    return (sdl3.SDL_GetPerformanceCounter() - _start_perf_count) / sdl3.SDL_GetPerformanceFrequency()


class Clock:
    def __init__(self):
        self.last_time = sdl3.SDL_GetPerformanceCounter()
        self.time = sdl3.SDL_GetPerformanceCounter()
        self.freq = sdl3.SDL_GetPerformanceFrequency()
        self.delta = 0
        self.maxFPS = -1
        self.elapsed = 0
        self.draw = 1

    def tick(self, cap = -1):
        if cap > 0:
            self.maxFPS = cap
        self.delta = ((self.time - self.last_time) / self.freq)
        if self.maxFPS > 0:
            if self.elapsed <= (1 / self.maxFPS):
                self.elapsed += self.delta
                self.draw = 1
            else:
                self.elapsed -= (1 / self.maxFPS)
                self.draw = 0

        # self.last_time = self.time

    def get_fps(self):
        self.last_time = self.time
        self.time = sdl3.SDL_GetPerformanceCounter()
        return round(1 / ((self.time - self.last_time) / self.freq))
