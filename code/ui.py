from settings import *

class UI:
    def __init__(self, surface, player, enable_extensions):
        self.surface = surface
        self.player = player
        self.enable_extensions = enable_extensions
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 16)

        self.inventory_slots = []

        # Load of Icon 
        self.starcoin_icon = pygame.transform.smoothscale(pygame.image.load(join("images", "tiles", "starcoin.png")).convert_alpha(),(28, 28))
        self.starcoin_icon_empty = self.starcoin_icon.copy()
        self.starcoin_icon_empty.fill((200, 200, 200, 150), special_flags=pygame.BLEND_RGBA_MULT)

        def load(path, scale): return pygame.transform.smoothscale(pygame.image.load(join("images", "keys", path)).convert_alpha(), scale)

        self.key_icon_size = (20, 20)
        self.key_icons = {
            "1": load("key_1.png", self.key_icon_size),
            "2": load("key_2.png", self.key_icon_size),
            "3": load("key_3.png", self.key_icon_size)
        }

    def draw_height(self): #!TODO: Will ich das? Höhe ungleich Höhenlayer, da anders gezählt
        height_value = int((WINDOW_WIDTH - TILE_SIZE) - self.player.hitbox.bottom)
        text_surface = self.font.render(f"Height: {int(height_value / 64)}", True, (0,0,0)) 
        text_rect = text_surface.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.surface.blit(text_surface, text_rect)

    def draw_inventory(self):
        slot_size = 48
        slot_count = 3
        padding = 10
        start_x = WINDOW_WIDTH // 2 - (slot_size * slot_count + padding * (slot_count - 1)) // 2
        y = WINDOW_HEIGHT - slot_size - 10

        for i in range(slot_count):
            rect = pygame.Rect(start_x + i * (slot_size + padding), y, slot_size, slot_size)
            pygame.draw.rect(self.surface, (220,220,220), rect) # Slot background
            pygame.draw.rect(self.surface, (0,0,0), rect, 2) # Border

            if i < len(self.player.inventory):
                item = self.player.inventory[i]
                icon = pygame.transform.smoothscale(item.image, (40,40))
                self.surface.blit(icon, rect.inflate(-8,-8).topleft)

            # Highlight selected slot
            if i == self.player.selected_item:
                pygame.draw.rect(self.surface, (255,215,0), rect, 3)
            
            # Draw key icon above slot
            num = str(i + 1)
            key_img = self.key_icons.get(num)
            if key_img:
                key_rect = key_img.get_rect(midbottom=(rect.centerx, rect.top + 2))
                bg = pygame.Rect(0, 0, key_rect.width + 6 , key_rect.height + 4)
                bg.center = (key_rect.centerx, key_rect.centery - 1)
                self.surface.blit(key_img, key_rect)

    def draw_starcoins_row(self):
        # Layout
        padding_x, padding_y = 8, 6 # Space between border and icon
        spacing = 8 # Space between icons
        icon_width = self.starcoin_icon.get_width()
        icon_height = self.starcoin_icon.get_height()
        total_icons = TOTAL_STARCOIN

        # Hintergrund-Panel berechnen
        total_width = total_icons * icon_width + (total_icons - 1) * spacing
        total_height = icon_height
        bg_rect = pygame.Rect(20, 30, total_width + 2 * padding_x, total_height + 2 * padding_y) # background rect

        # Panel zeichnen
        pygame.draw.rect(self.surface, (240, 240, 240), bg_rect, border_radius=6)
        pygame.draw.rect(self.surface, (0, 0, 0), bg_rect, 2, border_radius=6)

        # Icons nebeneinander
        start_pos_x = bg_rect.left + padding_x # Starting position for icon x
        start_pos_y = bg_rect.top + padding_y # Starting position for icon y
        for i in range(total_icons):
            icon = self.starcoin_icon if i < self.player.star_coins else self.starcoin_icon_empty
            self.surface.blit(icon, (start_pos_x, start_pos_y))
            start_pos_x += icon_width + spacing

    def draw(self):
        self.draw_height()
        self.draw_starcoins_row()
        if self.enable_extensions:
            self.draw_inventory()