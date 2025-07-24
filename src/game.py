import pygame
from scenes.living_room import LivingRoom
from scenes.bathroom import Bathroom
from scenes.garden import Garden
from ui.menu import MainMenu
from objects.player import Cat
from objects.item import Item, load_test_image, inventory

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"  # start in menu
        self.menu = MainMenu(self)
        self.show_inventory = False
        # shared cat object reusable across scenes
        self.cat = Cat(x=100, y=250)
        self.current_scene = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.state == "menu":
                if self.menu.start_button_rect.collidepoint(mouse_pos):
                    self.start_game()
                elif self.menu.quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
        
        if self.state == "playing":
            self.current_scene.handle_event(event)
            
            # Global input (for all scenes)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show_inventory = not self.show_inventory

    # called when starting the game from menu
    def start_game(self):
        self.state = "playing"
        self.current_scene = LivingRoom(self)
        self.cat.rect.x = self.screen.get_width() // 2  # Center the cat
        self.cat.rect.y = 250  # Fixed Y position

    # supposed to change to a new scene
    # entry_side: "left" or "right" - which side cat enters from
    # basically does nothing so far
    def change_scene(self, scene_name, entry_side):

        # set cat position based on entry side
        if entry_side == "left":
            self.cat.rect.x = 50  # slight offset from left
        else:  # "right"
            self.cat.rect.x = self.screen.get_width() - 50 - self.cat.rect.width  # Slight offset from right

        # create new scene
        if scene_name == "living_room":
            self.current_scene = LivingRoom(self)
        elif scene_name == "bathroom":
            self.current_scene = Bathroom(self)
        elif scene_name == "garden":
            self.current_scene = Garden(self)

    def update(self):
        if self.state == "playing":
            self.current_scene.update()

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "playing":
            self.current_scene.draw()