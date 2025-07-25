import pygame
from scenes.living_room import LivingRoom
from scenes.bathroom import Bathroom
from scenes.garden import Garden
from ui.menu import MainMenu
from objects.player import Cat
from scenes.character_select import CharacterSelect

from objects.item import Item, load_test_image, inventory

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = "menu"  # start in menu
        self.menu = MainMenu(self)
        self.show_inventory = False
        self.hover_message = ""
        self.state = "character_select"  # new initial state
        self.character_select = CharacterSelect(self)
        self.living_room = None
        self.garden = None
        self.boss_fight = None

        # shared cat object reusable across scenes
        self.cat = None  # Will be set after character selection
        self.current_scene = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.state == "character_select":
                self.character_select.handle_event(event)
            elif self.state == "menu":
                if self.menu.start_button_rect.collidepoint(mouse_pos):
                    self.start_game()
            #elif für livingroom und garden und so?
                #elif self.state == "boss_fight" and self.boss_fight:
                    #self.boss_fight.handle_event(event)

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
        if self.cat is None:
            # fallback cat if none was selected
            self.cat = Cat(x=100, y=250, image_path="../assets/media/sprites/cat_sprite.png")
        self.current_scene = LivingRoom(self)
        self.cat.rect.x = self.screen.get_width() // 2
        self.cat.rect.y = 250
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
        if self.state == "character_select":
            self.character_select.draw()
        elif self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "playing":
            self.current_scene.draw()

        pygame.display.flip()