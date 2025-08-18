import pygame
import os


#Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "assets"))
#Inventory
INVENTORY_MAX = 4
IMAGE_SCALE = 1
WHITE = (255, 255, 255)
DARK_GREY = (45, 45, 45)
INVENTORY_COLOR = DARK_GREY
INVENTORY_BORDER_COLOR = WHITE
INVENTORY_POSITION = 5
ITEM_SPACING = 80

#dictonary of what is inside the rooms
rooms = {
    "Living room":[
        {"item": "Cat tree", "movable": "no", "stat": "Damage", "effect": 3, "msg": "I could sharpen my claws on this.", "use_msg": "My claws feel sharper.", "x": 395, "y": 130},
        {"item": "Couch", "movable": "no", "stat": "Health", "effect": 3, "msg": "I could lie down on the couch to take a nap.", "use_msg": "I took a good nap.","x": 60, "y": 145},
        {"item": "Food bowl", "movable": "no", "stat": "none", "effect": 0, "msg": "The bowl is empty.. someone stole my food!!", "use_msg": "I ate the only cat kibble left. Where does this trail go?","x": 526, "y": 405},
        {"item": "Carton", "movable": "no", "stat": "none", "effect": 0,"msg": "This Box looks ver cozy", "use_msg": "Cartons are a cat's best friend.","x": 232, "y": 398},
        {"item": "Cable", "movable": "yes", "stat": "Damage", "effect": 1,"msg": "These look knotted, I will be careful to not get caught", "use_msg": "Ahh! Phew I almost got stuck..","x": 311, "y": 434},
        {"item": "Yarn ball", "movable": "yes", "stat": "Damage","effect": 1, "msg": "That looks fun! But I dont want to get distracted right now.", "use_msg": "I wish my human would play with me.","x": 500, "y": 238 },
    ],
    "Bathroom":[
        {"item": "Toilet", "movable": "no", "stat": "none","effect": 0, "msg": "That is a Toilet" , "use_msg": "This thing is way too loud sometimes.", "x": 467, "y": 137},
        {"item": "Shower", "movable": "no", "stat": "none", "effect": 0,"msg": "They're still in the shower, but Im so hungry!" , "use_msg": "Can't hear me.", "x": 0, "y": 0},
        {"item": "Cat litter", "movable": "yes", "stat": "none", "effect": 0,"msg": "I don't need to go right now." , "use_msg": "I'm not sure why I'm carrying this with me.", "x": 10, "y": 425},
        {"item": "Cabinet", "movable": "no", "stat": "none", "effect": 0,"msg": "There seem to be a lot of things stashed here." , "use_msg": "I went through the Toilet paper", "x": 322, "y": -7}
    ],
    "Garden":[
        {"item": "Squirrel", "movable": "no", "stat": "Scene change", "effect": 0, "msg": "I bet I can catch the Squirrel!" , "use_msg": "It got away!", "x": 100, "y": 100},
        {"item": "Boss Cat", "movable": "no", "stat": "Boss fight", "effect": 0,"msg": "Other cat bad." , "use_msg": "'* Hiss *'", "x": 100, "y": 100},
    ]
}

class Item:
    """Item class for managing item interactions and state."""
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

        # Multi-Click System for cabinet
        self.click_count = 0
        self.max_clicks = 4
        self.hidden_item_spawned = False


    def apply_effect(self, game):
        """Apply item stat effect to player stats."""
        if self.stat and self.stat != "none" and not self.used:
            game.stats[self.stat] = game.stats.get(self.stat, 0) + self.effect
            self.used = True  # prevent re-use

    def get_msg_for_item(self, name: object) -> str | int | None:
        """Get the message to display when hovering over the item."""
        for room_items in rooms.values():
            for item in room_items:
                if item ["item"] == name:
                    return item ["msg"]
        return None

    def get_use_for_item(self, name: object) -> str | int | None:
        """Get the message to display when using the item."""
        for room_items in rooms.values():
            for item in room_items:
                if item["item"] == name:
                    return item ["use_msg"]

    def try_pick_up(self):
        """Pick up item if it is movable and not already in inventory."""
        if self.movable == "yes":
            if self not in self.game.inventory:
                if len(self.game.inventory) < INVENTORY_MAX:
                    self.picked_up = True
                    self.game.inventory.append(self)
                    self.game.item_states[self.name] = True  # Update global state
                    # Apply stat effect when picked up
                    if self.stat != "none":
                        self.game.stats[self.stat] = self.game.stats.get(self.stat, 0) + self.effect

    def draw(self, screen):
        """Draw item to screen."""
        # Only draw the item if it is not picked up
        if not self.picked_up:
            screen.blit(self.image, self.rect)

        # Handle mouse hovering (optional based on your logic)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.picked_up:
            self.game.hover_message = self.msg

        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_pressed:
            self.mouse_was_pressed = False

        if not mouse_pressed:
            self.clicked = False

        # make things be clickable multiple times
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(mouse_pos) and not self.picked_up:
            self.game.hover_message = self.msg

    def check_click(self, pos):
        """Check if item is clicked and handle accordingly."""
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
        """Get movable status of item from dictionary."""
        for room_items in rooms.values():
            for item in room_items:
                if item["item"] == name:
                    return item["movable"]
        return "no"

    def handle_cabinet_clicks(self):
        """Handle clicks for the cabinet (special case)."""
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
        """Add toilet paper to the inventory properly (special case)."""
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
            except Exception as e:
                print("Can't find Toilet paper picture", e)

    def spawn_bow_item(self):
        """Spawn bow item in scene (special case)."""
        try:
            bow_image = load_test_image("Bow")
            bow_item = Item("Bow", (400, 300), bow_image, 0.9, self.game)
            # Set properties manually to ensure it's collectible
            bow_item.movable = "yes"
            bow_item.stat = "Love"
            bow_item.effect = 1
            bow_item.msg = "What a pretty Bow"
            bow_item.use_msg = "I look fab."
            # add to scene
            if hasattr(self.game.current_scene, "items"):
                self.game.current_scene.items.append(bow_item)
                self.game.item_states["Bow"] = False
        except Exception as e:
            print("Can't find Bow picture", e)


    def use(self):
        if self.stat and not self.movable:  # Only use non-movable items
            print(f"[USE] {self.name} used. +{self.effect} {self.stat}")
            self.game.update_stat(self.stat, self.effect)

#testing
def load_test_image(item_name):
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "assets", "media", "Items", f"{item_name}.png"
    )
    path = os.path.normpath(path)
    return pygame.image.load(path).convert_alpha()


# Function to create items from dictionary
def create_items_for_room(room_name, game, movable):
    item_list = []
    if room_name in rooms:
        for item_data in rooms[room_name]:
            name = item_data["item"]
            if item_data["item"] in ["Squirrel", "Boss Cat"]:
                continue
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

