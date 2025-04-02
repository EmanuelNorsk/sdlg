import sdlg
import sdl3
import ctypes
import pygame


def Font(fileArg: str, size: int):
    return sdlg.Font(fileArg, size, "Font")

def SysFont(name: str, size: int):
    return sdlg.Font(name, size, "SysFont")
    
