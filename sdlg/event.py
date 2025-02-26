import time as t

import sdl3


class Event:
    def __init__(self, type):
        self.type = type


class _Events:
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
