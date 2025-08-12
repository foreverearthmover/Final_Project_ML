from objects.player import Cat
from src.ui.helper import draw_inventory, draw_hover_message
import os
import pygame
from objects.item import Item, load_test_image, create_items_for_room, INVENTORY_COLOR,  INVENTORY_BORDER_COLOR, INVENTORY_POSITION, ITEM_SPACING, WHITE #!!!
from objects.item import create_items_for_room
from assets.media.text.fonts import get_big_font, get_small_font
from src.objects.item import rooms


#Hello I have to edit a couple things since the Items will be in this room, I will mark everything I add
class LivingRoom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        # Load items for the room
        self.items = create_items_for_room("Living room", game=self.game, movable=False)

        # Update item states based on the global state in self.game.item_states
        for item in self.items:
            if item.name in self.game.item_states:
                item.picked_up = self.game.item_states[item.name]
            else:
                self.game.item_states[item.name] = item.picked_up

        self.selected_inventory_item = None

        path = os.path.join("..", "assets", "media", "backgrounds", "living_room.png")
        self.background = pygame.image.load(path).convert()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print("Mouse clicked at:", mouse_pos)

            # Check clicks on items in the world
            for item in self.items:
                if item.rect.collidepoint(mouse_pos):
                    if not item.picked_up and item.movable == "yes":
                        # Pick up item
                        if not item.picked_up and item.movable == "yes":
                            # Check if inventory is full before trying to pick up
                            if len(self.game.inventory) >= 4:  # INVENTORY_MAX
                                self.game.status_message = "Inventory is full. Drop something first."
                                self.game.message_timer = pygame.time.get_ticks()
                            else:
                                item.try_pick_up()
                                self.game.inventory_items.add(item.name)
                                self.game.status_message = f"Picked up the {item.name}."
                                self.game.message_timer = pygame.time.get_ticks()



                    elif item.movable == "no":
                        # Use static/non-movable item
                        if item.name not in self.game.used_items:
                            self.game.used_items.add(item.name)

                            if item.stat != "none":
                                self.game.stats[item.stat] = self.game.stats.get(item.stat, 0) + item.effect

                            self.game.status_message = item.use_msg
                            self.game.message_timer = pygame.time.get_ticks()
                        else:
                            self.game.status_message = f"You already used the {item.name}."
                            self.game.message_timer = pygame.time.get_ticks()

            # Check inventory interactions
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

                    # Undo stats if applicable (prevent negative values)
                    if item.stat != "none":
                        current_stat = self.game.stats.get(item.stat, 0)
                        self.game.stats[item.stat] = max(0, current_stat - item.effect)

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
                    return

    def update(self):
        self.cat.update()

    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))

        # Reset the hover message
        self.game.hover_message = ""

        # Only draw items that are not picked up
        for item in self.items:
            if not item.picked_up:
                item.draw(self.screen)

        # Draw the cat
        self.cat.draw(self.screen)

        # If inventory is shown, draw it
        if self.game.show_inventory:
            draw_inventory(self.screen, self.game, self.selected_inventory_item)

        # Draw hover message if any
        draw_hover_message(self.screen, self.game)