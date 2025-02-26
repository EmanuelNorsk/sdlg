import time as t

import pytest
import sdl3

import sdlg
from sdlg.time import get_ticks, get_seconds, Clock
from sdlg import _start_perf_count, _perf_to_ms_divisor, start_perf_count

sdlg.init()  # sets _perf_to_ms_divisor etc


def test_get_ticks():
    if start_perf_count() is None:
        assert get_ticks() == 0
    else:
        assert isinstance(get_ticks(), float)
        assert get_ticks() >= 0

def test_get_seconds():
    if start_perf_count() is None:
        assert get_seconds() == 0
    else:
        t.sleep(.1)
        assert isinstance(get_seconds(), float)
        assert get_seconds() >= 0

def test_clock_initialization():
    clock = Clock()
    assert clock.get_seconds() == 0  # NOTE: May be an int before tick
    clock.tick()
    assert isinstance(clock._cycle, int)
    assert isinstance(clock._last_cycles, int)
    assert isinstance(clock._freq, int)
    assert isinstance(clock.get_seconds(), float)
    assert clock._max_fps == -1
    # assert clock.elapsed == 0
    assert clock.draw == 1

def test_clock_tick():
    clock = Clock()
    t.sleep(.1)
    clock.tick()
    assert isinstance(clock.get_seconds(), float)
    assert clock.get_seconds() >= 0, "delta is {} but should be positive".format(clock.get_seconds())

def test_clock_tick_framerate():
    clock = Clock()
    for i in range(11):
        clock.tick(60)
        clock.tick(60)
        clock.tick(60)
        clock.tick(60)
        clock.tick(60)
    fps = clock.get_fps()
    assert fps > 30
    assert fps < 120

def test_clock_get_fps():
    clock = Clock()
    for i in range(11):
        t.sleep(1/60)
        clock.tick()
    fps = clock.get_fps()
    # assert isinstance(fps, int)
    assert fps > 0
    assert fps > 30
    assert fps < 120


test_clock_initialization()