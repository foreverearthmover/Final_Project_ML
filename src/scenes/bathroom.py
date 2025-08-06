from objects.item import create_items_for_room, INVENTORY_COLOR, INVENTORY_BORDER_COLOR, WHITE, INVENTORY_POSITION, ITEM_SPACING
import os
import pygame

from src.objects.item import rooms


class Bathroom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        # Load items for the room
        self.items = create_items_for_room("Bathroom", game=self.game, movable=False)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check clicks on items in the world
            for item in self.items:
                if item.rect.collidepoint(mouse_pos):
                    # Special case for Cabinet: always call check_click to use its custom logic
                    if item.name == "Cabinet":
                        item.check_click(mouse_pos)
                        break
                    elif item.movable == "yes" and not item.picked_up and item not in self.game.inventory:
                        item.try_pick_up()
                        self.game.status_message = f"Picked up {item.name}."
                        self.game.message_timer = pygame.time.get_ticks()
                    elif item.movable == "yes" and item in self.game.inventory:
                        self.game.status_message = f"You already picked up {item.name}."
                        self.game.message_timer = pygame.time.get_ticks()
                    elif item.movable == "no":
                        if item.name not in self.game.used_items:
                            self.game.used_items.add(item.name)
                            if item.stat != "none":
                                self.game.stats[item.stat] += item.effect
                            self.game.status_message = item.use_msg
                            self.game.message_timer = pygame.time.get_ticks()
                        else:
                            self.game.status_message = f"You already used {item.name}."
                            self.game.message_timer = pygame.time.get_ticks()
                    break

            # Inventory interactions
            if self.game.show_inventory:
                for i, item in enumerate(self.game.inventory):
                    item_x = INVENTORY_POSITION + 20 + i * ITEM_SPACING
                    item_rect = pygame.Rect(item_x, 20, 40, 40)

                    if item_rect.collidepoint(mouse_pos):
                        self.selected_inventory_item = item
                        return

                    drop_rect = pygame.Rect(item_x, 90, 50, 20)
                    if (
                            item == self.selected_inventory_item
                            and item.movable == "yes"
                            and drop_rect.collidepoint(mouse_pos)
                    ):
                        # Drop logic
                        item.picked_up = False
                        self.game.item_states[item.name] = False

                        # Undo stats if applicable
                        if item.stat != "none":
                            self.game.stats[item.stat] -= item.effect

                        # Assign item back to its original room
                        for room_name, room_items in rooms.items():
                            if any(room_item["item"] == item.name for room_item in room_items):
                                target_room_items = self.game.rooms.get(
                                    room_name.lower().replace(" ", "_"), []
                                )
                                target_room_items.append(item)
                                break

                        self.game.inventory.remove(item)
                        self.selected_inventory_item = None
                        self.game.status_message = f"Dropped {item.name}."
                        self.game.message_timer = pygame.time.get_ticks()
                        return

    def update(self):
        self.cat.update()

    def draw_inventory(self):
        # Draw the inventory UI
        font = pygame.font.SysFont(None, 20)
        pygame.draw.rect(self.screen, INVENTORY_COLOR, (INVENTORY_POSITION, 5, 350, 80))  # Inventory background
        pygame.draw.rect(self.screen, INVENTORY_BORDER_COLOR, (INVENTORY_POSITION, 5, 350, 80), 2)  # Border

        ITEM_SPACING = 80  # Space between items

        for i, item in enumerate(self.game.inventory):
            item_x = INVENTORY_POSITION + 20 + i * ITEM_SPACING
            inventory_img = pygame.transform.scale(item.image, (45, 45))
            self.screen.blit(inventory_img, (item_x, 20))

            # Item name
            text = font.render(item.name, True, (WHITE))
            self.screen.blit(text, (item_x, 65))

            # Drop button
            if self.selected_inventory_item == item and item.movable == "yes":
                drop_font = pygame.font.SysFont(None, 18)
                drop_text = drop_font.render("Drop", True, (255, 0, 0))
                drop_rect = pygame.Rect(item_x, 90, 50, 20)
                pygame.draw.rect(self.screen, (50, 0, 0), drop_rect)
                self.screen.blit(drop_text, (item_x + 5, 93))


    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        self.game.hover_message = ""

        # Draw items (only if not picked up)
        for item in self.items:
            if not item.picked_up:
                item.draw(self.screen)

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw inventory if shown
        if self.game.show_inventory:
            self.draw_inventory()

            # Draw hover message if any
        self.draw_hover_message()

    def draw_hover_message(self):
        if hasattr(self.game, "hover_message") and self.game.hover_message:
            font = pygame.font.SysFont(None, 20)
            msg_surface = font.render(self.game.hover_message, True, (255, 255, 255))
            bg_rect = msg_surface.get_rect(topleft=(self.screen.get_width() / 4, self.screen.get_height() - 30))
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect.inflate(10, 10))
            self.screen.blit(msg_surface, bg_rect)

