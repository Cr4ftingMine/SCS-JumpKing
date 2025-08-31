# Game Class - Extended Version of Jump King 
# Was main.py but was changed to game.py due to the addition of a menu
from settings import *
from player import Player
from tiledmap import TiledMap
from sprites import CollisionSprite
from camera import Camera
from ui import UI

class Game: 
    def __init__(self, display_surface, level_path=None, enable_extensions=True):
        self.display_surface = display_surface 
        self.level_path = level_path
        self.enable_extensions = enable_extensions

        # Game surface
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Clock
        self.clock = pygame.time.Clock() 

        # Running Variable
        self.running = True

        # Load Tiled Map
        self.map = TiledMap(self.level_path)

        # Camera
        self.camera = Camera(self.map.height)

        # All Sprites
        self.all_sprites = pygame.sprite.Group()

        # Player I
        self.player = Player(collision_sprites=self.map.collision_sprites, slope_sprites=self.map.slope_sprites, slippery_sprites=self.map.slippery_sprites, actionblock_sprites=self.map.actionblock_sprites)

        # UI
        #self.ui = UI(self.display_surface, self.player, self.map)
        self.ui = UI(self.game_surface, self.player, self.map)

        # Items
        for item in self.map.item_sprites:
            self.all_sprites.add(item)

        # Checkpoint
        for checkpoint in self.map.checkpoint_sprites:
            self.all_sprites.add(checkpoint)

        # Action Block
        for action_block in self.map.actionblock_sprites:
            self.all_sprites.add(action_block)
        
        # Player II
        self.all_sprites.add(self.player) #!TODO: Platzänderung wegen Zeichenreichenfolge

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
            self.game_surface.fill((255, 255, 255))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pass # Open ingame menu
                else: self.player.event_handler(event)
            
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

            #self.map.draw(self.display_surface, self.camera)
            self.map.draw(self.game_surface, self.camera)

            for spr in self.all_sprites:
                offset_rect = spr.rect.move(0, self.camera.offset.y)
                #self.display_surface.blit(spr.image, offset_rect)
                self.game_surface.blit(spr.image, offset_rect)

                if isinstance(spr, Player):
                    #spr.draw_charge_bar(self.display_surface, self.camera)
                    spr.draw_charge_bar(self.game_surface, self.camera)
            
            self.debug_draw_grid()

            self.ui.draw()

            ######
            sw, sh = self.display_surface.get_size()
            x = (sw - WINDOW_WIDTH) // 2
            y = (sh - WINDOW_HEIGHT) // 2
            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.game_surface, (x,y))
            ######

            pygame.display.flip()
        
        #pygame.quit() # Pygame instance getting closed


# if __name__ == "__main__":
#     game = Game() 
#     game.run()