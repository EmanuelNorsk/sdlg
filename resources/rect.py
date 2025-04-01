import sdl3, ctypes

class Rect:
    def __init__(self, x, y, width, height):
        super().__setattr__("x", x)
        super().__setattr__("y", y)
        super().__setattr__("width", width)
        super().__setattr__("height", height)
        super().__setattr__("frect", (0, 0))
        self.getFrect()
        self.updateExtra()

    def getFrect(self):
        super().__setattr__("frect", sdl3.SDL_FRect(ctypes.c_float(self.x), ctypes.c_float(self.y), ctypes.c_float(self.width), ctypes.c_float(self.height)))


    def updateBase(self, type):
        if type == "center":
            super().__setattr__("x", self.center[0] - self.width / 2)
            super().__setattr__("y", self.center[1] - self.height / 2)
        elif type == "topleft":
            super().__setattr__("x", self.topleft[0])
            super().__setattr__("y", self.topleft[1])
        elif type == "topright":
            super().__setattr__("x", self.topright[0])
            super().__setattr__("y", self.topright[1])
            super().__setattr__("x", self.x - self.width)
        elif type == "bottomleft":
            super().__setattr__("x", self.bottomleft[0])
            super().__setattr__("y", self.bottomleft[1])
            super().__setattr__("y", self.y - self.height)
        elif type == "bottomright":
            super().__setattr__("x", self.bottomright[0])
            super().__setattr__("y", self.bottomright[1])
            super().__setattr__("x", self.x - self.width)
            super().__setattr__("y", self.y - self.height)
    
    def updateExtra(self):
        super().__setattr__("centerx", self.x + self.width / 2)
        super().__setattr__("centery", self.y + self.height / 2)
        super().__setattr__("center", (self.centerx, self.centery))
        super().__setattr__("topleft", (self.x, self.y))
        super().__setattr__("topright", (self.x + self.width, self.y))
        super().__setattr__("bottomleft", (self.x, self.y + self.height))
        super().__setattr__("bottomright", (self.x + self.width, self.y + self.height))


    def __str__(self):
        return f"{[self.x, self.y, self.width, self.height]}"
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        
        if name in ["centerx", "centery"]:
            super().__setattr__("center", (self.centerx, self.centery))
            self.updateBase("center")
        elif name in ["topleft", "topright", "bottomleft", "bottomright"]:
            self.updateBase(name)

        self.updateExtra()
        self.getFrect()

