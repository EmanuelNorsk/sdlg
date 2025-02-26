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
    """Measure time
    Stores in platform-specific performance counter tick
    called "cycle" in this code to distinguish from
    ms (Pygame-like millisecond tick).

    Attributes:
    _cycle: Current time in platform-specific increments
    _freq: platform-specific increments per second
    draw: (sdlg-specific) 1 of tick delayed, 0 if it did not.
    """
    def __init__(self):
        self._first_cycles = sdl3.SDL_GetPerformanceCounter()
        self._last_cycles = sdl3.SDL_GetPerformanceCounter()
        self._cycle = sdl3.SDL_GetPerformanceCounter()
        self._freq = sdl3.SDL_GetPerformanceFrequency()
        self._to_ns_div = int(self._freq // 1_000_000_000)
        self._to_ns_fac = 1_000_000_000 / self._freq
        if self._to_ns_div == 0:
            # Prevent divide by zero in case of coarse frequency
            self._to_ns_div = None
            self._to_ns_fac = 1_000_000_000 // self._freq
        # else default to clean integer division.
        self._to_ms_div = int(self._freq // 1_000)
        assert self._to_ms_div > 0, "NotImplementedError: _to_ms_fac for course platform timer"
        self._max_fps = -1
        self._elapsed_cycles = 0
        self._paused_cycles = 0
        self.draw = 1

        self._deltas = np.zeros(10, dtype=float)
        self._delta_count = 0
        self._delta_idx = 0
        self._raw_delta_cycles = 0
        self._delta_cycles = 0

    def tick(self, framerate = -1):
        """Return the number of milliseconds
        that passed since the last call."""
        if framerate > 0:
            self._max_fps = framerate
        self._cycle = sdl3.SDL_GetPerformanceCounter()
        self._delta_cycles = self._cycle - self._last_cycles
        self._raw_delta_cycles = self._delta_cycles
        cycles_per_frame = int(self._freq // framerate)
        if self._max_fps > 0:
            if self._raw_delta_cycles < cycles_per_frame:
                delay_cycles = int(cycles_per_frame - self._raw_delta_cycles)
                if self._to_ns_div:
                    delay_ns = delay_cycles // self._to_ns_div
                else:
                    delay_ns = int(delay_cycles * self._to_ns_fac)
                sdl3.SDL_DelayPrecise(delay_ns)
                self._cycle = sdl3.SDL_GetPerformanceCounter()
                self._delta_cycles = self._raw_delta_cycles + delay_cycles
                self.draw = 1
            else:
                self.draw = 0
        self._elapsed_cycles += self._delta_cycles
        self._deltas[self._delta_idx] = self._delta_cycles
        self._delta_idx += 1
        if self._delta_idx >= len(self._deltas):
            self._delta_idx = 0
        if self._delta_count < len(self._deltas):
            self._delta_count += 1
        ms = (self._raw_delta_cycles) // self._to_ms_div
        self._last_cycles = self._cycle
        return ms  # ms as per Pygame

    def get_raw(self):
        """Get number of ms passed since started *not* including
        seconds waited during tick with framerate set
        """
        return self._raw_delta_cycles // self._to_ms_div

    def get_fps(self):
        """Get average frames per second
        based on last 10 calls to tick."""
        if self._delta_count < 1:
            return 0
        total = 0
        for i in range(self._delta_count):
            total += self._deltas[i] / self._freq
        average_delta = total / self._delta_count
        return 1.0 / average_delta

    def get_raw_seconds(self):
        """Get number of seconds passed since started *not* including
        seconds waited during tick with framerate set

        (sdlg-specific)
        """
        return self._raw_delta_cycles / self._freq

    def get_seconds(self):
        """Get number of seconds passed since started including
        seconds waited during tick with framerate set

        (sdlg-specific)
        """
        return self._delta_cycles / self._freq

    def elapsed_seconds(self):
        """Get all time elapsed since started, in seconds.

        (sdlg-specific)
        """
        return self._elapsed_cycles / self._freq
