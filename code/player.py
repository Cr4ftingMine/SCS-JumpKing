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
        hitbox_w, hitbox_h = 36, 54
        self.hitbox = pygame.FRect(0,0, hitbox_w, hitbox_h)
        self.hitbox.midbottom = self.rect.midbottom # Benötigt?

        self.velocity_x = 0
        self.velocity_y = 0
        self.jump_power = 0
        self.jump_direction = 0
        self.on_ground = True
        self.charging_jump = False
        self.direction = 0 # 1 for right, -1 for left

        self.collision_sprites = collision_sprites

    def load_images(self):
        def load(path): return pygame.transform.smoothscale(pygame.image.load(join("images", "player", path)).convert_alpha(), self.scale)

        self.frames = {
            "idle": [load("player.png")],
            "walk": [load("player_walk1.png"), load("player_walk2.png")],
            "duck": [load("player_duck.png")],
            "jump": [load("player_jump.png")]
        }

    def input(self,dt):
        keys = pygame.key.get_pressed()
        if self.on_ground:
            if keys[pygame.K_SPACE]:
                self.charging_jump = True
                self.jump_power = min(self.jump_power + JUMP_CHARGE_RATE *dt, MAX_JUMP_POWER)
                self.jump_direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            elif not self.charging_jump:
                self.direction = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
                self.rect.x += self.direction * PLAYER_SPEED *dt
        #print(f"Jump Power: {self.jump_power}, Jump Direction: {self.jump_direction}")


    def release_jump(self):
        if self.charging_jump:
            self.velocity_y = -self.jump_power
            self.velocity_x = self.jump_direction * PLAYER_SPEED
            self.jump_power = 0
            self.charging_jump = False
            self.on_ground = False 

    def handle_collisions(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.velocity_x > 0: 
                        self.rect.right = sprite.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = sprite.rect.right
                    self.velocity_x = 0
                elif direction == "vertical":
                    if self.velocity_y > 0:
                        self.rect.bottom = sprite.rect.top
                        #self.rect.y = round(self.rect.y) # Addon!
                        self.velocity_y = 0
                        self.velocity_x = 0
                        self.on_ground = True
                    elif self.velocity_y < 0:
                        self.rect.top = sprite.rect.bottom
                        #self.rect.y = round(self.rect.y) #Addon!
                        self.velocity_y = 0


    def move(self, dt):
        #if not self.on_ground: # Lieber immer anwenden?
        self.velocity_y += GRAVITY * dt

        self.rect.x += self.velocity_x * dt
        self.handle_collisions("horizontal")

        if self.velocity_y != 0: 
            self.rect.y += self.velocity_y * dt
            self.on_ground = False
            self.handle_collisions("vertical")
    

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

    def check_if_on_ground(self):
        if self.on_ground:
            one_pixel_below = self.rect.move(0, 1)
            if not any(sprite.rect.colliderect(one_pixel_below) for sprite in self.collision_sprites):
                self.on_ground = False

    def update(self, dt):
        self.input(dt)
        self.move(dt)
        #self.check_if_on_ground() # Wird nicht benötigt
        self.animate(dt)