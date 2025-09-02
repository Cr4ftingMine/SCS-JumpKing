from settings import *
from game import *
from menu_utils import draw_button, draw_panel

class Menu: 
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Jump King - Extended Version")

        self.clock = pygame.time.Clock()

        # Fonts
        self.font_big = pygame.font.SysFont(None, 64)
        self.font = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 26)

        # Zustände
        self.menu_mode = "main" # "main" or "levels" 
        self.running = True
        self.enable_extensions = True 

        # Hauptmenü
        self.main_menu = None
        self.main_menu_selected = 0

        # Level-Liste
        self.levels = self.load_levels()
        self.level_selected = 0
        self.scores = {}
        self.load_scores()

        # Sound
        self.select_sound = pygame.mixer.Sound(join("audio", "menu_click.ogg"))
        self.select_sound.set_volume(0.008)
        self.switch_sound = pygame.mixer.Sound(join("audio", "switch29.ogg"))
        self.switch_sound.set_volume(0.008)

    def load_levels(self):
        # Load all .tmx files and return them as a list of dicts {"name": <level name>, "path": <file path>}
        level_dir = os.path.join(os.path.dirname(__file__), "../data/Map")
        levels = []
        for filename in os.listdir(level_dir):
            if filename.endswith(".tmx"): # Only .tmx files
                path = join(level_dir, filename) # Build path
                name = splitext(filename)[0] 
                levels.append({"name": name, "path": path}) # store name and path 
        
        return levels

    def load_scores(self):
        # Load best scores from JSON file into self.scores
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                known = {level["name"] for level in self.levels}
                for k, v in data.items():
                    if k in known:
                        self.scores[k] = int(v)
            except Exception:
                self.scores = {} # Fallback if error: no scores
    
    def change_extension_state(self):
        self.enable_extensions = not self.enable_extensions

    # Event-Handler
    def handle_main_keydown_events(self, event):
        if event.key in (pygame.K_UP, pygame.K_w):
            self.main_menu_selected = (self.main_menu_selected - 1) % 2
            self.select_sound.play()
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.main_menu_selected = (self.main_menu_selected + 1) % 2
            self.select_sound.play()
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.select_sound.play()
            if self.main_menu_selected == 0:
                self.menu_mode = "levels"
            else: 
                self.running = False 

    def handle_levels_keydown_events(self, event):
        if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.menu_mode = "main"
            self.select_sound.play()
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.select_sound.play()
            if self.levels:
                self.level_selected = (self.level_selected - 1) % len(self.levels) 
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.select_sound.play()
            if self.levels:
                self.level_selected = (self.level_selected + 1) % len(self.levels)
        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.switch_sound.play()
            self.change_extension_state()
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.select_sound.play()
            self.start_selected_level()
    
    # Draw Menu / Levels
    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        panel_rect, y_top = draw_panel(self.screen, self.font_big, "Jump King - Extended Version")

        # Vertical button layout
        centerx = self.screen.get_width() // 2
        first_button_y = y_top + 40 # First button: some space below the title (40 px)
        second_button_y = first_button_y + BUTTON_GAP + BUTTON_HEIGHT # Second button: place below the first with a fixed gap and button height

        # Play button
        self.button_play = draw_button(
            self.screen, centerx, first_button_y, "Spielen", 
            self.font,
            selected=(self.main_menu_selected==0)
        )

        # Quit button
        self.button_quit = draw_button(
            self.screen, centerx, second_button_y, "Beenden",
            self.font,
            selected=(self.main_menu_selected==1)
        )

    def draw_levels(self):
        self.screen.fill((255, 255, 255)) # clear screen and fill with white
        panel_rect, y_top = draw_panel(self.screen, self.font_big, "Select Level")

        # Extension-Toggle (top-right)
        box_width, box_height = 180, 56
        self.ext_toggle_rect = pygame.Rect(0, 0, box_width, box_height)
        self.ext_toggle_rect.top = panel_rect.top + 24
        self.ext_toggle_rect.right = panel_rect.right - 24
        pygame.draw.rect(self.screen, (250, 250, 250), self.ext_toggle_rect) # fill
        pygame.draw.rect(self.screen, (0, 0, 0), self.ext_toggle_rect, 6) # border
        txt = f"Extended: {"an" if self.enable_extensions else "aus"}"
        t_s = self.font_small.render(txt, True, (0, 0, 0))
        self.screen.blit(t_s, t_s.get_rect(center=self.ext_toggle_rect.center))

        # Column headers (left = level ; right = score)
        left_column = panel_rect.left + 120
        right_column = panel_rect.right - 120
        header_y = y_top + 20 # Y-position of left- and right-header
        left_header = self.font_small.render("Level", True, (60, 60, 60))
        right_header = self.font_small.render("Score", True, (60, 60, 60))
        self.screen.blit(left_header, (left_column, header_y))
        self.screen.blit(right_header, (right_column, header_y))

        # Level list 
        start_level_row_y = header_y + 30 # start drawing 30px below header

        for i, lvl in enumerate(self.levels):
            level_row_y = start_level_row_y + i * LEVEL_ROW_H
            # Highlight for currently selected row
            is_selected = (i == self.level_selected)
            row_rect = pygame.Rect(panel_rect.left+40, level_row_y-6, panel_rect.width-80, LEVEL_ROW_H) # rect for the whole row
            if is_selected:
                pygame.draw.rect(self.screen, (255,235,150), row_rect)
                pygame.draw.rect(self.screen, (0,0,0), row_rect, 2)
            # left column (name)
            name_lvl = self.font.render(lvl["name"], True, (0,0,0))
            self.screen.blit(name_lvl, (left_column, level_row_y))

            # right column (score)
            score_value = self.scores.get(lvl["name"], "-") # Get Value or default "-"
            score_surface = self.font.render(str(score_value), True, (0,0,0)) # Creates surface with text
            score_rect = score_surface.get_rect(right=panel_rect.right - 120, centery=level_row_y + name_lvl.get_height()//2)
            self.screen.blit(score_surface, score_rect.topleft)

        # Footer
        footer = "ENTER starten • ESC zurück •  ←/→ toggelt Extension"
        footer_surface = self.font_small.render(footer, True, (60,60,60)) # Creates surface with text
        self.screen.blit(footer_surface, footer_surface.get_rect(center=(self.screen.get_width()//2, panel_rect.bottom - 24)))

    # Create game class and start selected level
    def start_selected_level(self):
        if not self.levels:
            return
        level = self.levels[self.level_selected]
        game = Game(display_surface=self.screen, level_path=level["path"], enable_extensions=self.enable_extensions)
        game.run()
        self.load_scores()


    # Run-Loop
    def run(self):
        while self.running:

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                elif event.type == pygame.KEYDOWN:
                    if self.menu_mode == "main":
                        self.handle_main_keydown_events(event)
                    elif self.menu_mode == "levels":
                        self.handle_levels_keydown_events(event)
            
            # Draw handler
            if self.menu_mode == "main":
                self.draw_menu()
            elif self.menu_mode == "levels":
                self.draw_levels()
            

            pygame.display.flip()
        pygame.quit()



if __name__ == "__main__":
    Menu().run()