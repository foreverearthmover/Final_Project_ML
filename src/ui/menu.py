import pygame
import os

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "fonts", "8-bit_wonder.TTF")
        font_path = os.path.normpath(font_path)

        # debugging
        if not os.path.isfile(font_path):
            raise FileNotFoundError(f"Font file not found at {font_path}")

        self.title_font = pygame.font.Font(font_path, 48)
        self.button_font = pygame.font.Font(font_path, 36)

        self.start_button_rect = pygame.Rect(275, 280, 200, 60)
        self.quit_button_rect = pygame.Rect(275, 360, 200, 60)

        self.button_color_default = (255, 255, 255)
        self.button_color_hover = (180, 180, 180)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button_rect.collidepoint(mouse_pos):
                #self.game.state = "playing"  # Change to playing state
                self.game.start_game()  # Initialize the living room
            elif self.quit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # title
        title_surface = self.title_font.render("Main Menu", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 100))

        mouse_pos = pygame.mouse.get_pos()

        # Start Button
        start_color = self.button_color_hover if self.start_button_rect.collidepoint(mouse_pos) else self.button_color_default
        pygame.draw.rect(screen, start_color, self.start_button_rect, border_radius=10)
        start_text = self.button_font.render("Start", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=self.start_button_rect.center)
        screen.blit(start_text, start_rect)

        # Quit Button
        quit_color = self.button_color_hover if self.quit_button_rect.collidepoint(mouse_pos) else self.button_color_default
        pygame.draw.rect(screen, quit_color, self.quit_button_rect, border_radius=10)
        quit_text = self.button_font.render("Exit", True, (0, 0, 0))
        quit_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        screen.blit(quit_text, quit_rect)