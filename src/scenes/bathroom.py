from objects.item import create_items_for_room, INVENTORY_COLOR, INVENTORY_BORDER_COLOR, WHITE, INVENTORY_POSITION, ITEM_SPACING
from src.ui.helper import draw_inventory, draw_hover_message
import os
import pygame
from assets.media.text.fonts import get_big_font, get_small_font
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

        # invisible wall to prevent moving out of bounds
        self.left_wall = pygame.Rect(0, 0, 5, self.screen.get_height())

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
                        # Check if inventory is full before trying to pick up
                        if len(self.game.inventory) >= 4:  # INVENTORY_MAX
                            self.game.status_message = "Inventory is full. Drop something first."
                            self.game.message_timer = pygame.time.get_ticks()
                        else:
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
                                self.game.stats[item.stat] = self.game.stats.get(item.stat, 0) + item.effect
                            self.game.status_message = item.use_msg
                            self.game.message_timer = pygame.time.get_ticks()
                        else:
                            self.game.status_message = f"You already examined the {item.name}."
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
                        self.game.status_message = f"Dropped {item.name}."
                        self.game.message_timer = pygame.time.get_ticks()
                        return

    def update(self):
        self.cat.update()

        # Check collision with the invisible wall
        if self.cat.rect.colliderect(self.left_wall):
            self.cat.rect.left = self.left_wall.right

    def draw(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))
        self.game.hover_message = ""

        # Count collected toilet papers
        toilet_paper_count = sum(1 for inv_item in self.game.inventory if inv_item.name == "Toilet paper")

        # Draw items (only if not picked up)
        for item in self.items:
            if not item.picked_up:
                if item.name == "Cabinet":
                    # Cabinet appears only if at least 2 Toilet paper collected
                    if toilet_paper_count >= 2:
                        item.draw(self.screen)
                else:
                    item.draw(self.screen)

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw inventory if shown
        if self.game.show_inventory:
            draw_inventory(self.screen, self.game, self.selected_inventory_item)

            # Draw hover message if any
        draw_hover_message(self.screen, self.game)