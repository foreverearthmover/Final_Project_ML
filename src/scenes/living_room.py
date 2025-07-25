from objects.player import Cat
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room, inventory, INVENTORY_COLOR,  INVENTORY_BORDER_COLOR, WHITE #!!!

#Hello I have to edit a couple things since the Items will be in this room, I will mark everything I add
class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        #self.items = create_items_for_room("Living room")
        self.items = create_items_for_room("Living room", game=self.game)
        self.selected_inventory_item = None

        path = os.path.join("..", "assets", "media", "backgrounds", "living_room.png")
        self.background = pygame.image.load(path).convert()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse clicked at:", mouse_pos)

            # Check clicks on items in the world
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()

            # Check inventory interactions
            if self.game.show_inventory:
                for i, item in enumerate(inventory):
                    item_x = 20 + i * 50
                    item_y = 20
                    item_rect = pygame.Rect(item_x, item_y, 40, 40)

                    # Select item if clicked
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_inventory_item = item
                        return

                    # Drop button click
                    drop_rect = pygame.Rect(item_x, 65, 40, 20)
                    if item == self.selected_inventory_item and item.movable == "yes" and drop_rect.collidepoint(
                            mouse_pos):
                        item.picked_up = False
                        item.rect.topleft = item.previous_pos
                        self.items.append(item)
                        inventory.remove(item)
                        self.selected_inventory_item = None
                        return

        #No event-specific behavior here (yet) --> later add click detection logic
        #pass


    def update(self):
        self.cat.update()

    def draw_inventory(self):
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(self.screen, (INVENTORY_COLOR), (10, 10, 300, 80))  # inventory background
        pygame.draw.rect(self.screen, (INVENTORY_BORDER_COLOR), (10, 10, 300, 80), 2)  # border

        for i, item in enumerate(inventory):
            # Scale image for inventory display
            inventory_img = pygame.transform.scale(item.image, (45, 45))
            self.screen.blit(inventory_img, (20 + i * 60, 20))

            # Optional: item name below it
            text = font.render(item.name, True, (WHITE))
            self.screen.blit(text, (15 + i * 65, 65))

            # If selected, show drop option (only if movable)
            if self.selected_inventory_item == item and item.movable == "yes":
                drop_font = pygame.font.SysFont(None, 18)
                drop_text = drop_font.render("Drop", True, (255, 0, 0))
                item_x = 20 + i * 50  # <-- this must be inside the loop
                drop_rect = pygame.Rect(item_x, 65, 40, 20)
                pygame.draw.rect(self.screen, (50, 0, 0), drop_rect)
                self.screen.blit(drop_text, (item_x + 5, 67))

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





