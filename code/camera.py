from settings import *

class Camera: 
    def __init__(self, world_h):
        self.offset = pygame.Vector2(0,0)
        self.world_h = world_h
        self._screen_top = 0 # Screen-Ancor (World-Y of upper Windowborder)

    def update(self, target_rect):
        # self.offset.y = -(target_rect.centery - WINDOW_HEIGHT // 2)
        # self.offset.y = min(0, self.offset.y)
        # self.offset.y = max(-(self.world_h - WINDOW_HEIGHT), self.offset.y)

        # screen_index = int(target_rect.centery // WINDOW_HEIGHT)
        # screen_top = screen_index * WINDOW_HEIGHT

        # if screen_top < 0:
        #     screen_top = 0
        # max_top = max(0, self.world_h - WINDOW_HEIGHT)
        # if screen_top > max_top:
        #     screen_top = max_top
        
        # self._screen_top = screen_top
        # self.offset.y = -self.screen_top

        screen_index = int(target_rect.centery // WINDOW_HEIGHT)
        screen_top = screen_index * WINDOW_HEIGHT

        max_top = self.world_h - WINDOW_HEIGHT
        if screen_top > max_top:
            screen_top = max_top

        self._screen_top = screen_top
        self.offset.y = -self._screen_top