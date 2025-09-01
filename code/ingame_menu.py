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
        self.selected = 0

    # Run-Loop (blocking)
    def run(self, game_surface_for_background=None):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60)

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        return "resume"
                    elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s):
                        self.selected = 1 - self.selected  # zwischen 0 und 1 togglen
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
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

            # Footer hints
            footer = "ENTER bestätigen • ESC schließen"
            footer_surface = self.font_small.render(footer, True, (60, 60, 60))
            self.surface.blit(footer_surface, footer_surface.get_rect(
                center=(self.surface.get_width() // 2, panel_rect.bottom - 24)
            ))

            pygame.display.flip()