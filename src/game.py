#from scenes.living_room import LivingRoom
from ui.menu import MainMenu

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"  # start in menu
        #self.inventory = []
        #self.cat = None
        #self.scene_name = "living_room"
        #self.scenes = {
            #"living_room": LivingRoom(self)
        #}
        self.menu = MainMenu(self)

    def handle_event(self, event):
        if self.state == "menu":
            self.menu.handle_event(event)
        #elif self.state == "playing":
            #self.scenes[self.scene_name].handle_event(event)

    def update(self):
        pass
        #if self.state == "playing":
        #self.scenes[self.scene_name].update()

    def draw(self):
        if self.state == "menu":
            self.menu.draw(self.screen)
        #elif self.state == "playing":
            #self.scenes[self.scene_name].draw()
