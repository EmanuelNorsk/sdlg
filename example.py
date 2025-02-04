import sdlg
#import pygame as sdlg
import time as t
import random

import colorsys

def rainbow(time, speed, opacity = 255):
    ti = ((time * speed) % 1)
    colors = colorsys.hsv_to_rgb(ti, 1, 1)
    return (int(colors[0] * 255), int(colors[1] * 255), int(colors[2] * 255), opacity)



Clock = sdlg.time.Clock()

class Player:
    def __init__(self, rect=(0, 0, 0, 0), color=(0, 0, 0, 0), borderWidth=0):
        # rect=(x, y, w, h)
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = color
        self.borderWidth = borderWidth


        self.keyboard = False
        self.speed = 640
    def draw(self):
        global Screen
        sdlg.draw.rect(Screen, self.color, (self.x, self.y, self.width, self.height), self.borderWidth)
        return None

    def attachKeyboard(self):
        self.keyboard = True

    def main(self):
        global FramesPerSecond
        keys = sdlg.key.get_pressed()
        if keys[sdlg.K_w]:
            self.y += self.speed * Clock.delta
        if keys[sdlg.K_a]:
            self.x -= self.speed * Clock.delta
        if keys[sdlg.K_s]:
            self.y -= self.speed * Clock.delta
        if keys[sdlg.K_d]:
            self.x += self.speed * Clock.delta
        #self.color = rainbow(t.time(), 0.2, 255)


Sprites = []
Player1 = Player((0, 0, 200, 200), (100, 100, 100, 255), 20)
Player1.attachKeyboard()

Sprites.append(Player1)

sdlg.init()
Screen = sdlg.display.set_mode((640, 360), sdlg.RESIZABLE)
Screen.cartesian_coordinate_system(True)
Screen.scaleWindow(True)
Screen.setInnerSize((1280, 720))
started = t.perf_counter()
running = True
FramesPerSecond = 0


starting_time = t.time()

fps = 0
fps_per_second = 0
last_fps_per_second = t.perf_counter()


def loop():
    global running
    while running:
        Clock.tick()


        for e in sdlg.event.get():
            if e.type == sdlg.QUIT: # QUIT
                running = False
        
        Screen.fill((255,255,255,255))


        for sprite in Sprites:
            sprite: Player
            sprite.main()
            sprite.draw()




        print(f"FPS: {Clock.get_fps()}")
        #print(Screen.get_fps())
        sdlg.display.update()

import cProfile
cProfile.run('loop()', filename='profile_results.prof')

if __name__ == "__main__":
    loop()



sdlg.quit()



# Same syntax
# Added features
# Clock.delta - gives you a fps factor of 1 / fps. Add it to changes happening every frame to get a similar effect to capping events to a timer
# Screen.cartesian_coordinate_system( True / False ) - Give you a coordinate system where (0, 0) is in the center of the screen, where x goes from left to right and y goes from down to up.
# Screen.scaleWindow( True / False ) - Makes the screen scale with the window size, meaning it will look the exact same, but just bigger or smaller.
# Screen.setInnerSize(Tuple(width, height)) - Set's the internal size of the window. It is a reference to how much the screen should scale. Does nothing if Screen.scaleWindow is set to False.
