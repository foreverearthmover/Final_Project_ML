from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room, inventory #!!!

#Hello I have to edit a couple things since the Items will be in this room, I will mark everything I add
class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        #self.items = create_items_for_room("Living room")
        self.items = create_items_for_room("Living room", game=self.game)

        path = os.path.join("..", "assets", "media", "backgrounds", "living_room.png")
        self.background = pygame.image.load(path).convert()



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse clicked at:", pygame.mouse.get_pos())
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()



        #No event-specific behavior here (yet) --> later add click detection logic
        #pass


    def update(self):
        self.cat.update()

    def draw_inventory(self):
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, 300, 100))  # inventory background
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 300, 100), 2)  # border

        for i, item in enumerate(inventory):
            # Scale image for inventory display
            inventory_img = pygame.transform.scale(item.image, (40, 40))
            self.screen.blit(inventory_img, (20 + i * 50, 20))

            # Optional: item name below it
            text = font.render(item.name, True, (255, 255, 255))
            self.screen.blit(text, (20 + i * 50, 65))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        #!!!
        self.game.hover_message = ""

        for item in self.items:
            item.draw(self.screen)
        self.cat.draw(self.screen)
        if self.game.show_inventory:
            self.draw_inventory()
        self.draw_hover_message()


    def draw_hover_message(self):
        if hasattr(self.game, "hover_message") and self.game.hover_message:
            font = pygame.font.SysFont(None, 20)
            msg_surface = font.render(self.game.hover_message, True, (255, 255, 255))
            bg_rect = msg_surface.get_rect(topleft=(10, self.screen.get_height() - 30))
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect.inflate(10, 10))
            self.screen.blit(msg_surface, bg_rect)





