from settings import *
from menu_utils import draw_button, draw_panel

class ingameMenu:
    def __init__(self, surface):
        self.surface = surface
        
        # Fonts
        self.font_big = pygame.font.SysFont(None, 64)
        self.font = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 26)

        # Button
        self.button_resume = None
        self.button_quit = None
        self.selected = 0 # Index of selected button (0 = resume, 1 = quit)

        # Sound
        self.sound_select = pygame.mixer.Sound(join("audio", "menu_click.ogg"))
        self.sound_select.set_volume(0.008)

        # Key-Icons
        def load(path, scale): return pygame.transform.smoothscale(pygame.image.load(join("images", "keys", path)).convert_alpha(), scale)

        self.key_icon_size = (32, 32)
        self.key_icons = {
            "1": load("key_1.png", self.key_icon_size), # Iventory Slot 1
            "2": load("key_2.png", self.key_icon_size), # Iventory Slot 2
            "3": load("key_3.png", self.key_icon_size), # Iventory Slot 3
            "E": load("key_e.png", self.key_icon_size), # Use Item
            "F": load("key_f.png", self.key_icon_size), # Interact
            "R": load("key_r.png", self.key_icon_size), # Respawn / Checkpoint
            "A": load("key_a.png", self.key_icon_size), # Left movement
            "D": load("key_d.png", self.key_icon_size), # Right movement
            "SPACE": load("key_space.png", self.key_icon_size) # Charge jump
        }

    # Draw a row with key icons and a label next to it
    def draw_hint_row(self, x, y, keys, text, key_gap=8, label_gap=12):
        imgs = [self.key_icons[k] for k in keys if k in self.key_icons and self.key_icons[k] is not None]
        text_surf = self.font_small.render(text, True, (0, 0, 0))
        max_height = max([img.get_height() for img in imgs] + [text_surf.get_height()]) if imgs else text_surf.get_height()

        current_x = x
        for img in imgs:
            img_y = y + (max_height - img.get_height()) // 2 # center vertically
            self.surface.blit(img, (current_x, img_y))
            current_x += img.get_width() + key_gap # next position

        if imgs:
            current_x += label_gap
        text_y = y + (max_height - text_surf.get_height()) // 2
        self.surface.blit(text_surf, (current_x, text_y))

        total_width = (current_x + text_surf.get_width()) - x
        return pygame.Rect(x, y, total_width, max_height)

    # Draw the keybind explanation
    def draw_keybind_explain(self, panel_rect, after_rect):
        left_x = panel_rect.left + 48     # Left alignment inside panel
        y = after_rect.bottom + 24        # Start below the "Quit" button
        row_gap = 10

        # key + label
        rows = [
            (["A", "D"],     "Bewegen (links/rechts)"),
            (["SPACE"],      "Springen – halten & loslassen"),
            (["E"],          "Item benutzen"),
            (["F"],          "Interagieren"),
            (["R"],          "Respawn / Checkpoint"),
            (["1", "2", "3"],"Inventar-Slot wählen"),
        ]

        for keys, label in rows:
            r = self.draw_hint_row(left_x, y, keys, label)
            y = r.bottom + row_gap


    # Run-Loop (blocking)
    def run(self, game_surface_for_background=None):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60)

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sound_select.play()
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        self.sound_select.play()
                        return "resume"
                    elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                        self.sound_select.play()
                        self.selected = 1 - self.selected  # Toggle selection between Resume and Quit
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.sound_select.play()
                        return "resume" if self.selected == 0 else "quit"

            # Background: frozen game frame centered in current window + darker menu overlay 
            self.surface.fill((0, 0, 0))
            if game_surface_for_background is not None:
                surface_width, surface_height = self.surface.get_size()
                offset_x, offset_y = (surface_width - WINDOW_WIDTH) // 2, (surface_height - WINDOW_HEIGHT) // 2
                self.surface.blit(game_surface_for_background, (offset_x, offset_y))

            # dark overlay
            overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.surface.blit(overlay, (0, 0))

            # Panel + Buttons
            panel_rect, y_top = draw_panel(self.surface, self.font_big, "Pause")
            centerx = self.surface.get_width() // 2
            first_y = y_top + 40
            second_y = first_y + BUTTON_GAP + BUTTON_HEIGHT

            self.button_resume = draw_button(
                self.surface, centerx, first_y, "Fortsetzen", self.font, selected=(self.selected == 0)
            )
            self.button_quit = draw_button(
                self.surface, centerx, second_y, "Beenden", self.font, selected=(self.selected == 1)
            )

            # Draw keybind explanation
            self.draw_keybind_explain(panel_rect, self.button_quit)


            # Footer hints
            footer = "ENTER bestätigen • ESC schließen"
            footer_surface = self.font_small.render(footer, True, (60, 60, 60))
            self.surface.blit(footer_surface, footer_surface.get_rect(
                center=(self.surface.get_width() // 2, panel_rect.bottom - 24)
            ))

            pygame.display.flip()