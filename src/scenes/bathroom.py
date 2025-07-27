from objects.item import create_items_for_room, inventory, INVENTORY_COLOR, INVENTORY_BORDER_COLOR, WHITE
import os
import pygame

class Bathroom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        # Load items for the room
        self.items = create_items_for_room("Bathroom", game=self.game)

        # Update item states based on the global state in `self.game.item_states`
        for item in self.items:
            if item.name in self.game.item_states:
                item.picked_up = self.game.item_states[item.name]
            else:
                self.game.item_states[item.name] = item.picked_up

        self.selected_inventory_item = None

        # Background image
        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "bathroom.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()

    def handle_event(self, event):
        # Handle item interactions
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Click on items in the room
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()

            # Click in the inventory
            if self.game.show_inventory:
                for i, item in enumerate(inventory):
                    item_x = 20 + i * 50
                    item_y = 20
                    item_rect = pygame.Rect(item_x, item_y, 40, 40)

                    # Select item if clicked
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_inventory_item = item
                        return

                    # Drop item if clicking "drop" button
                    drop_rect = pygame.Rect(item_x, 65, 40, 20)
                    if item == self.selected_inventory_item and item.movable == "yes" and drop_rect.collidepoint(
                            mouse_pos):
                        item.picked_up = False
                        self.game.item_states[item.name] = False
                        item.rect.topleft = item.previous_pos
                        self.items.append(item)
                        inventory.remove(item)
                        self.selected_inventory_item = None
                        return

    def update(self):
        self.cat.update()

    def draw_inventory(self):
        # Draw the inventory UI
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(self.screen, INVENTORY_COLOR, (10, 10, 300, 80))  # Inventory background
        pygame.draw.rect(self.screen, INVENTORY_BORDER_COLOR, (10, 10, 300, 80), 2)  # Border

        for i, item in enumerate(inventory):
            # Scale item image for inventory
            inventory_img = pygame.transform.scale(item.image, (45, 45))
            self.screen.blit(inventory_img, (20 + i * 60, 20))

            # Optional: Draw the item's name
            text = font.render(item.name, True, WHITE)
            self.screen.blit(text, (15 + i * 65, 65))

            # Show "Drop" button for selected item
            if self.selected_inventory_item == item and item.movable == "yes":
                drop_font = pygame.font.SysFont(None, 18)
                drop_text = drop_font.render("Drop", True, (255, 0, 0))
                item_x = 20 + i * 50
                drop_rect = pygame.Rect(item_x, 65, 40, 20)
                pygame.draw.rect(self.screen, (50, 0, 0), drop_rect)
                self.screen.blit(drop_text, (item_x + 5, 67))

    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Draw items (only if not picked up)
        for item in self.items:
            if not item.picked_up:
                item.draw(self.screen)

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw inventory if shown
        if self.game.show_inventory:
            self.draw_inventory()