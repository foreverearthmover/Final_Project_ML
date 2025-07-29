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
INVENTORY_POSITION = 100
ITEM_SPACING = 80

#Inventory
inventory = []

#dictonary of what is inside the rooms
rooms = {
    "Living room":[
        {"item": "Cat tree", "movable": "no", "stat": "Damage", "effect": 3, "msg": "You could sharpen your claws on this.", "use": "test", "x": 395, "y": 130},
        {"item": "Couch", "movable": "no", "stat": "Health", "effect": 3, "msg": "You could lie down on the couch and take a nap.", "use": "test","x": 60, "y": 145},
        {"item": "Food bowl", "movable": "no", "stat": "none", "effect": 0, "msg": "The bowl is empty, but you are still hungry.", "use": "test","x": 526, "y": 405},
        {"item": "Carton", "movable": "no", "stat": "Health", "effect": 1,"msg": "You could go inside, or maybe on top?", "use": "test","x": 232, "y": 398},
        {"item": "Cable", "movable": "yes", "stat": "Damage", "effect": 1,"msg": "These look knotted, be careful to not get caught.", "use": "test","x": 311, "y": 434},
        {"item": "Yarn ball", "movable": "yes", "stat": "Damage","effect": 1, "msg": "That looks fun! But lets not get distracted right now.", "use": "test","x": 500, "y": 238 },
        #do we add a message?
    ],
    "Bathroom":[
        {"item": "Toilet", "movable": "no", "stat": "none","effect": 0, "msg": "That is a Toilet." , "use": "test", "x": 467, "y": 137},
        {"item": "Shower", "movable": "no", "stat": "none", "effect": 0,"msg": "She is still in the shower, but you can't wait to eat." , "use": "test", "x": 0, "y": 0},
        {"item": "Cat litter", "movable": "yes", "stat": "none", "effect": 0,"msg": "I don't need to go right now." , "use": "test", "x": 10, "y": 425},
        {"item": "Toilet paper", "movable": "yes", "stat": "Damage", "effect": 1,"msg": "You could push over the tower.. Or maybe just take one." , "use": "test", "x": 430, "y": 290},
        {"item": "Bow", "movable": "yes", "stat": "Love", "effect": 1,"msg": "What a pretty Bow" , "use": "test", "x": 430, "y": 290}
    ],
    "Garden":[
        {"item": "Squirrel", "movable": "no", "stat": "Scene change", "effect": 0, "msg": "You could try to catch that Squirrel!" , "use": "test", "x": 100, "y": 100},
        {"item": "Boss Cat", "movable": "no", "stat": "Boss fight", "effect": 0,"msg": "Other cat bad." , "use": "test", "x": 100, "y": 100},
    ]
}




class Item:
    def __init__(self, name, pos, image, scale, game, movable = True):
        self.name = name
        self.x, self.y = pos
        self.game = game
        self.scale = scale
        self.collected = False

        self.previous_pos = pos
        self.movable = self.get_movable_status(name)
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=pos)
        self.picked_up = False
        self.clicked = False
        self.msg = self.get_msg_for_item(name)
        self.use = self.get_use_for_item(name)
        self.mouse_was_pressed = True  # Track initial mouse state

        # Get item data from dictionary

        item_data = None
        for room_items in rooms.values():
            for item in room_items:
                if item["item"] == name:
                    item_data = item
                    break
            if item_data:
                break

        self.movable = item_data.get("movable", True) if item_data else True
        self.stat = item_data.get("stat", None) if item_data else None
        self.effect = item_data.get("effect", 0) if item_data else 0

        for item in inventory:
            print(item)

    def apply_effect(self, game):
        if self.stat and self.stat != "none" and not self.used:
            game.stats[self.stat] = game.stats.get(self.stat, 0) + self.effect
            self.used = True  # prevent re-use

    def get_msg_for_item(self, name: object) -> str | int | None:
        for room_items in rooms.values():
            for item in room_items:
                if item ['item'] == name:
                    return item ['msg']
        return None

    def get_use_for_item(self, name: object) -> str | int | None:
        for room_items in rooms.values():
            for item in room_items:
                if item["item"] == name:
                    return item ["use"]

    def try_pick_up(self):
        if self.movable == "yes":
            if len(inventory) < INVENTORY_MAX:
                self.picked_up = True
                inventory.append(self)
                self.game.item_states[self.name] = True  # Update global state
                print(f"You picked up [Item: {self.name}]")
            else:
                print("Inventory full. Drop something first.")
        else:
            print(f"[{self.name}] is not movable and cannot be picked up.")


    def draw(self, screen):
        # Only draw the item if it is not picked up
        if not self.picked_up:
            screen.blit(self.image, self.rect)

        # Handle mouse hovering (optional based on your logic)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.picked_up:
            self.game.hover_message = self.msg

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



    def use(self):
        if self.stat and not self.movable:  # Only use non-movable items
            print(f"[USE] {self.name} used. +{self.effect} {self.stat}")
            self.game.update_stat(self.stat, self.effect)

#testing


def load_test_image(item_name):
    path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'assets', 'media', 'Items', f"{item_name}.png"
    )
    path = os.path.normpath(path)
    return pygame.image.load(path).convert_alpha()


# Function to create items from dic
def create_items_for_room(room_name, game, movable):
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



            movable = item_data.get("movable", True)
            item = Item(name, (x, y), image, IMAGE_SCALE, game, movable=movable)

            item_list.append(item)
        return item_list

