import pytest
import sdl3
import time
from sdlg.event import Event, _Events

def setup_module(module):
    sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO | sdl3.SDL_INIT_EVENTS | sdl3.SDL_INIT_AUDIO)

def teardown_module(module):
    sdl3.SDL_Quit()

def test_event_initialization():
    event = Event(sdl3.SDL_EVENT_QUIT)
    assert event.type == sdl3.SDL_EVENT_QUIT

def test_events_initialization():
    events = _Events()
    assert isinstance(events.sdl_event, sdl3.SDL_Event)
    assert isinstance(events.started, float)
    assert events.started > time.time() - 1

def test_get_events():
    events = _Events()
    event_list = events.get()
    assert isinstance(event_list, list)
    for event in event_list:
        assert isinstance(event, Event)
        assert isinstance(event.type, int)
