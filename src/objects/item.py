import pygame
import os

#Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'assets'))
INVENTORY_MAX = 4
IMAGE_SCALE = 1
WHITE = (255, 255, 255)
INVENTORY_COLOR = (155, 103, 60)
INVENTORY_BORDER_COLOR = (245,222,179)

#Inventory
inventory = []

#dictonary of what is inside the rooms
rooms = {
    "Living room":[
        {"item": "Cat tree", "movable": "no", "use": "attack boost", "msg": "You could sharpen your claws on this.", "x": 395, "y": 130},
        {"item": "Couch", "movable": "no", "use": "health", "msg": "You could lie down on the couch and take a nap.","x": 60, "y": 145},
        {"item": "Food bowl", "movable": "no", "use": "none", "msg": "The bowl is empty, but you are still hungry.","x": 526, "y": 405},
        {"item": "Carton", "movable": "no", "use": "key ", "msg": "You could go inside, or maybe on top?","x": 232, "y": 398},
        {"item": "Cable", "movable": "yes", "use": "attack", "msg": "These look knotted, be careful to not get caught.","x": 311, "y": 434},
        {"item": "Yarn ball", "movable": "yes", "use": "attack", "msg": "That looks fun! But lets not get distracted right now.","x": 500, "y": 238 },
        #do we add a message?
    ],
    "Bathroom":[
        {"item": "Toilet", "movable": "no", "use": "none", "msg": "That is a Toilet." ,"x": 100, "y": 100},
        {"item": "Shower", "movable": "no", "use": "none", "msg": "She is still in the shower, but you can't wait to eat." ,"x": 100, "y": 100},
        {"item": "Cat litter", "movable": "yes", "use": "none", "msg": "I don't need to go right now." ,"x": 100, "y": 100},
        {"item": "Toilet paper", "movable": "yes", "use": "attack", "msg": "You could push over the tower.. Or maybe just take one." ,"x": 100, "y": 100},
    ],
    "Garden":[
        {"item": "Squirrel", "movable": "no", "use": "Scene change", "msg": "You could try to catch that Squirrel!" ,"x": 100, "y": 100},
        {"item": "Boss Cat", "movable": "no", "use": "interact", "msg": "Other cat bad." ,"x": 100, "y": 100},
    ]
}




class Item:
    def __init__(self, name, pos, image, scale, game):
        width = image.get_width()
        height = image.get_height()
        self.game = game
        self.name = name
        self.scale = scale
        self.previous_pos = pos
        self.movable = self.get_movable_status(name)
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=pos)
        self.picked_up = False
        self.clicked = False
        self.msg = self.get_msg_for_item(name)
        self.mouse_was_pressed = True  # Track initial mouse state

    def get_msg_for_item(self, name):
        for room_items in rooms.values():
            for item in room_items:
                if item ['item'] == name:
                    return item ['msg']
        return None

    def try_pick_up(self):
        if self.movable == "yes":
            if len(inventory) < INVENTORY_MAX:
                self.picked_up = True
                inventory.append(self)
                print(f"You picked up [Item: {self.name}]")
            else:
                print("Inventory full. Drop something first.")
        else:
            print(f"[{self.name}] is not movable and cannot be picked up.")


    def draw(self, screen):
        #only show item if not in inventory
        if not self.picked_up:
            screen.blit(self.image, self.rect)

        #mouse hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            print(self.msg) #supposed to show the message predifned in the dic when hovering

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_pressed:
            self.mouse_was_pressed = False

        if not mouse_pressed:
            self.clicked = False

        #make things be clickable multiple times
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(mouse_pos) and not self.picked_up:
            self.game.hover_message = self.msg

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def get_movable_status(self, name):
        for room_items in rooms.values():
            for item in room_items:
                if item['item'] == name:
                    return item['movable']
        return "no"


#testing


def load_test_image(item_name):
    path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'assets', 'media', 'Items', f"{item_name}.png"
    )
    path = os.path.normpath(path)
    return pygame.image.load(path).convert_alpha()


# Function to create items from dic
def create_items_for_room(room_name, game):
    item_list = []
    if room_name in rooms:
        for item_data in rooms[room_name]:
            name = item_data["item"]
            try:
                image = load_test_image(name)
            except FileNotFoundError:
                print(f"[Warning] No pic found for {name}")
                continue

            x = item_data.get("x", 100)
            y = item_data.get("y", 100)

            item = Item(name, (x, y), image, IMAGE_SCALE, game)
            item_list.append(item)
        return item_list