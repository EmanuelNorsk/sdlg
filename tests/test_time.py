import time as t

import pytest
import sdl3

from sdlg.time import get_ticks, get_seconds, Clock
from sdlg import _start_perf_count, _perf_to_ms_divisor

def test_get_ticks():
    if _start_perf_count is None:
        assert get_ticks() == 0
    else:
        assert isinstance(get_ticks(), float)
        assert get_ticks() >= 0

def test_get_seconds():
    if _start_perf_count is None:
        assert get_seconds() == 0
    else:
        assert isinstance(get_seconds(), float)
        assert get_seconds() >= 0

def test_clock_initialization():
    clock = Clock()
    assert clock.delta == 0  # NOTE: is an int before tick
    clock.tick()
    assert isinstance(clock.time, int)
    assert isinstance(clock.last_time, int)
    assert isinstance(clock.freq, int)
    assert isinstance(clock.delta, float)
    assert clock.maxFPS == -1
    assert clock.elapsed == 0
    assert clock.draw == 1

def test_clock_tick():
    clock = Clock()
    t.sleep(.1)
    clock.tick()
    assert isinstance(clock.delta, float)
    assert clock.delta >= 0, "delta is {} but should be positive".format(clock.delta)

def test_clock_get_fps():
    clock = Clock()
    fps = clock.get_fps()
    assert isinstance(fps, int)
    assert fps > 0
