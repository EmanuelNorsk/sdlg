from sdlg import (
    init,
    display,
    RESIZABLE,
    t,
    event,
    QUIT,
    draw,
    key,
    K_w,
)

init()
Screen = display.set_mode((640, 480), RESIZABLE)
started = t.perf_counter()
running = True

fps = 0
fps_per_second = 0
last_fps_per_second = t.perf_counter()

while running:

    for e in event.get():
        if e.type == QUIT:
            running = False

    Screen.fill((255,255,255,255))
    draw.rect(Screen, (0,0,0,255), (100, 100, 100, 100))


    fps += 1
    if last_fps_per_second + 1 <= t.perf_counter():
        last_fps_per_second += 1
        fps_per_second = fps
        fps = 0
        print(f"FPS: {fps_per_second}")

    keys = key.get_pressed()
    if keys[K_w]:
        print("Key W Pressed!")

    display.update()

quit()