import pygame
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "..", "assets"))

WHITE = (255, 255, 255)

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, game=None):
        super().__init__()
        self.x = x
        self.y = y
        self.image_path = image_path  # Save it for later use in set_image_with_bow()
        self.original_image_path = image_path
        self.game = game
        self.name = self.get_name_from_path(image_path)
        self.bow_equipped = False
        self.frame_width = 975
        self.frame_height = 1000
        self.scale = 0.15
        self.scale_smaller = 0.14
        self.color = WHITE
        self.speed = 4

        # Load sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.normpath(image_path)).convert_alpha()

        self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
        self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]

        # Cat hitbox
        self.rect = self.image.get_rect(topleft=(x, y))

        # position and state player starts out with
        self.animation_timer = 0
        self.animation_delay = 200
        self.state = "idle"
        self.facing_left = False

        self.stats = {
            "Damage": 0,
            "Health": 0,
            "Love": 0
        }

        self.auto_walk_right = False
        self.auto_walk_speed = 8

    def start_auto_walk_right(self):
        # automatic walking
        self.auto_walk_right = True
        self.state = "walk"
        self.current_frames = self.walk_frames
        self.facing_left = False

    def stop_auto_walk(self):
        self.auto_walk_right = False

    def get_name_from_path(self, path):
        # Tommy_bow.png -> Tommy
        filename = os.path.basename(path)
        return filename.replace(".png", "").replace("_bow", "")

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

    def update_sprite_if_bow_equipped(self):
        if not self.game or not hasattr(self.game, "inventory"):
            return

        has_bow = any(item.name == "Bow" for item in self.game.inventory)

        if has_bow and not self.bow_equipped:
            bow_path = self.original_image_path.replace(".png", "_bow.png")
            if os.path.exists(bow_path):
                self.sprite_sheet = pygame.image.load(bow_path).convert_alpha()
                self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
                self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
                self.current_frames = self.idle_frames
                self.frame_index = 0
                self.bow_equipped = True

        elif not has_bow and self.bow_equipped:
            original_path = self.original_image_path
            if os.path.exists(original_path):
                self.sprite_sheet = pygame.image.load(original_path).convert_alpha()
                self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
                self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
                self.current_frames = self.idle_frames
                self.frame_index = 0
                self.bow_equipped = False

    #HIER IST DAS PROBLEM :,)
    def update(self):
        self.update_sprite_if_bow_equipped()

        if self.auto_walk_right:
            self.rect.x += self.auto_walk_speed
            self.facing_left = False
            self.state = "walk"
            self.current_frames = self.walk_frames

            self.animate()
            return

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_left = True
            moved = True

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_left = False
            moved = True

        if moved:
                self.state = "walk"
                self.current_frames = self.walk_frames
                #self.frame_index = 0 #to reset it
        else:
                self.state = "idle"
                self.current_frames = self.idle_frames
        self.animate()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index +1) % len(self.current_frames)
            frame = self.current_frames[self.frame_index]

            # flipping the image if walking left
            if self.facing_left:
                frame = pygame.transform.flip(frame, True, False).convert_alpha()
            self.image = frame


    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) # for debugging
        screen.blit(self.image, self.rect)