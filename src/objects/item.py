import pygame
#To do:
#items clickable
#list of constants
INVENTORY_MAX = 4

#list of variables
inventory = []

#dictonary of what is inside the rooms
rooms = {
    "living room":[
        {"item": "Cat tree", "movability": "no", "use": "attack boost", "msg": "you scratch your claws on the tree."},
        {"item": "Couch", "movability": "no", "use": "health", "msg": "you lie down on the couch and take a nap."},
        {"item": "Food bowl", "movability": "no", "use": "none", "msg": "the bowl is empty, but you are still hungry."},
        {"item": "Carton", "movability": "yes", "use": "attack", "msg": "These look knotted, be careful to not get caught."},
        { }#do we add a message?
    ]
}


class Item:
    def __init__(self, name, image_path, pos):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=pos)
        self.picked_up = False

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)
