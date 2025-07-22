import pygame
from scenes.living_room import LivingRoom
from ui.menu import MainMenu
from objects.player import Cat

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"  # start in menu

        self.menu = MainMenu(self)

        self.living_room = None

        # shared cat object reusable across scenes
        self.cat = Cat(x=100, y=250) # adjust

        #ignore for now:
        #self.inventory = []
        #self.scene_name = "living_room"
        #self.scenes = {
            #"living_room": LivingRoom(self)
        #}


    def handle_event(self, event):
        if self.state == "menu":
            self.menu.handle_event(event)
        elif self.state == "living_room":
            self.living_room.handle_event(event)
        # add bathroom, garden, game over screens
        #elif self.state == "playing":
            #self.scenes[self.scene_name].handle_event(event)

    def update(self):
        if self.state == "menu":
            pass
        elif self.state == "living_room":
            if not self.living_room:
                self.living_room = LivingRoom(self)
            self.living_room.update()
        #if self.state == "playing":
        #self.scenes[self.scene_name].update()

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "living_room":
            self.living_room.draw()
        #elif self.state == "playing":
            #self.scenes[self.scene_name].draw()
