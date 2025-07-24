import pygame
import os

#Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'assets'))
INVENTORY_MAX = 4
IMAGE_SCALE = 1
WHITE = (255, 255, 255)

#Inventory
inventory = []

#dictonary of what is inside the rooms
rooms = {
    "Living room":[
        {"item": "Cat tree", "movable": "no", "use": "attack boost", "msg": "you scratch your claws on the tree."},
        {"item": "Couch", "movable": "no", "use": "health", "msg": "you lie down on the couch and take a nap."},
        {"item": "Food bowl", "movable": "no", "use": "none", "msg": "the bowl is empty, but you are still hungry."},
        {"item": "Cable", "movable": "yes", "use": "attack", "msg": "These look knotted, be careful to not get caught."},
        {"item": "Cartoon", "movable": "yes", "use": "key ", "msg": "You could go inside, or maybe on top?"},
        {"item": "Yarn ball", "movable": "yes", "use": "attack", "msg": "That looks fun! But lets not get distracted right now."},
        #do we add a message?
    ],
    "Bathroom":[
        {"item": "Toilet", "movable": "no", "use": "none", "msg": "That is a Toilet."},
        {"item": "Shower", "movable": "no", "use": "none", "msg": "She is still in the shower, but you can't wait to eat."},
        {"item": "Cat litter", "movable": "yes", "use": "none", "msg": "I dont't need to go right now."},
        {"item": "Toilet paper", "movable": "yes", "use": "attack", "msg": "You could roll down the entire roll.. Or maybe just take one."},
    ],
    "Garden":[
        {"item": "Squirrel", "movable": "no", "use": "Scene change", "msg": "You could try to catch that Squirrel!"},
        {"item": "Boss Cat", "movable": "no", "use": "interact", "msg": "Other cat bad."},
    ]
}




class Item:
    def __init__(self, name, pos, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.name = name
        self.scale = scale
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=pos)
        self.picked_up = False
        self.clicked = False
        self.msg = self.get_msg_for_item(name)

    def get_msg_for_item(self, name):
        for room_items in rooms.values():
            for item in room_items:
                if item ['item'] == name:
                    return item ['msg']
        return None

    def draw(self, screen):
        #only show item if not in inventory
        if not self.picked_up:
            screen.blit(self.image, self.rect)

        #mouse hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            print(self.msg) #supposed to show the message predifned in the dic when hovering

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            if len(inventory) < INVENTORY_MAX:
                self.picked_up = True
                print(f"You picked up [Item: {self.name}]")
                #inventory.append(self.name)
            else:
                print("Your inventory is full. Drop something first.")

        #make things be clickable multiple times
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

#testing
def load_test_image(item_name):
    path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'assets', 'media', 'Items', f"{item_name}.png"
    )
    path = os.path.normpath(path)
    return pygame.image.load(path).convert_alpha()

# Function to create items from dic
def create_items_for_room(room_name):
    item_list = []
    if room_name in rooms:
        base_x, base_y = 100, 100  # Place holder
        spacing = 120

        for index, item_data in enumerate(rooms[room_name]):
            name = item_data["item"]
            try:
                image = load_test_image(name)  #expects File
            except FileNotFoundError:
                print(f"[Warning] No pic found for {name}")
                continue

            x = base_x + (index % 3) * spacing
            y = base_y + (index // 3) * spacing
            item = Item(name, (x, y), image, IMAGE_SCALE)
            item_list.append(item)
    return item_list


#trying inside Item

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Item Test")

    items = create_items_for_room("Living room")

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for item in items:
            item.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

