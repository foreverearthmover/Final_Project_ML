import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'assets'))

WHITE = (255, 255, 255)

class Cat:
    def __init__(self, x, y):
        self.frame_width = 975
        self.frame_height = 1000
        self.scale = 0.15
        self.scale_smaller = 0.14
        self.color = WHITE
        self.speed = 4

        # Load sprite sheet
        sprite_sheet_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'media', 'sprites', 'cat_sprite.png'
        )
        sprite_sheet_path = os.path.normpath(sprite_sheet_path)
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()

        self.rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
        self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
        self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]
        self.animation_timer = 0
        self.animation_delay = 200
        self.state = "idle"
        self.facing_left = False
    ...
    def load_frames(self, start_index, count, scale):
        frames = []
        for i in range(start_index, start_index + count):
            x = i * self.frame_width
            frame = self.get_image(x,0, self.frame_width, self.frame_height, scale)
            frames.append(frame)
        return frames

    #printing the image on a different sheet
    def get_image(self, x, y, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha() #this should be an empty image
        image.blit(self.sprite_sheet, (0,0), pygame.Rect(x,y,width,height))
        image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
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