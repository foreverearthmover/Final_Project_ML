from objects.player import Cat
import os
import pygame

class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        path = os.path.join("..", "assets", "media", "backgrounds", "living_room.png")
        self.background = pygame.image.load(path).convert()

    def handle_event(self, event):
        # No event-specific behavior here (yet) --> later add click detection logic
        pass

    def update(self):
        self.cat.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.cat.draw(self.screen)
