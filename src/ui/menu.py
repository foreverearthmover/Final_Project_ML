import pygame
from assets.media.text.fonts import get_big_font


class MainMenu:
    """ Main menu screen."""
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.title_font = get_big_font()
        self.button_font = get_big_font()

        self.start_button_rect = pygame.Rect(275, 280, 200, 60)
        self.quit_button_rect = pygame.Rect(275, 360, 200, 60)

        self.button_color_default = (255, 255, 255)
        self.button_color_hover = (180, 180, 180)

    def handle_event(self, event):
        """ Handle mouse clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button_rect.collidepoint(mouse_pos):
                self.game.start_game()  # Initialize the living room
            elif self.quit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                exit()

    def draw(self, screen):
        """ Draw buttons and text on screen."""
        screen.fill((0, 0, 0))

        # Title text
        title_surface = self.title_font.render("Main Menu", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 100))

        # check for mouse
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