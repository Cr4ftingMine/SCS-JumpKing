from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, collision_sprites=None):
        super().__init__()
        self.frames = {}
        self.scale = (64, 64)  
        self.state = "idle"
        self.frame_index = 0

        self.load_images()

        self.image = self.frames["idle"][0]
        self.rect = self.image.get_frect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 64))

        # Hitbox for pixelperfect Collision
        hitbox_w, hitbox_h = 30, 54 # 30,54
        self.hitbox = pygame.FRect(0,0, hitbox_w, hitbox_h)
        self.hitbox.midbottom = self.rect.midbottom # Connect Renderrect and Colliderect

        # Kinematics
        self.velocity_x = 0
        self.velocity_y = 0

        # Input-/State
        self.direction = 0 # Direction if on_ground: 1 for right, -1 for left
        self.jump_power = 0
        self.jump_direction = 0
        self.on_ground = True
        self.charging_jump = False

        self.collision_sprites = collision_sprites

    def load_images(self):
        def load(path): return pygame.transform.smoothscale(pygame.image.load(join("images", "player", path)).convert_alpha(), self.scale)

        self.frames = {
            "idle": [load("player.png")],
            "walk": [load("player_walk1.png"), load("player_walk2.png")],
            "duck": [load("player_duck.png")],
            "jump": [load("player_jump.png")]
        }

    # !TODO Arbeitet an Events und steuert diese 
    def event_handler(self, event): 
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.release_jump()

    def input(self,dt):
        keys = pygame.key.get_pressed()

        #Horizontal Directions (only "Groundlevel")
        self.direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if self.on_ground:
            if keys[pygame.K_SPACE]:
                self.charging_jump = True
                self.jump_power = min(self.jump_power + JUMP_CHARGE_RATE *dt, MAX_JUMP_POWER)
                self.jump_direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        #print(f"Jump Power: {self.jump_power}, Jump Direction: {self.jump_direction}")

    def move(self, dt):
        # 1) Horizontal movement + Kollision
        if self.on_ground:
            if not self.charging_jump:
                self.hitbox.x += self.direction * PLAYER_SPEED * dt
        else: 
            self.hitbox.x += self.velocity_x * dt
        self.handle_collisions("horizontal")

        # 2) Vertical movement + Kollision
        self.velocity_y += GRAVITY * dt
        self.hitbox.y += self.velocity_y * dt
        self.on_ground = False
        self.handle_collisions("vertical")

        # Reconnect Renderrect and Colliderect -> Movement from Renderrect
        self.rect.midbottom = self.hitbox.midbottom 


    def release_jump(self):
        if self.charging_jump:
            self.velocity_y = -self.jump_power
            self.velocity_x = self.jump_direction * PLAYER_SPEED
            self.jump_power = 0
            self.charging_jump = False
            self.on_ground = False 

    def handle_collisions(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "vertical":
                    if self.velocity_y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.velocity_y = 0
                        self.velocity_x = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:
                        self.hitbox.top = sprite.rect.bottom
                        self.velocity_y = 0

#!TODO: Doppelbounce möglich? Im Spiel auch unterstützt?
                elif direction == "horizontal":
                    move_dir = self.velocity_x if not self.on_ground else self.direction
                    #if self.velocity_x > 0:
                    if move_dir > 0: 
                        self.hitbox.right = sprite.rect.left

                        # Wall Bounce - Right into wall
                        self.velocity_x = -PLAYER_SPEED * 0.5
                        self.velocity_y = max(self.velocity_y, -200)

                    #elif self.velocity_x < 0:
                    elif move_dir < 0:
                        self.hitbox.left = sprite.rect.right

                        # Wall Bounce - Left into wall
                        self.velocity_x = PLAYER_SPEED * 0.5
                        self.velocity_y = max(self.velocity_y, -200)

    def animate(self, dt):
        if not self.on_ground:
            self.state = "jump"
        elif self.charging_jump:
            self.state = "duck"
        elif self.direction != 0:
            self.state = "walk"
        else:
            self.state = "idle"

        frames = self.frames[self.state]
        self.frame_index += 5 * dt if len(frames) > 1 else 0
        self.image = frames[int(self.frame_index) % len(frames)]

        flip = False
        if self.state == "duck":
            if self.jump_direction != 0:
                flip = self.jump_direction < 0
        else: 
            if self.direction != 0:
                flip = self.direction < 0
        
        self.image = pygame.transform.flip(self.image, True, False) if flip else self.image

    def draw_charge_bar(self, surface, camera):
        # Show only when charging or midjump
        if not self.charging_jump and self.jump_power <= 0:
            return

        screen_rect = self.rect.move(0, camera.offset.y)
        width, height = 60, 8
        gap = -10 # Extra space between player and bar (on top of rect.top)
        bg_color, fg_color, border_color = (40, 40, 40), (80, 200, 120), (0, 0, 0) # background color, filling color, border color

        # Position Background rectangle (above the player)
        x = screen_rect.centerx - width // 2
        y = screen_rect.top - gap - height
        bg_rect = pygame.Rect(x, y, width, height)

        # Fill rectangle based on jump_power
        pct = self.jump_power / MAX_JUMP_POWER
        fill_rect = pygame.Rect(x, y, int(width * pct), height)

        pygame.draw.rect(surface, bg_color, bg_rect, border_radius=3) # Background
        pygame.draw.rect(surface, fg_color, fill_rect, border_radius=3) # Filling
        pygame.draw.rect(surface, border_color, bg_rect, 1, border_radius=3) # Border

    def update(self, dt):
        self.input(dt)
        self.move(dt)
        self.animate(dt)