from settings import *

def draw_panel(display_surface, font_big, title):
    window_width, window_heigth = display_surface.get_size()
    rect = pygame.Rect(PANEL_MARGIN, PANEL_MARGIN, window_width - 2 * PANEL_MARGIN, window_heigth - 2 * PANEL_MARGIN)
    pygame.draw.rect(display_surface, (240, 240, 240), rect) # fill
    pygame.draw.rect(display_surface, (0, 0, 0), rect, 6) # border

    # Place and center text
    title_surf = font_big.render(title, True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(window_width//2, rect.top + 60))
    display_surface.blit(title_surf, title_rect)
    return rect, title_rect.bottom
    
def draw_button(surface, centerx, y, text, font, selected=False):
    rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    rect.centerx = centerx
    rect.top = y
    bg = (250, 250, 250)
    pygame.draw.rect(surface, bg, rect) # fill
    pygame.draw.rect(surface, (0, 0, 0), rect, 6) # border

    if selected:
        pygame.draw.rect(surface, (255, 215, 0), rect.inflate(10, 10), 6) # highlight + inflate

    label = font.render(text, True, (0, 0, 0))
    surface.blit(label, label.get_rect(center=rect.center))
    return rect 