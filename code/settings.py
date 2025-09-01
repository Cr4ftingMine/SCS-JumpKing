import pygame
import json
from os.path import join, splitext, basename, dirname
from os import walk, listdir
import os
import sys

WINDOW_WIDTH = 960 # 640
WINDOW_HEIGHT = 960 # 360

TILE_SIZE = 64 # Größe eines Tiles in Pixeln
##

# MAX_JUMP_POWER = 10
# JUMP_CHARGE_RATE = 20
# GRAVITY = 20
# PLAYER_SPEED = 250

GRAVITY = 2000         # Pixel pro Sekunde² – für realistisches Jump-Feeling
MAX_JUMP_POWER = 1100   # Initialgeschwindigkeit (Pixel pro Sekunde) # 1000
PLAYER_SPEED = 300     # Laufgeschwindigkeit (Pixel pro Sekunde)
JUMP_CHARGE_RATE = 1000  # Wie schnell Sprungkraft geladen wird (Pixel/s²)

SLIDE_SPEED = 200 # Rutschgeschwindigkeit auf der Rampe
ICE_SPEED = 150 # Geschwindigkeit auf Eis
ICE_SPEED_DRAG = 5.0 # Geschwindigkeitsreduktion beim Rutschen


# DRAW
PANEL_MARGIN = 60
BUTTON_WIDTH, BUTTON_HEIGHT = 420, 70
BUTTON_GAP = 90

LEVEL_ROW_H = 44
LEVEL_COL_GAP = 280

# Starcoin
TOTAL_STARCOIN = 3

# Custom events
GAME_WON = pygame.event.custom_type()

# Win Screen
WINSCREEN_DURATION_MS = 4000

# Score json
DATA_DIR = join(dirname(__file__), "../data")
SCORE_FILE = join(DATA_DIR, "scores.json")