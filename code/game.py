# Game Class - Extended Version of Jump King 
# Was main.py but was changed to game.py due to the addition of a menu
from settings import *
from player import Player
from tiledmap import TiledMap
from sprites import *
from camera import Camera
from ui import UI
from ingame_menu import ingameMenu
from winscreen import WinScreen

class Game: 
    def __init__(self, display_surface, level_path=None, enable_extensions=True):
        self.display_surface = display_surface 
        self.level_path = level_path
        self.enable_extensions = enable_extensions

        # Ingame menu
        self.show_ingame_menu = False
        self.ingame_menu = ingameMenu(self.display_surface)

        # Game surface
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Win Screen
        self.winscreen = WinScreen(self.display_surface)
        self.show_winscreen = False

        # Clock
        self.clock = pygame.time.Clock() 

        # Level-Timer
        self.level_time = 0.0 # elapsed time in seconds

        # Running Variable
        self.running = True

        # Load Tiled Map
        self.map = TiledMap(self.level_path, self.enable_extensions)

        # Camera
        self.camera = Camera(self.map.height)

        # All Sprites
        self.all_sprites = pygame.sprite.Group()

        # Player I
        self.player = Player(collision_sprites=self.map.collision_sprites, slope_sprites=self.map.slope_sprites, slippery_sprites=self.map.slippery_sprites, actionblock_sprites=self.map.actionblock_sprites)

        # UI
        #self.ui = UI(self.display_surface, self.player, self.enable_extensions)
        self.ui = UI(self.game_surface, self.player, self.enable_extensions)

        # Items
        for item in self.map.item_sprites:
            self.all_sprites.add(item)

        # Checkpoint
        for checkpoint in self.map.checkpoint_sprites:
            self.all_sprites.add(checkpoint)

        # Action Block
        for action_block in self.map.actionblock_sprites:
            self.all_sprites.add(action_block)

        # Star Coin
        for starcoin in self.map.starcoin_sprites:
            self.all_sprites.add(starcoin)
        
        
        # Player II
        self.all_sprites.add(self.player) #!TODO: Platzänderung wegen Zeichenreichenfolge

        # Sounds
        self.starcoin_sound = pygame.mixer.Sound(join("audio", "starcoin.wav"))
        self.starcoin_sound.set_volume(0.008)
        self.item_pickup_sound = pygame.mixer.Sound(join("audio", "item_pickup.wav"))
        self.item_pickup_sound.set_volume(0.008)
        self.checkpoint_sound = None
        

    def debug_draw_grid(self):
        for x in range(0, WINDOW_WIDTH, 64):
            pygame.draw.line(self.display_surface, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 64):
            pygame.draw.line(self.display_surface, (50, 50, 50), (0, y), (WINDOW_WIDTH, y))

    def save_score(self):
        os.makedirs(dirname(SCORE_FILE), exist_ok=True) # Ensure the directory for the score file exists 

        # Load existing scores
        data = {}
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        
        level_name = splitext(basename(self.level_path))[0] if self.level_path else "unknown"

        # Keep level highscore 
        prev = int(data.get(level_name, 0))
        best = max(prev, int(self.player.star_coins))
        data[level_name] = best

        # Save back to json or create json
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def run_game(self, dt):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == GAME_WON:
                self.save_score()
                self.show_winscreen = True # Open win screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_ingame_menu = True # Open ingame menu
            else: self.player.event_handler(event)

        # Update level time if not paused or win screen
        if not self.show_ingame_menu and not self.show_winscreen:
            self.level_time += dt
        
        # Background
        self.display_surface.fill((255, 255, 255))
        self.game_surface.fill((255, 255, 255))

        self.all_sprites.update(dt) # Update all sprites
        self.camera.update(self.player.rect)

        # Items
        item_hits = pygame.sprite.spritecollide(self.player, self.map.item_sprites, dokill=True)
        for item in item_hits:
            if hasattr(item, "on_pickup"):
                item.on_pickup(self.player)
                self.item_pickup_sound.play()

        # Checkpoints
        checkpoint_hits = pygame.sprite.spritecollide(self.player, self.map.checkpoint_sprites, dokill=False)
        for checkpoint in checkpoint_hits:
            print("kollision checkpoint")
            checkpoint.set_active()
            self.player.last_checkpoint = checkpoint

        # Star Coin
        starcoin_hits = pygame.sprite.spritecollide(self.player, self.map.starcoin_sprites, dokill=True)
        for starcoin in starcoin_hits:
            print("Sternenmünze Kollision")
            if hasattr(starcoin, "on_pickup"):
                starcoin.on_pickup(self.player)
                self.starcoin_sound.play()
            print(self.player.star_coins)

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

        self.ui.draw(self.level_time)

        # Compute offsets for centering the game surface in the current window
        display_surface_width, display_surface_height = self.display_surface.get_size()
        x = (display_surface_width - WINDOW_WIDTH) // 2
        y = (display_surface_height - WINDOW_HEIGHT) // 2
        self.display_surface.fill((0, 0, 0))
        self.display_surface.blit(self.game_surface, (x,y))

        pygame.display.flip()
    
    # Game loop
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000 # delta time
            dt = min(dt, 0.05) # limit dt to max 50ms (avoid big physics jumps when window is dragged or game lags)

            self.run_game(dt)

            # show blocking win screen, when requested 
            if self.show_winscreen:
                self.show_winscreen = False
                win_choice = self.winscreen.run(game_surface_for_background=self.game_surface, duration_ms=WINSCREEN_DURATION_MS)
                if win_choice in ("done", "quit"):
                    self.running = False
            
            # show blocking ingame menu, when requested
            if self.show_ingame_menu:
                self.show_ingame_menu = False
                choice = self.ingame_menu.run(self.game_surface)
                if choice == "quit":
                    self.running = False