# Game Class - Extended Version of Jump King 
from settings import *
from player import Player
from tiledmap import TiledMap
from sprites import CollisionSprite
from camera import Camera
from ui import UI

class Game: 
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Extended Jump King")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load Tiled Map
        self.map = TiledMap("data/Map/unbenannt.tmx")

        # Camera
        self.camera = Camera(self.map.height)

        # Sprites 
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(collision_sprites=self.map.collision_sprites, slope_sprites=self.map.slope_sprites, slippery_sprites=self.map.slippery_sprites, actionblock_sprites=self.map.actionblock_sprites)
        #self.all_sprites.add(self.player)

        # UI
        self.ui = UI(self.display_surface, self.player, self.map)

        # Items
        for item in self.map.item_sprites:
            self.all_sprites.add(item)

        # Checkpoint
        for checkpoint in self.map.checkpoint_sprites:
            self.all_sprites.add(checkpoint)
        
        # Action Block
        for action_block in self.map.actionblock_sprites:
            self.all_sprites.add(action_block)

        self.all_sprites.add(self.player) #!TODO: Platzänderung wegen Zeichenreichenfolge

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
            dt = min(dt, 0.05) # limit dt to max 50ms (avoid big physics jumps when window is dragged or game lags)

            self.display_surface.fill((255, 255, 255))
            #self.map.draw(self.display_surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else: 
                    self.player.event_handler(event) 

            self.all_sprites.update(dt) # Update all sprites
            self.camera.update(self.player.rect)

            # Items
            item_hits = pygame.sprite.spritecollide(self.player, self.map.item_sprites, dokill=True)
            for item in item_hits:
                if hasattr(item, "on_pickup"):
                    item.on_pickup(self.player)

            # Checkpoints
            checkpoint_hits = pygame.sprite.spritecollide(self.player, self.map.checkpoint_sprites, dokill=False)
            for checkpoint in checkpoint_hits:
                print("kollision checkpoint")
                checkpoint.set_active()
                self.player.last_checkpoint = checkpoint



            self.map.draw(self.display_surface, self.camera)
            
            for spr in self.all_sprites:
                offset_rect = spr.rect.move(0, self.camera.offset.y)
                self.display_surface.blit(spr.image, offset_rect)

                if isinstance(spr, Player):
                    spr.draw_charge_bar(self.display_surface, self.camera)

            #self.all_sprites.draw(self.display_surface)

            self.debug_draw_grid()

            self.ui.draw()
            #print(f"Velocity x: {self.player.velocity_x}, Velocity y: {self.player.velocity_y}")
            #pygame.display.update()  # Update the display
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game() 
    game.run()