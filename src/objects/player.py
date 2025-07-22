import pygame
import os
from pygame.examples.sprite_texture import sprite

#this needs to be somewhere later not sure if it can stay here

WHITE = (255, 255, 255)
#putting a BG to work, later DELETE

# Setting game window dimensions
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "backgrounds", "garden.png")
image_path = os.path.normpath(image_path)

background = pygame.image.load(image_path)


# it is having troubles t find the picture, so I used this method, but i dont know where to put it in the code yet:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sprite_sheet_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "sprites", "cat_sprite.png")
sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()




class Cat:
    def __init__(self,sheet,frame, x, y, width, height, scale, color):
        self.sprite_sheet = sheet
        self.image = self.get_image(sprite_sheet,(frame * width) ,x,y,width, height, scale, color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4

    #printing the image on a different sheet
    def get_image(self,sheet, frame, x, y, width, height,scale,color ):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha() #this should be an empty image
        image.blit(self.sprite_sheet, (0,0), pygame.Rect(x,y,width,height))
        image = pygame.transform.scale(image,(width * scale, height * scale))
        image.set_colorkey(color)

        return image




    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def update(self):
        pass  # add animation, collision, etc.

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#later DELETE
clock = pygame.time.Clock()
cat = Cat(
    sprite_sheet,  # sheet
    0,             # frame
    100, 100,      # x, y
    900, 900,      # width, height from the sprite sheet (adjust as needed!)
    0.2,           # scale
    WHITE          # color to make transparent
)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        cat.handle_event(event)

    screen.blit (background, (0, 0))  # Draw background
    cat.update()
    cat.draw(screen)
    pygame.display.update()
    clock.tick(60)
