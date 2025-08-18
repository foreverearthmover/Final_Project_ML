import pygame
from assets.media.text.fonts import get_small_font


class IntroScreen:
    def __init__(self, game):
        self.game = game
        self.font = get_small_font(14)
        self.text = (
            "Hello, Kitty! To finish this game you have to explore your owner’s apartment\n"
            "on the search for food while your owner is in the shower...\n"
            "but there may be some surprises ahead.\n\n"
            "Controls:\n"
            "You move using the arrow keys and can examine items by hovering over them.\n"
            "To add them to your inventory click them.\n"
            "Opening your inventory with “E” allows you to drop them again.\n\n"
            "Click to continue."
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clicking leads to the character select screen
            self.game.state = "character_select"

    def update(self):
        pass  # nothing animated here

    def draw(self, screen):
        # Fill background black
        screen.fill((0, 0, 0))

        # Render text in the center of the screen
        lines = self.text.split("\n")
        y = screen.get_height() // 4
        for line in lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(text_surface, text_rect)
            y += text_surface.get_height() + 5
