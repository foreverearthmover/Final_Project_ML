from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room, inventory

class Bathroom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "bathroom.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()
        self.width = self.background.get_width()

    def handle_event(self, event):
        # No event-specific behavior here (yet) --> later add click detection logic
        pass

    def update(self):
        self.cat.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.cat.draw(self.screen)
