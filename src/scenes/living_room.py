from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room #!!!

#Hello I have to edit a couple things since the Items will be in this room, I will mark everything I add
class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        self.items = create_items_for_room("Living room")



        path = os.path.join("..", "assets", "media", "backgrounds", "living_room.png")
        self.background = pygame.image.load(path).convert()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse clicked at:", pygame.mouse.get_pos())
        #No event-specific behavior here (yet) --> later add click detection logic
        #pass


    def update(self):
        self.cat.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        #!!!
        for item in self.items:
            item.draw(self.screen)
        self.cat.draw(self.screen)



