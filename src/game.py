from scenes.living_room import LivingRoom
from scenes.bathroom import Bathroom
from scenes.garden import Garden

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.inventory = []
        self.cat = None  # will be passed to each scene
        self.scene_name = "living_room"
        self.scenes = {
            "living_room": LivingRoom(self),
            "bathroom": Bathroom(self),
            "garden": Garden(self)
        }

    def handle_event(self, event):
        self.scenes[self.scene_name].handle_event(event)

    def update(self):
        self.scenes[self.scene_name].update()

    def draw(self):
        self.scenes[self.scene_name].draw()
