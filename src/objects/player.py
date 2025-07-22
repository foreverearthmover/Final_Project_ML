import pygame
import os

WHITE = (255, 255, 255)


#putting a BG to work, later DELETE
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Cat')

#Load BG DELETE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "backgrounds", "garden.png")
image_path = os.path.normpath(image_path)
background = pygame.image.load(image_path)


#Load sprite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sprite_sheet_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "sprites", "cat_sprite.png")
sprite_sheet_path = os.path.normpath(sprite_sheet_path)
sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()




class Cat:
    def __init__(self, sheet, frame_width, frame_height, x, y, scale, color, num_frames):
        self.sprite_sheet = sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.color = color
        self.frames = []
        self.rect = pygame.Rect(x, y, frame_width, frame_height)
        self.speed = 4

        #Animation
        self.idle_frames = self.load_frames(start_index=0, count=4)
        self.walk_frames = self.load_frames(start_index=4, count=3)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]
        self.animation_timer = 0
        self.animation_delay = 200 #milsecs between frames
        self.state = "idle"
        self.facing_left = False

    def load_frames(self, start_index, count):
        frames = []
        for i in range(start_index, start_index + count):
            x = i * self.frame_width
            frame = self.get_image(x,0, self.frame_width, self.frame_height)
            frames.append(frame)
        return frames

    #printing the image on a different sheet
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha() #this should be an empty image
        image.blit(self.sprite_sheet, (0,0), pygame.Rect(x,y,width,height))
        image = pygame.transform.scale(image,(int(width * self.scale), int(height * self.scale)))
        image.set_colorkey(self.color)
        return image

    def update(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_left = True
            moved = True

        elif keys[pygame.K_RIGHT]: #or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_left = False
            moved = True

        if moved:
            #if self.state != "walk":
                self.state = "walk"
                self.current_frames = self.walk_frames
                #self.frame_index = 0 #to reset it
        else:
            #if self.state != "idle":
                self.state = "idle"
                self.current_frames = self.idle_frames
                #self.frame_index = 0
        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index +1) % len(self.current_frames)
            frame = self.current_frames[self.frame_index]

            #flipping the image if walking left
            if self.facing_left:
                frame = pygame.transform.flip(frame, True, False).convert_alpha()
            self.image = frame


    def draw(self, screen):
        screen.blit(self.image, self.rect)

#later DELETE

# Example
cat = Cat(
    sheet=sprite_sheet,
    frame_width=975,
    frame_height=1000,
    x=100,
    y=200,
    scale=0.2,
    color=WHITE,
    num_frames=4
)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.blit (background, (0, 0))  # Draw background
    cat.update()
    cat.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
