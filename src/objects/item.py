import pygame
import os



#Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'assets'))
#Inventory
INVENTORY_MAX = 4
IMAGE_SCALE = 1
WHITE = (255, 255, 255)
DARK_GREY = (45, 45, 45)
INVENTORY_COLOR = (DARK_GREY)
INVENTORY_BORDER_COLOR = (WHITE)
INVENTORY_POSITION = 100
ITEM_SPACING = 80

#dictonary of what is inside the rooms
rooms = {
    "Living room":[
        {"item": "Cat tree", "movable": "no", "stat": "Damage", "effect": 3, "msg": "You could sharpen your claws on this.", "use_msg": "My claws feel sharper.", "x": 395, "y": 130},
        {"item": "Couch", "movable": "no", "stat": "Health", "effect": 3, "msg": "You could lie down on the couch and take a nap.", "use_msg": "I rested for a while.","x": 60, "y": 145},
        {"item": "Food bowl", "movable": "no", "stat": "none", "effect": 0, "msg": "The bowl is empty, but you are still hungry.", "use_msg": "I ate the only cat kibble left. Still hungry.","x": 526, "y": 405},
        {"item": "Carton", "movable": "no", "stat": "none", "effect": 0,"msg": "You could go inside, or maybe on top?", "use_msg": "Cartons are a cat's best friend.","x": 232, "y": 398},
        {"item": "Cable", "movable": "yes", "stat": "Damage", "effect": 1,"msg": "These look knotted, be careful to not get caught.", "use_msg": "Ahh! Phew I almost got stuck..","x": 311, "y": 434},
        {"item": "Yarn ball", "movable": "yes", "stat": "Damage","effect": 1, "msg": "That looks fun! But lets not get distracted right now.", "use_msg": "I wish my human would play with me.","x": 500, "y": 238 },
        #do we add a message?
    ],
    "Bathroom":[
        {"item": "Toilet", "movable": "no", "stat": "none","effect": 0, "msg": "That is a Toilet." , "use_msg": "This thing is way too loud sometimes.", "x": 467, "y": 137},
        {"item": "Shower", "movable": "no", "stat": "none", "effect": 0,"msg": "She is still in the shower, but you can't wait to eat." , "use_msg": "Can't hear me.", "x": 0, "y": 0},
        {"item": "Cat litter", "movable": "yes", "stat": "none", "effect": 0,"msg": "I don't need to go right now." , "use_msg": "I'm not sure why I'm carrying this with me.", "x": 10, "y": 425},
        {"item": "Cabinet", "movable": "no", "stat": "none", "effect": 0,"msg": "That's a lot of Toilet paper" , "use_msg": "You go through the Toilet paper", "x": 322, "y": -7}
    ],
    "Garden":[
        {"item": "Squirrel", "movable": "no", "stat": "Scene change", "effect": 0, "msg": "You could try to catch that Squirrel!" , "use_msg": "It got away!", "x": 100, "y": 100},
        {"item": "Boss Cat", "movable": "no", "stat": "Boss fight", "effect": 0,"msg": "Other cat bad." , "use_msg": "'* Hiss *'", "x": 100, "y": 100},
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
        self.use_msg = self.get_use_for_item(name)
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

        # Multi-Click System for closet
        self.click_count = 0
        self.max_clicks = 4
        self.hidden_item_spawned = False


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
                    return item ["use_msg"]

    def try_pick_up(self):
        if self.movable == "yes":
            if self not in self.game.inventory:
                if len(self.game.inventory) < INVENTORY_MAX:
                    self.picked_up = True
                    self.game.inventory.append(self)
                    self.game.item_states[self.name] = True  # Update global state
                    # Apply stat effect when picked up
                    if self.stat != "none":
                        self.game.stats[self.stat] = self.game.stats.get(self.stat, 0) + self.effect
                    print(f"You picked up the [Item: {self.name}]")
                else:
                    print("Inventory full. Drop something first.")
            else:
                print(f"The {self.name} is already in your inventory.")
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
            print(self.msg) #supposed to show the message predefined in the dic when hovering

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
        if self.rect.collidepoint(pos) and not self.picked_up:
            if self.name == "Cabinet" and self.movable == "no":
                self.handle_cabinet_clicks()
                return True
            elif self.movable == "yes":
                self.try_pick_up()
                return True
            else:
                self.use()
                return True
        return False

    def get_movable_status(self, name):
        for room_items in rooms.values():
            for item in room_items:
                if item['item'] == name:
                    return item['movable']
        return "no"

    def handle_cabinet_clicks(self):
        self.click_count += 1
        if self.click_count <= 3:
            self.add_toilet_paper_to_inventory()
            self.game.status_message = "Picked up Toilet paper."
            self.game.message_timer = pygame.time.get_ticks()
        elif self.click_count == 4:
            self.spawn_bow_item()
            self.game.status_message = "I found this behind the stacks of toilet paper.. How pretty!"
            self.game.message_timer = pygame.time.get_ticks()
        else:
            self.game.status_message = "The cabinet is empty."
            self.game.message_timer = pygame.time.get_ticks()

    def add_toilet_paper_to_inventory(self):
        if len(self.game.inventory) < 4:  # INVENTORY_MAX
            try:
                tp_image = load_test_image("Toilet paper")
                tp_item = Item("Toilet paper", (0, 0), tp_image, 1, self.game)
                # Set properties manually to ensure it's droppable
                tp_item.picked_up = True
                tp_item.movable = "yes"
                tp_item.stat = "none"  # Toilet paper has no stat effect
                tp_item.effect = 0
                tp_item.msg = "You could push over the tower.. Or maybe just take one."
                tp_item.use_msg = "Let me just take this."
                self.game.inventory.append(tp_item)
                print("YOU PICKED UP TOILET PAPER")
            except Exception as e:
                print("Can't find Toilet paper picture", e)

    def spawn_bow_item(self):
        try:
            bow_image = load_test_image("Bow")
            bow_item = Item("Bow", (400, 300), bow_image, 1, self.game)
            # Set properties manually to ensure it's collectible
            bow_item.movable = "yes"
            bow_item.stat = "Love"
            bow_item.effect = 1
            bow_item.msg = "What a pretty Bow"
            bow_item.use_msg = "I look fab."
            #add to scene
            if hasattr(self.game.current_scene, 'items'):
                self.game.current_scene.items.append(bow_item)
                self.game.item_states["Bow"] = False
            print("THERES A BOW!")
        except Exception as e:
            print("Can't find Bow picture", e)


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

