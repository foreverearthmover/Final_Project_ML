import os
import pygame


def load_skin() :
    # loads the skin for the boss cat -> always "Jimmy"
    path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "sprites", "Jimmy.png")
    return os.path.normpath(path)

class BossCat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Sprite and animation settings
        self.frame_width = 975
        self.frame_height = 1000
        self.scale = 0.14
        self.sprite_sheet = pygame.image.load(load_skin()).convert_alpha()
        self.image_path = load_skin()

        self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(2400, 120))  # appears at far right in garden

        self.animation_timer = 0
        self.animation_delay = 300  # milliseconds between frames

        self.visible = False  # invisible by default

    def load_frames(self, start_index, count, scale):
        frames = []
        for i in range(start_index, start_index + count):
            x = i * self.frame_width
            frame = self.get_image(x, 0, self.frame_width, self.frame_height, scale)
            frames.append(frame)
        return frames

    def get_image(self, x, y, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey((255, 255, 255))  # remove white bg if present
        return image

    def start_chase(self):
        self.visible = True # controls whether boss cat is drawn and moves

    def update(self):
        if not self.visible:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
