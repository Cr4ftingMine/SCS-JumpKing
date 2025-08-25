# Game Class - Extended Version of Jump King 
from settings import *
from player import Player
from tiledmap import TiledMap
from sprites import CollisionSprite

class Game: 
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Extended Jump King")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load Tiled Map
        self.map = TiledMap("data/Map/unbenannt.tmx")

        #Sprites 
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(collision_sprites=self.map.collision_sprites)
        self.all_sprites.add(self.player)

        

    def load_images(self):
        pass
    
    def input(self):
        pass

    def setup(self):
        pass

    def debug_draw_grid(self):
        for x in range(0, WINDOW_WIDTH, 64):
            pygame.draw.line(self.display_surface, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 64):
            pygame.draw.line(self.display_surface, (50, 50, 50), (0, y), (WINDOW_WIDTH, y))

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000 # delta time

            self.display_surface.fill((255, 255, 255))
            self.map.draw(self.display_surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # TODO: Eventhandling sollte glaube eher im Player-Objekt sein
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.player.release_jump()

            self.all_sprites.update(dt) # Update all sprites
            self.all_sprites.draw(self.display_surface)
            self.debug_draw_grid()
            pygame.display.update()  # Update the display

        pygame.quit()


if __name__ == "__main__":
    game = Game() 
    game.run()