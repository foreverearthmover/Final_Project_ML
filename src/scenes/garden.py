from objects.item import create_items_for_room, inventory, INVENTORY_COLOR, INVENTORY_BORDER_COLOR, WHITE
import os
import pygame

from src.objects.item import rooms


class Garden:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        self.button_font = game.button_font  # Use same font as in game

        # Load items for the garden
        self.items = create_items_for_room("Garden", game=self.game)

        # Update item states based on the global state in `self.game.item_states`
        for item in self.items:
            if item.name in self.game.item_states:
                item.picked_up = self.game.item_states[item.name]
            else:
                self.game.item_states[item.name] = item.picked_up

        self.selected_inventory_item = None

        # Load the garden background
        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "garden.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()
        self.scroll_offset = 0

        # Squirrel attributes
        self.squirrel_rect = pygame.Rect(self.screen.get_width() - 200, self.screen.get_height() // 2, 40, 40)
        self.squirrel_visible = True
        self.squirrel_running = False

        # Chase button attributes
        self.chase_button_rect = pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() - 50, 150, 40)
        self.show_chase_button = False

        # Boss cat scene attributes
        self.boss_cat_rect = pygame.Rect(0, self.cat.rect.y, 40, 40)
        self.boss_cat_visible = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle squirrel click
            if self.squirrel_visible and self.squirrel_rect.collidepoint(mouse_pos):
                self.squirrel_running = True

            # Handle chase button click
            if self.show_chase_button and self.chase_button_rect.collidepoint(mouse_pos):
                self.navigate_to_boss_area()

            # Handle item interactions in the garden
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()

            # Handle inventory interactions
            if self.game.show_inventory:
                for i, item in enumerate(inventory):
                    item_x = 20 + i * 50
                    item_y = 20
                    item_rect = pygame.Rect(item_x, item_y, 40, 40)

                    # Select item in inventory
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_inventory_item = item
                        return

                    # Drop item if clicking "drop" button
                    drop_rect = pygame.Rect(item_x, 65, 40, 20)
                    if (
                        item == self.selected_inventory_item
                        and item.movable == "yes"
                        and drop_rect.collidepoint(mouse_pos)
                    ):
                        # Mark item as not picked up
                        item.picked_up = False
                        self.game.item_states[item.name] = False

                        # Assign item back to its original room
                        for room_name, room_items in rooms.items():
                            if any(room_item["item"] == item.name for room_item in room_items):
                                target_room_items = self.game.rooms.get(
                                    room_name.lower().replace(" ", "_"), []
                                )
                                target_room_items.append(item)
                                break  # Stop searching once the correct room is found

                        # Remove item from inventory and reset selection
                        inventory.remove(item)
                        self.selected_inventory_item = None
                        return


    def update(self):
        # Handle the squirrel running off-screen
        if self.squirrel_running:
            self.squirrel_rect.x += 5  # Squirrel runs to the right
            if self.squirrel_rect.left > self.screen.get_width():  # If squirrel goes off-screen
                self.squirrel_running = False
                self.squirrel_visible = False
                self.show_chase_button = True  # Show the chase button

        # Update the player cat animation
        self.cat.update()

    def navigate_to_boss_area(self):
        # Hide chase button and transition to the boss scene
        self.show_chase_button = False
        self.scroll_offset = self.background.get_width() // 2  # Move to the second half of the background
        self.cat.rect.x = 50  # Place cat near the left side of the screen
        self.boss_cat_visible = True
        self.boss_cat_rect.x = self.screen.get_width() - 100  # Boss cat appears on the right side

    def draw_inventory(self):
        # Draw the inventory panel
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(self.screen, INVENTORY_COLOR, (10, 10, 300, 80))  # Inventory background
        pygame.draw.rect(self.screen, INVENTORY_BORDER_COLOR, (10, 10, 300, 80), 2)  # Border

        for i, item in enumerate(inventory):
            inventory_img = pygame.transform.scale(item.image, (45, 45))
            self.screen.blit(inventory_img, (20 + i * 60, 20))

            text = font.render(item.name, True, WHITE)
            self.screen.blit(text, (15 + i * 65, 65))

            if self.selected_inventory_item == item and item.movable == "yes":
                drop_font = pygame.font.SysFont(None, 18)
                drop_text = drop_font.render("Drop", True, (255, 0, 0))
                item_x = 20 + i * 50
                drop_rect = pygame.Rect(item_x, 65, 40, 20)
                pygame.draw.rect(self.screen, (50, 0, 0), drop_rect)
                self.screen.blit(drop_text, (item_x + 5, 67))

    def draw(self):
        # Draw the background with the offset
        self.screen.blit(self.background, (-self.scroll_offset, 0))

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw the squirrel if visible
        if self.squirrel_visible:
            pygame.draw.rect(self.screen, (165, 42, 42), self.squirrel_rect)  # Red rectangle as squirrel

        # Draw the boss cat if visible
        if self.boss_cat_visible:
            pygame.draw.rect(self.screen, (0, 0, 255), self.boss_cat_rect)  # Blue rectangle as boss cat

        # Draw chase button
        if self.show_chase_button:
            pygame.draw.rect(self.screen, (200, 200, 200), self.chase_button_rect, border_radius=10)
            chase_text = self.button_font.render("Chase", True, (0, 0, 0))
            text_rect = chase_text.get_rect(center=self.chase_button_rect.center)
            self.screen.blit(chase_text, text_rect)

        # Draw items (only if not picked up)
        for item in self.items:
            if not item.picked_up:
                item.draw(self.screen)

        # Draw inventory if shown
        if self.game.show_inventory:
            self.draw_inventory()