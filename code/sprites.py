from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill("red")  # sichtbar zum Debuggen
        self.image.set_alpha(0)  # unsichtbar im Spiel
        self.rect = self.image.get_frect(topleft=pos)
