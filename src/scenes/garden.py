from src.objects.item import create_items_for_room, INVENTORY_COLOR, INVENTORY_BORDER_COLOR, INVENTORY_POSITION, ITEM_SPACING, WHITE
from src.ui.helper import draw_inventory, draw_hover_message, DROPBUTTON_POS_Y
import os
import pygame
import time
from pygame import mixer
from src.scenes.boss_fight import BossFight
from src.objects.boss_cat import BossCat
from src.objects.item import rooms
from assets.media.text.fonts import get_small_font
from src.objects.player import Cat

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

        # Load and setup animated squirrel
        squirrel_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "sprites", "Squirrel.png")
        #self.squirrel_sprite_sheet = pygame.image.load(os.path.normpath(squirrel_path)).convert_alpha()
        self.squirrel_sprite_sheet = pygame.image.load(os.path.normpath(squirrel_path)).convert()
        self.squirrel_sprite_sheet.set_colorkey((255, 255, 255))  # Remove white

        # Animation setup
        self.squirrel_frame_width = 975
        self.squirrel_frame_height = 1000
        self.squirrel_scale = 0.1
        self.squirrel_frame_count = 4
        self.squirrel_idle_frames = self.load_squirrel_frames()
        self.squirrel_walk_frames = self.load_squirrel_walk_frames()

        self.squirrel_current_frame = 0
        self.squirrel_animation_timer = 0
        self.squirrel_animation_delay = 400  # Milliseconds between frames
        self.squirrel_current_frames = self.squirrel_idle_frames  # Start with idle

        # Current squirrel image
        self.current_squirrel_image = self.squirrel_current_frames[0]

        # Get scaled dimensions for click rect
        scaled_width = self.squirrel_idle_frames[0].get_width()
        scaled_height = self.squirrel_idle_frames[0].get_height()
        self.squirrel_rect = pygame.Rect(
            self.screen.get_width() - scaled_width - 20,
            0,
            scaled_width,
            scaled_height
        )

        # Load squirrel idle frames
        self.squirrel_idle_frames = self.load_squirrel_frames()
        self.squirrel_current_frame = 0
        self.squirrel_animation_timer = 0
        self.squirrel_animation_delay = 100  # Milliseconds between frames

        # Current squirrel image
        self.current_squirrel_image = self.squirrel_idle_frames[0]

        # Squirrel attributes
        self.squirrel_rect = pygame.Rect(self.screen.get_width() - 300, self.screen.get_height() //2, 40, 40)
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

        #Timer for auto-Walk
        self.cat_walking_to_boss = False
        self.walk_start_time = 0
        self.walk_duration = 3000

    def load_squirrel_frames(self):
        #Load squirrel animation frames from sprite sheet
        frames = []
        for i in range(self.squirrel_frame_count):
            x = i * self.squirrel_frame_width
            frame = self.get_squirrel_frame(x, 0, self.squirrel_frame_width, self.squirrel_frame_height)
            frames.append(frame)
        return frames

    def load_squirrel_walk_frames(self):
        frames = []
        for i in range(4, 7):  # Frames 4, 5, 6 für Walk
            x = i * self.squirrel_frame_width
            frame = self.get_squirrel_frame(x, 0, self.squirrel_frame_width, self.squirrel_frame_height)
            frames.append(frame)
        return frames

    def get_squirrel_frame(self, x, y, width, height):
        #Extract single frame from squirrel sprite sheet
        frame = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        frame.blit(self.squirrel_sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))
        frame = pygame.transform.scale(frame, (int(width * self.squirrel_scale), int(height * self.squirrel_scale)))
        return frame

    def animate_squirrel(self):
        if not self.squirrel_visible:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.squirrel_animation_timer > self.squirrel_animation_delay:
            self.squirrel_animation_timer = current_time
            self.squirrel_current_frame = (self.squirrel_current_frame + 1) % len(self.squirrel_current_frames)
            self.current_squirrel_image = self.squirrel_current_frames[self.squirrel_current_frame]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle squirrel click
            click_rect = self.squirrel_rect.inflate(40, 40)  # make hitbox wider
            if self.squirrel_visible and click_rect.collidepoint(mouse_pos):
                self.squirrel_running = True
                #self.squirrel_visible = False  # optionally hide it immediately
                self.show_chase_button = False
                return  # prevent double-processing

            # Handle chase button click
            if self.show_chase_button and self.chase_button_rect.collidepoint(mouse_pos):
                self.cat.start_auto_walk_right()
                self.cat_walking_to_boss = True
                self.walk_start_time = pygame.time.get_ticks()
                self.show_chase_button = False

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

                    drop_rect = pygame.Rect(item_x, DROPBUTTON_POS_Y, 50, 20)
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
            # Switch to walk animation when running
            if self.squirrel_current_frames != self.squirrel_walk_frames:
                self.squirrel_current_frames = self.squirrel_walk_frames
                self.squirrel_current_frame = 0  # Reset frame index

            self.squirrel_rect.x += 5  #Squirrel runs to the right
            if self.squirrel_rect.left > self.screen.get_width():  # Squirrel off-screen
                self.squirrel_running = False
                self.squirrel_visible = False
                self.show_chase_button = True
                # Move wall to the far right so the cat can walk to the end
                self.right_wall.x = self.screen.get_width() - 10
        else:
            # Use idle animation when not running
            if self.squirrel_current_frames != self.squirrel_idle_frames:
                self.squirrel_current_frames = self.squirrel_idle_frames
                self.squirrel_current_frame = 0

        if self.cat_walking_to_boss:
            current_time = pygame.time.get_ticks()

            if current_time - self.walk_start_time > self.walk_duration:
                self.cat.stop_auto_walk()
                self.navigate_to_boss_area()
                self.cat_walking_to_boss = False

        # Update the player cat animation
        self.cat.update()
        # Animate squirrel
        self.animate_squirrel()

        # Update boss cat if visible
        if self.boss_cat_visible:
            self.boss_cat.update()

        # Check collision with wall
        if not self.cat.auto_walk_right and self.cat.rect.colliderect(self.right_wall):
            self.cat.rect.right = self.right_wall.left

    def navigate_to_boss_area(self):
        self.show_chase_button = False
        self.scroll_offset = self.background.get_width() // 2  # Pan camera right
        self.cat.rect.x = 50
        self.boss_cat.rect.topleft = (self.screen.get_width() - 250, self.cat.rect.y)
        self.boss_cat.start_chase()  # Trigger idle animation and visibility
        self.boss_cat_visible = True

    def draw(self):
        # Draw the background with the offset
        self.screen.blit(self.background, (-self.scroll_offset, 0))

        self.game.hover_message = ""

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw the squirrel if visible
        # Draw the animated squirrel if visible
        if self.squirrel_visible:
            self.screen.blit(self.current_squirrel_image, self.squirrel_rect)
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
            draw_inventory(self.screen, self.game, self.selected_inventory_item)

        # Draw hover message if any
        draw_hover_message(self.screen, self.game)