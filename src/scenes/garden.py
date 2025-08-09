from objects.item import create_items_for_room, INVENTORY_COLOR, INVENTORY_BORDER_COLOR,INVENTORY_POSITION, ITEM_SPACING,  WHITE
import os
import pygame
from pygame import mixer
from scenes.boss_fight import BossFight
from objects.boss_cat import BossCat, load_skin
from src.objects.item import rooms
from assets.media.text.fonts import get_big_font, get_small_font

mixer.init()
sound_path = os.path.join('..', 'assets', 'media', 'sounds', 'cat_hiss.mp3')
mixer.music.load(sound_path)
mixer.music.set_volume(0.7)

class Garden:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        self.boss_cat = BossCat()

        # Load items for the garden
        self.items = create_items_for_room("Garden", game=self.game, movable=False)

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
        self.boss_cat_visible = False
        self.boss_cat = BossCat()

        # invisible wall to prevent moving out of bounds
        self.right_wall = pygame.Rect(
            self.squirrel_rect.left - 10,
            0,
            10,
            self.screen.get_height()
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle squirrel click s
            if self.squirrel_visible and self.squirrel_rect.collidepoint(mouse_pos):
                self.squirrel_running = True
                #self.squirrel_visible = False  # optionally hide it immediately
                self.show_chase_button = False
                return  # prevent double-processing

            # Handle chase button click
            if self.show_chase_button and self.chase_button_rect.collidepoint(mouse_pos):
                self.navigate_to_boss_area()
                return

            # Click on boss cat to enter fight
            if self.boss_cat_visible and self.boss_cat.rect.collidepoint(mouse_pos):
                self.game.current_scene = BossFight(self.game)
                mixer.music.play()
                return

            # Handle item interactions
            for item in self.items:
                if item.rect.collidepoint(mouse_pos) and not item.picked_up:
                    item.try_pick_up()

            # Handle inventory interactions
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
                        self.game.inventory.remove(item)
                        self.selected_inventory_item = None
                        return


    def update(self):
        # Handle squirrel movement
        if self.squirrel_running:
            self.squirrel_rect.x += 5  # Squirrel runs to the right
            if self.squirrel_rect.left > self.screen.get_width():  # Squirrel off-screen
                self.squirrel_running = False
                self.squirrel_visible = False
                self.show_chase_button = True
                # Move wall to the far right so the cat can walk to the end
                self.right_wall.x = self.screen.get_width() - 10

        # Update the player cat animation
        self.cat.update()

        # Update boss cat if visible
        if self.boss_cat_visible:
            self.boss_cat.update()

        # Check collision with wall
        if self.cat.rect.colliderect(self.right_wall):
            self.cat.rect.right = self.right_wall.left

    def navigate_to_boss_area(self):
        self.show_chase_button = False
        self.scroll_offset = self.background.get_width() // 2  # Pan camera right
        self.cat.rect.x = 50
        self.boss_cat.rect.topleft = (self.screen.get_width() - 250, self.cat.rect.y)
        self.boss_cat.start_chase()  # Trigger idle animation and visibility
        self.boss_cat_visible = True

    def draw_inventory(self):
        # Draw the inventory panel
        font = get_small_font(9)
        pygame.draw.rect(self.screen, INVENTORY_COLOR, (INVENTORY_POSITION, 5, 350, 80))  # Inventory background
        pygame.draw.rect(self.screen, INVENTORY_BORDER_COLOR, (INVENTORY_POSITION, 5, 350, 80), 2)  # Border


        for i, item in enumerate(self.game.inventory):
            item_x = INVENTORY_POSITION + 20 + i * ITEM_SPACING
            inventory_img = pygame.transform.scale(item.image, (45, 45))
            self.screen.blit(inventory_img, (item_x, 20))

            # Item name
            text = font.render(item.name, True, (WHITE))
            self.screen.blit(text, (item_x, 65))

            # Drop button
            if self.selected_inventory_item == item and item.movable == "yes":
                drop_font = get_small_font(11)
                drop_text = drop_font.render("Drop", True, (255, 0, 0))
                drop_rect = pygame.Rect(item_x, 90, 50, 20)
                pygame.draw.rect(self.screen, (50, 0, 0), drop_rect)
                self.screen.blit(drop_text, (item_x + 5, 93))

    def draw(self):
        # Draw the background with the offset
        self.screen.blit(self.background, (-self.scroll_offset, 0))

        self.game.hover_message = ""

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw the squirrel if visible
        if self.squirrel_visible:
            pygame.draw.rect(self.screen, (165, 42, 42), self.squirrel_rect)  # Red rectangle as squirrel

        if self.show_chase_button:
            button_surface = pygame.Surface(self.chase_button_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(button_surface, (0, 0, 0, 180), button_surface.get_rect(), border_radius=10)
            self.screen.blit(button_surface, self.chase_button_rect.topleft)
            pygame.draw.rect(self.screen, (255, 255, 255), self.chase_button_rect, width=2, border_radius=10)

            self.button_font = get_small_font()
            chase_text = self.button_font.render("CHASE?", True, (255, 255, 255))
            text_rect = chase_text.get_rect(center=self.chase_button_rect.center)
            self.screen.blit(chase_text, text_rect)

        # Draw items (only if not picked up)
        for item in self.items:
            if not item.picked_up:
                item.draw(self.screen)

        if self.boss_cat_visible:
            self.boss_cat.draw(self.screen)

        self.cat.draw(self.screen)

        # Draw inventory if shown
        if self.game.show_inventory:
            self.draw_inventory()

        # Draw hover message if any
        self.draw_hover_message()

    def draw_hover_message(self):
        if hasattr(self.game, "hover_message") and self.game.hover_message:
            font = get_small_font(12)
            msg_surface = font.render(self.game.hover_message, True, (255, 255, 255))
            bg_rect = msg_surface.get_rect(topleft=(self.screen.get_width() / 4, self.screen.get_height() - 30))
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect.inflate(10, 10))
            self.screen.blit(msg_surface, bg_rect)

