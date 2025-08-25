import pygame
from os.path import join 
from os import walk

WINDOW_WIDTH = 960 # 640
WINDOW_HEIGHT = 960 # 360

TILE_SIZE = 64 # Größe eines Tiles in Pixeln
##

# MAX_JUMP_POWER = 10
# JUMP_CHARGE_RATE = 20
# GRAVITY = 20
# PLAYER_SPEED = 250

GRAVITY = 2000         # Pixel pro Sekunde² – für realistisches Jump-Feeling
MAX_JUMP_POWER = 1000   # Initialgeschwindigkeit (Pixel pro Sekunde)
PLAYER_SPEED = 300     # Laufgeschwindigkeit (Pixel pro Sekunde)
JUMP_CHARGE_RATE = 1000  # Wie schnell Sprungkraft geladen wird (Pixel/s²)
