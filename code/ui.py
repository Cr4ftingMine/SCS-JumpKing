from settings import *

class UI:
    def __init__(self, surface, player, enable_extensions):
        self.surface = surface
        self.player = player
        self.enable_extensions = enable_extensions
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 16)

        # Effects
        self._effect_totals = {}

        # Inventory
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
    
    # Draw the time elapsed since start of level
    def draw_timer(self, elapsed_time):
        minutes = int(elapsed_time // 60)
        sec = int(elapsed_time % 60)
        label = f"Time: {minutes:02d}:{sec:02d}"
        text_surface = self.font.render(label, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.surface.blit(text_surface, text_rect)

    # Draw the inventory slots
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

    # Draw the star coin row (top-left corner)
    def draw_starcoins_row(self):
        # Layout
        padding_x, padding_y = 8, 6 # Space between border and icon
        spacing = 8 # Space between icons
        icon_width = self.starcoin_icon.get_width()
        icon_height = self.starcoin_icon.get_height()
        total_icons = TOTAL_STARCOIN

        # Calculate background rect
        total_width = total_icons * icon_width + (total_icons - 1) * spacing
        total_height = icon_height
        bg_rect = pygame.Rect(20, 30, total_width + 2 * padding_x, total_height + 2 * padding_y) # background rect

        # Draw panel
        pygame.draw.rect(self.surface, (240, 240, 240), bg_rect, border_radius=6)
        pygame.draw.rect(self.surface, (0, 0, 0), bg_rect, 2, border_radius=6)

        # Draw icons next to each other
        start_pos_x = bg_rect.left + padding_x # Starting position for icon x
        start_pos_y = bg_rect.top + padding_y # Starting position for icon y
        for i in range(total_icons):
            icon = self.starcoin_icon if i < self.player.star_coins else self.starcoin_icon_empty
            self.surface.blit(icon, (start_pos_x, start_pos_y))
            start_pos_x += icon_width + spacing

    # Draw active effects with timers (if any)
    def draw_effects(self):
        # Collect active effects 
        effects = []
        if getattr(self.player, "jump_boost_timer", 0) > 0:
            effects.append(("Jump Boost", self.player.jump_boost_timer))
        if getattr(self.player, "slowfall_timer", 0) > 0:
            effects.append(("Slowfall", self.player.slowfall_timer))

        if not effects:
            return

        # Collect total time, if remaining time is higher than before (=new effect)
        for name, remaining in effects:
            prev_total = self._effect_totals.get(name, 0)
            if remaining > prev_total:
                self._effect_totals[name] = remaining

        # Draw
        font = getattr(self, "small_font", None) or pygame.font.Font(None, 20)
        x, y0 = 20, 72          # Under starcoin row
        h_badge, h_bar, gap = 22, 6, 6 

        for i, (label, remaining) in enumerate(effects):
            # Use stored total time for progress calculation
            total = max(self._effect_totals.get(label, remaining), 0.0001)  # Fallback to avoid div by zero
            y = y0 + i * (h_badge + h_bar + gap)

            # Render text
            text = font.render(f"{label}  {remaining:0.1f}s", True, (0, 0, 0))
            w = text.get_width() + 24
            badge = pygame.Rect(x, y, w, h_badge)
            bar_background = pygame.Rect(x, y + h_badge + 2, w, h_bar)

            # Draw badge, background and border
            pygame.draw.rect(self.surface, (240, 240, 240), badge, border_radius=8)
            pygame.draw.rect(self.surface, (0, 0, 0), badge, 1, border_radius=8)
            self.surface.blit(text, (badge.x + 12, badge.y + (h_badge - text.get_height()) // 2))

            # Draw progr
            pct = max(0.0, min(1.0, remaining / total))
            bar_foreground = pygame.Rect(bar_background.x, bar_background.y, int(bar_background.w * pct), h_bar)
            pygame.draw.rect(self.surface, (220, 220, 220), bar_background, border_radius=3)
            pygame.draw.rect(self.surface, (80, 200, 120), bar_foreground, border_radius=3)
            pygame.draw.rect(self.surface, (0, 0, 0), bar_background, 1, border_radius=3)



    def draw(self, elapsed_time):
        self.draw_timer(elapsed_time)
        self.draw_starcoins_row()
        if self.enable_extensions:
            self.draw_inventory()
            self.draw_effects()