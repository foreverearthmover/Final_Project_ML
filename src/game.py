import pygame
from scenes.living_room import LivingRoom
from scenes.bathroom import Bathroom
from scenes.garden import Garden
from src.objects.item import create_items_for_room, rooms
from ui.menu import MainMenu
from objects.player import Cat, WHITE
from scenes.character_select import CharacterSelect  # Importing CharacterSelect
import os
from scenes.boss_fight import BossFight


class Game:
    def __init__(self, screen):
        self.status_message = ""
        self.used_items = set()
        self.inventory_items = set()
        self.screen = screen
        self.state = "character_select"  # Start with character select state
        self.cat = None
        self.current_scene = None
        self.show_inventory = False
        self.menu = MainMenu(self)
        self.character_select = CharacterSelect(self)  # Initialize CharacterSelect
        self.hover_message = ""
        self.current_room = None
        self.font = pygame.font.SysFont(None, 20)
        self.selected_character = None
        self.message_timer = 0

        # Initialize inventory
        self.inventory = []  # Add this line to initialize the inventory

        # Track items in each room
        self.rooms = {
            "living_room": create_items_for_room("Living room", self, movable=False),
            "bathroom": create_items_for_room("Bathroom", self, movable=False),
            "garden": create_items_for_room("Garden", self, movable=False),
        }

        # Load custom font
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, "..", "assets", "media", "fonts", "8-bit_wonder.TTF")
        font_path = os.path.normpath(font_path)
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found at: {font_path}")
        self.button_font = pygame.font.Font(font_path, 11)

        # Navigation buttons
        self.left_button = pygame.Rect(10, self.screen.get_height() - 40, 100, 30)
        self.right_button = pygame.Rect(self.screen.get_width() - 170, self.screen.get_height() - 40, 100, 30)

        # Room connections
        self.item_states = {}  # Dictionary to track item states across scenes
        self.room_exits = {
            "living_room": {"left": "bathroom", "right": "garden"},
            "bathroom": {"right": "living_room"},
            "garden": {"left": "living_room"}
        }
        self.stats = {"Health": 0, "Damage": 0, "Love": 0}

        # Recalculate stats from inventory
        for item in self.inventory:
            item.apply_effect(self)

    def start_game(self):
        if not self.cat:
            self.cat = Cat(x=100, y=270, image_path="../assets/media/sprites/Tofu.png", game = self)

        # Set up initial scene
        self.current_scene = LivingRoom(self)
        self.current_room = "living_room"
        self.state = "playing"

    def change_scene(self, scene_name, entry_side):
        # Position cat based on entry side
        if entry_side == "left":
            self.cat.rect.x = 50
        else:  # "right"
            self.cat.rect.x = self.screen.get_width() - 150

        self.cat.rect.y = 270
        self.current_room = scene_name

        # Create new scene
        if scene_name == "living_room":
            self.current_scene = LivingRoom(self)
        elif scene_name == "bathroom":
            self.current_scene = Bathroom(self)
        elif scene_name == "garden":
            self.current_scene = Garden(self)

    def handle_scene_transitions(self):
        screen_width = self.screen.get_width()
        cat = self.cat

        if self.current_room == "living_room":
            if cat.rect.right < 0:
                self.change_scene("bathroom", entry_side="right")
            elif cat.rect.left > screen_width:
                self.change_scene("garden", entry_side="left")

        elif self.current_room == "bathroom":
            if cat.rect.left > screen_width:
                self.change_scene("living_room", entry_side="left")

        elif self.current_room == "garden":
            # Prevent walking past boss cat
            if hasattr(self.current_scene, 'boss_cat') and cat.rect.right > self.current_scene.boss_cat.rect.left:
                cat.rect.right = self.current_scene.boss_cat.rect.left

            if cat.rect.right < 0:
                self.change_scene("living_room", entry_side="right")

   # unused
    def draw_navigation_buttons(self):
        if self.state != "playing" or not self.current_room:
            return

        available_exits = self.room_exits.get(self.current_room, {})

        def format_room_name(room_name):
            return room_name.replace("_", " ").title()  # Convert "living_room" to "Living Room"

        # Size
        self.left_button.width = 150
        self.left_button.height = 35
        self.right_button.width = 150
        self.right_button.height = 35

        # Colors
        button_bg_color_default = (180, 180, 180)
        button_bg_color_hover = (255, 255, 255)
        button_border_color = (100, 100, 100)
        button_text_color = (50, 50, 50)

        mouse_pos = pygame.mouse.get_pos()

        # Draw left button if there's a left exit
        if "left" in available_exits:
            left_color = button_bg_color_hover if self.left_button.collidepoint(mouse_pos) else button_bg_color_default
            pygame.draw.rect(self.screen, left_color, self.left_button, border_radius=10)

        # Border
            pygame.draw.rect(self.screen, button_border_color, self.left_button, width=2, border_radius=10)

        # Text
            text = self.button_font.render(f"To {format_room_name(available_exits['left'])}", True, button_text_color)
            text_rect = text.get_rect(center=self.left_button.center)
            self.screen.blit(text, text_rect)

        # Draw right button if there's a right exit
        if "right" in available_exits:
            right_color = button_bg_color_hover if self.right_button.collidepoint(mouse_pos) else button_bg_color_default
            pygame.draw.rect(self.screen, right_color, self.right_button, border_radius=10)

        # Border
            pygame.draw.rect(self.screen, button_border_color, self.right_button, width=2, border_radius=10)

        # Text
            text = self.button_font.render(f"To {format_room_name(available_exits['right'])}", True, button_text_color)
            text_rect = text.get_rect(center=self.right_button.center)
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if self.state == "character_select":
            self.character_select.handle_event(event)
        elif self.state == "menu":
            self.menu.handle_event(event)
        elif self.state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #available_exits = self.room_exits.get(self.current_room, {})

                #if "left" in available_exits and self.left_button.collidepoint(mouse_pos):
                    #self.change_scene(available_exits["left"], "right")
                #elif "right" in available_exits and self.right_button.collidepoint(mouse_pos):
                    #self.change_scene(available_exits["right"], "left")

            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Check for the "E" key
                    self.show_inventory = not self.show_inventory

            if self.current_scene:
                self.current_scene.handle_event(event)

    def update(self):
        if self.state == "character_select":
            self.character_select.update()
        elif self.state == "playing" and self.current_scene:
            self.current_scene.update()
            self.handle_scene_transitions()
        if self.state == "character_select":
            self.character_select.update()
        elif self.state == "playing" and self.current_scene:
            self.cat.update_sprite_if_bow_equipped()  # <-- check for bow
            self.current_scene.update()
            self.handle_scene_transitions()

    def has_bow(self):
        return any(item.name == "Bow" for item in self.inventory)

    def draw_stats(self):
            font = pygame.font.SysFont(None, 24)

            # Prepare each stat line separately
            lines = [
                f"Health: {self.stats['Health']}",
                f"Damage: {self.stats['Damage']}",
                f"Love: {self.stats['Love']}"
            ]

            x, y = 10, 10
            padding = 5
            line_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]

            # Determine background size based on all lines
            width = max(surface.get_width() for surface in line_surfaces)
            height = sum(surface.get_height() for surface in line_surfaces) + (padding * (len(lines) - 1))

            # Create background surface
            bg_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
            bg_surf.fill((0, 0, 0, 180))  # semi-transparent background
            self.screen.blit(bg_surf, (x - 5, y - 5))

            # Render each line
            for surface in line_surfaces:
                self.screen.blit(surface, (x, y))
                y += surface.get_height() + padding



    def draw(self):
        if self.state == "character_select":
            self.character_select.draw(self.screen)
        elif self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "playing" and self.current_scene:
            self.current_scene.draw()
            #self.draw_navigation_buttons()
            self.draw_stats()

            if self.show_inventory:
                self.current_scene.draw_inventory()

            if self.status_message:
                font = pygame.font.SysFont(None, 24)
                text_surface = font.render(self.status_message, True, WHITE)  # text
                text_rect = text_surface.get_rect()
                text_rect.topleft = (10, self.screen.get_height() - 420)  # adjust position as needed

                pygame.draw.rect(self.screen, (50, 120, 30), text_rect.inflate(10, 10))  # black background
                self.screen.blit(text_surface, text_rect)
                if self.status_message and pygame.time.get_ticks() - self.message_timer > 2000:
                    self.status_message = ""

    def update_stat(self, stat_name, value):
        if stat_name in self.cat.stats:
            self.cat.stats[stat_name] += value
            print(f"[STAT] {stat_name} updated to {self.cat.stats[stat_name]}")


