import time as t
import sdl3

class Clock:
    def __init__(self):
        self.time = sdl3.SDL_GetPerformanceCounter()
        self.last_time = sdl3.SDL_GetPerformanceCounter()

        self.freq = sdl3.SDL_GetPerformanceFrequency()


    def tick(self):
        self.last_time = self.time


    def get_fps(self):
        self.time = sdl3.SDL_GetPerformanceCounter()
        return round(1 / ((self.time - self.last_time) / self.freq))

        
 