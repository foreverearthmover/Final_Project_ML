import pygame
import sys

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font_path = "../assets/media/fonts/8-BIT WONDER.ttf"
        self.title_font = pygame.font.Font(self.font_path, 48)
        self.button_font = pygame.font.Font(self.font_path, 32)

        self.start_button_rect = pygame.Rect(275, 280, 200, 60)
        self.quit_button_rect = pygame.Rect(275, 360, 200, 60)

        self.button_color_default = (255, 255, 255)
        self.button_color_hover = (180, 180, 180)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button_rect.collidepoint(event.pos):
                self.game.state = "playing"
            elif self.quit_button_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Title
        title_text = self.title_font.render("Main Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(375, 150))
        screen.blit(title_text, title_rect)

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
