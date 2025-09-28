from settings import *

class Camera: 
    def __init__(self, world_h):
        self.offset = pygame.Vector2(0,0)
        self.world_h = world_h
        self._screen_top = 0 # Screen-Ancor (World-Y of upper Windowborder)

    def update(self, target_rect):
        screen_index = int(target_rect.centery // WINDOW_HEIGHT)
        screen_top = screen_index * WINDOW_HEIGHT

        max_top = self.world_h - WINDOW_HEIGHT
        if screen_top > max_top:
            screen_top = max_top

        self._screen_top = screen_top
        self.offset.y = -self._screen_top