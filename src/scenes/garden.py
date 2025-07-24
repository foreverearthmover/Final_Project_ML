from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room, inventory

class Garden:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "garden.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()
        self.width = self.screen.get_width()
        #self.name = "garden"

    def handle_event(self, event):
        # No event-specific behavior here (yet) --> later add click detection logic
        pass

    def update(self):
        self.cat.update()
        self.check_boundaries()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.cat.draw(self.screen)

    def check_boundaries(self):
        # Can only exit to the left (back to living room)
        if self.cat.rect.left < 0:
            self.game.change_scene("living_room", "right")

