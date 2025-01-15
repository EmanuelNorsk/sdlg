import time as t

class Clock:
    def __init__(self):
        self.time = t.perf_counter()
        self.last_time = self.time
        self.delta = 0.0

    def tick(self):
        self.last_time = self.time
        self.time = t.perf_counter()
        self.delta = (self.time - self.last_time)


    def get_fps(self):
        fps = round(1 / (self.time - self.last_time))
        return fps
        
 