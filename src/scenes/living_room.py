import pygame
from objects.player import Cat

class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.background = pygame.image.load("../assets/media/backgrounds/living_room.png")
        self.cat = Cat(100, 200)
        self.items = []  # add items later

    def handle_event(self, event):
        self.cat.handle_event(event)
        # add item click logic

    def update(self):
        self.cat.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.cat.draw(self.screen)
        for item in self.items:
            item.draw(self.screen)
