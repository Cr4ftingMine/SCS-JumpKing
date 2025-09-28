from settings import *

class WinScreen:
    def __init__(self, surface):
        self.surface = surface
        self.font_big = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 28)

        self.win_sound = pygame.mixer.Sound(join(AUDIO_DIR, "win_sound.wav"))
        self.win_sound.set_volume(0.008)

    def run(self, game_surface_for_background=None, duration_ms=5000):
        self.win_sound.play()
        clock = pygame.time.Clock()
        start = pygame.time.get_ticks()

        while True:
            dt = clock.tick(60)

            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN: # skip win screen
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        return "done"

            # frozen background + win overlay
            self.surface.fill((0, 0, 0))
            if game_surface_for_background is not None:
                surface_width, surface_height = self.surface.get_size() # current window/surface width & height
                offset_x, offset_y = (surface_width - WINDOW_WIDTH) // 2, (surface_height - WINDOW_HEIGHT) // 2 # Compute offsets to center the fixed-size game canvas
                self.surface.blit(game_surface_for_background, (offset_x, offset_y))

            overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.surface.blit(overlay, (0, 0))

            # draws centred title + subtitle
            rect = self.surface.get_rect()
            title = self.font_big.render("Geschafft!", True, (255, 215, 0))
            info  = self.font.render("Danke fürs Spielen", True, (230, 230, 230))
            self.surface.blit(title, title.get_rect(center=(rect.centerx, rect.centery - 20)))
            self.surface.blit(info, info.get_rect(center=(rect.centerx, rect.centery + 40)))

            pygame.display.flip()

            # close if duration expired
            if pygame.time.get_ticks() - start >= duration_ms:
                return "done"
