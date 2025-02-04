import time as t
import sdl3

class Clock:
    def __init__(self):
        self.time = sdl3.SDL_GetPerformanceCounter()
        self.last_time = sdl3.SDL_GetPerformanceCounter()
        self.delta = 0
        self.maxFPS = -1
        self.elapsed = 0
        self.draw = 1
        self.freq = sdl3.SDL_GetPerformanceFrequency()


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


        self.last_time = self.time


    def get_fps(self):
        self.time = sdl3.SDL_GetPerformanceCounter()
        return round(1 / ((self.time - self.last_time) / self.freq))

        
 