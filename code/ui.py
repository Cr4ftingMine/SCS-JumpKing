from settings import *

class UI:
    def __init__(self, surface, player, game_map):
        self.surface = surface
        self.player = player
        self.map = game_map
        self.font = pygame.font.Font(None, 36)

        self.inventory_slots = []

    def draw_height(self):
        
        height_value = int((WINDOW_WIDTH - TILE_SIZE) - self.player.hitbox.bottom)
        text_surface = self.font.render(f"Height: {height_value}", True, (0,0,0))
        text_rect = text_surface.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.surface.blit(text_surface, text_rect)

    def draw_inventory(self):
        slot_size = 48
        slot_count = 2
        padding = 10
        start_x = WINDOW_WIDTH // 2 - (slot_size * slot_count + padding * (slot_count - 1)) // 2
        y = WINDOW_HEIGHT - slot_size - 10

        for i in range(slot_count):
            rect = pygame.Rect(start_x + i * (slot_size + padding), y, slot_size, slot_size)
            pygame.draw.rect(self.surface, (220,220,220), rect) # Slot background
            pygame.draw.rect(self.surface, (0,0,0), rect, 2) # Border

    def draw(self):
        self.draw_height()
        self.draw_inventory()