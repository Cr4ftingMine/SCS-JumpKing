from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # self.image.fill("red")  # sichtbar zum Debuggen
        # self.image.set_alpha(0)  # unsichtbar im Spiel
        self.rect = self.image.get_frect(topleft=pos)


class SlopeSprite(pygame.sprite.Sprite):
    def __init__(self,pos, image: pygame.Surface, *groups):
        super().__init__(*groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)
        self.heights = self.build_heightmap_from_alpha(self.image)
        

    def build_heightmap_from_alpha(self, surf: pygame.Surface):
        w, h = surf.get_size()
        alpha = pygame.surfarray.pixels_alpha(surf)
        heights = [h] * w
        for x in range(w):
            col = alpha[x]
            for y in range(h):
                if col[y] > 0:
                    heights[x] = y 
                    break
        del alpha
        return heights
    
    def y_on(self, x_world):
        x_local = int(max(0, min(self.rect.w - 1, x_world - self.rect.left)))
        y_local = self.heights[x_local]
        return self.rect.top + y_local
