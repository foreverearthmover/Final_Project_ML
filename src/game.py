import pygame
from scenes.living_room import LivingRoom
from scenes.bathroom import Bathroom
from scenes.garden import Garden
from ui.menu import MainMenu
from objects.player import Cat
from scenes.character_select import CharacterSelect  # Importing CharacterSelect
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "character_select"  # Start with character select state
        self.cat = None
        self.current_scene = None
        self.show_inventory = False
        self.menu = MainMenu(self)
        self.character_select = CharacterSelect(self)  # Initialize CharacterSelect
        self.hover_message = ""
        self.current_room = None
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

        # Navigation buttons
        #self.button_font = pygame.font.SysFont(None, 24)
        #self.left_button = pygame.Rect(10, self.screen.get_height() - 40, 100, 30)
        #self.right_button = pygame.Rect(self.screen.get_width() - 140, self.screen.get_height() - 40, 100, 30)

        # Room connections
        self.room_exits = {
            "living_room": {"left": "bathroom", "right": "garden"},
            "bathroom": {"right": "living_room"},
            "garden": {"left": "living_room"}
        }

    def start_game(self):
        if not self.cat:
            self.cat = Cat(x=100, y=250, image_path="../assets/media/sprites/Tofu.png")

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

        self.cat.rect.y = 250
        self.current_room = scene_name

        # Create new scene
        if scene_name == "living_room":
            self.current_scene = LivingRoom(self)
        elif scene_name == "bathroom":
            self.current_scene = Bathroom(self)
        elif scene_name == "garden":
            self.current_scene = Garden(self)

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
                available_exits = self.room_exits.get(self.current_room, {})

                if "left" in available_exits and self.left_button.collidepoint(mouse_pos):
                    self.change_scene(available_exits["left"], "right")
                elif "right" in available_exits and self.right_button.collidepoint(mouse_pos):
                    self.change_scene(available_exits["right"], "left")

            if self.current_scene:
                self.current_scene.handle_event(event)

    def update(self):
        if self.state == "character_select":
            self.character_select.update()
        elif self.state == "playing" and self.current_scene:
            self.current_scene.update()

    def draw(self):
        if self.state == "character_select":
            self.character_select.draw()
        elif self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "playing" and self.current_scene:
            self.current_scene.draw()
            self.draw_navigation_buttons()

            if self.show_inventory:
                self.current_scene.draw_inventory()

