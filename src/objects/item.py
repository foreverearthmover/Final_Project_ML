import pygame
#To do:
#items clickable
#list of constants
INVENTORY_MAX = 4

#list of variables
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

#load item images
cat_tree_img = pygame.image.load('location').convert_alpha()


class Item:
    def __init__(self, name, pos, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.name = name
        self.scale = 1
        self.image = pygame.transform.scale (image, (int(width  * scale), int(height * scale)))
        self.rect = self.image.get_rect(topleft=pos)
        self.picked_up = False

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect)


    def check_click(self, pos):
        return self.rect.collidepoint(pos)

#maybe needs to be moved
cat_tree = Item("Cat tree", (100, 100), cat_tree_img, scale )

cat_tree.draw()