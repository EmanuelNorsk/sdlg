import ctypes
import sdl3



class SDL_FPoint(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("x", ctypes.c_float), ("y", ctypes.c_float)]

class SDL_Color(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("r", ctypes.c_uint8),
        ("g", ctypes.c_uint8),
        ("b", ctypes.c_uint8),
        ("a", ctypes.c_uint8),
    ]

class SDL_Vertex(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("position", SDL_FPoint),  # 8 bytes
        ("color", SDL_Color),      # 4 bytes
        ("tex_coord", SDL_FPoint)  # 8 bytes
    ]

print("SDL_Vertex size:", ctypes.sizeof(SDL_Vertex))  # Should print 16
print("Offsets:")
for field_name, field_type in SDL_Vertex._fields_:
    print(f"{field_name}: {getattr(SDL_Vertex, field_name).offset}")