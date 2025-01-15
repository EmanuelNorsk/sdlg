# SDLG
A pure python written library built on top of PySDL3 to create programs and games. It has the exact same syntax/api design as pygame, and is mainly created for the flexibility you get with SDL3. Additional features will be created as well. This is only a basic and minimal version of what it will become.

This document was written in version v0.0.1

-------------------------------------------












Functions added to the current version:

### Creates a screen to draw on with the width and height of your choice. Current flags that work are: sdlg.RESIZABLE
sdlg.display.set_mode(Tuple(width, height), flags) -> Display

# Fills the window with a color. Color values are between 0 - 255
Display.fill((red, green, blue, alpha)) 

# Both does the same thing, updates the Display
Display.flip()
Display.update()

# Makes (0, 0) be in the center of the screen and centers each elements drawn to the screen.
Display.cartesian_coordinate_system(Bool)

# Adds the feature to scale the window to match the new resolution to keep everything looking the same and changing at the right pace
Display.scaleWindow(Bool)

# Sets the inner size to what you want. This impacts how things scale and if you want things to scale based on a window size not running at the moment of launching Display.scaleWindow(True)
Display.setInnerSize(Tuple(width, height))

# Draws a rectangle to the screen with the properties given. Border might not work just yet, and it does not support scaling yet.
sdlg.draw.rect(Display, (red, green, blue, alpha), (x, y, width, height), borderWidth = 0) 

# Generates a list of events. Use this in a for loop and ask for the current event's type. So [event.type for event in sdlg.event.get()] to get a list of events.
sdlg.event.get()

# Gives a list with the keyboard state
sdlg.key.get_pressed()

# Starts up the library
sdlg.init()

# Closes the library
sdlg.quit()

Every constant are exactly the same as pygame.
pygame.RESIZABLE == sdlg.RESIZABLE
pygame.QUIT == sdlg.QUIT
pygame.VIDEORESIZE == sdlg.VIDEORESIZE

Every key is also the same:
pygame.K_a == sdlg.K_a

Most of the keys are added and only the events above are added.
More features are in early testing and will not be described in this document.
Go see the example page if you want to see a actual project.
