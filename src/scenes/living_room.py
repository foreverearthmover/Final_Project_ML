from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image #!!!

#Hello I have to edit a couple things since the Items will be in this room, I will mark everything I add
class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        #self.items = [] #!!!

        #!!!Test item hinzufügen, gotta see if there is a way to not add them all individually
        #cat_tree_img = load_test_image("Cat tree")
        #cat_tree = Item("Cat tree", (100, 100), cat_tree_img)
        #self.items.append(cat_tree)

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
        #!!!
        #for item in self.items:
            #item.draw(self.screen)
