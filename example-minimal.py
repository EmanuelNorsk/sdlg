import sdlg
import time as t

sdlg.init()
Screen = sdlg.display.set_mode((640, 480), sdlg.RESIZABLE)
started = t.perf_counter()
running = True

fps = 0
fps_per_second = 0
last_fps_per_second = t.perf_counter()

while running:

    for e in sdlg.event.get():
        if e.type == sdlg.QUIT:
            running = False

    Screen.fill((255,255,255,255))
    sdlg.draw.rect(Screen, (0,0,0,255), (100, 100, 100, 100))

    fps += 1
    if last_fps_per_second + 1 <= t.perf_counter():
        last_fps_per_second += 1
        fps_per_second = fps
        fps = 0
        print(f"FPS: {fps_per_second}")

    keys = sdlg.key.get_pressed()
    if keys[sdlg.K_w]:
        print("Key W Pressed!")

    sdlg.display.update()

quit()
