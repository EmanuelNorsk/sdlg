from __future__ import division
import ctypes

import numpy as np
# import time as t
import sdl3

from sdlg import (
    perf_to_ms_divisor,
    start_perf_count,
)



def get_ticks():
    """Get the number of milliseconds since init.
    0 until init is called."""
    if start_perf_count() is None:
        return 0  # 0 until init as per Pygame
    return (sdl3.SDL_GetPerformanceCounter() - start_perf_count()) / perf_to_ms_divisor()


def get_seconds():
    """Get the number of seconds since init.
    0 until init is called.

    (sdlg-specific)
    """
    if start_perf_count() is None:
        return 0  # 0 until init as per Pygame
    return (sdl3.SDL_GetPerformanceCounter() - start_perf_count()) / sdl3.SDL_GetPerformanceFrequency()


class Clock:
    def __init__(self):
        self._first = sdl3.SDL_GetPerformanceCounter()
        self.last_time = sdl3.SDL_GetPerformanceCounter()
        self.time = sdl3.SDL_GetPerformanceCounter()
        self.freq = sdl3.SDL_GetPerformanceFrequency()
        self._to_ns_div = int(self.freq // 1_000_000_000)
        self._to_ms_div = int(self.freq // 1_000)
        self.delta = 0
        self.maxFPS = -1
        # self.elapsed = 0
        self.draw = 1

        self._deltas = np.zeros(10, dtype=float)
        self._delta_count = 0
        self._delta_idx = 0

    def tick(self, framerate = -1):
        """Return the number of milliseconds
        that passed since the last call."""
        if framerate > 0:
            self.maxFPS = framerate
        self.time = sdl3.SDL_GetPerformanceCounter()
        self.delta = ((self.time - self.last_time) / self.freq)
        if self.maxFPS > 0:
            if self.delta < (1 / self.maxFPS):
                delta_ns = int(self.time - self.last_time) // self._to_ns_div
                ns_per_frame = int(1_000_000_000 // framerate)
                delay_ns = int(ns_per_frame - delta_ns)
                sdl3.SDL_DelayPrecise(delay_ns)
                print("delay={}".format(delay_ns))
                self.time = sdl3.SDL_GetPerformanceCounter()
                self.delta = ((self.time - self.last_time) / self.freq)
                # self.elapsed += self.delta
                self.draw = 1
            else:
                # self.elapsed -= (1 / self.maxFPS)
                self.draw = 0
        self._deltas[self._delta_idx] = self.delta
        self._delta_idx += 1
        if self._delta_idx >= len(self._deltas):
            self._delta_idx = 0
        if self._delta_count < len(self._deltas):
            self._delta_count += 1
        ms = (self.time - self.last_time) // self._to_ms_div
        self.last_time = self.time
        return ms  # ms as per Pygame

    def get_fps(self):
        """Get average frames per second
        based on last 10 calls to tick."""
        if self._delta_count < 1:
            return 0
        total = 0
        for i in range(self._delta_count):
            total += self._deltas[i]
        average_delta = total / self._delta_count
        return 1.0 / average_delta
