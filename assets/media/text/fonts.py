import os
import pygame


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to font files
FONT_PATH_BIG = os.path.join(BASE_DIR, "8-bit_wonder.ttf")
FONT_PATH_SMALL = os.path.join(BASE_DIR, "retro_gaming.ttf")

def get_big_font(size=36):
    return pygame.font.Font(FONT_PATH_BIG, size)

def get_small_font(size=24):
    return pygame.font.Font(FONT_PATH_SMALL, size)
