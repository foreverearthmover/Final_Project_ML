import pygame
import os




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', '..', 'assets'))

WHITE = (255, 255, 255)

class Cat:
    def __init__(self, x, y, image_path):
        self.frame_width = 975
        self.frame_height = 1000
        self.scale = 0.15
        self.scale_smaller = 0.14
        self.color = WHITE
        self.speed = 4
        #self.image = pygame.image.load(image_path).convert_alpha()
        # Load sprite sheet
        tofu_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'media', 'sprites', 'Tofu.png'
        )

        asja_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'media', 'sprites', 'Asja.png'
        )

        tommy_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'media', 'sprites', 'Tommy.png'
        )

        kira_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'assets', 'media', 'sprites', 'Kira.png'
        )

        self.image_path = image_path  # Save it for later use in set_image_with_bow()
        self.sprite_sheet = pygame.image.load(os.path.normpath(image_path)).convert_alpha()

        self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
        self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]

        # Replaced this:
        # self.rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
        # With this:
        self.rect = self.image.get_rect(topleft=(x, y))
        # so that cat has right hitbox

        self.animation_timer = 0
        self.animation_delay = 200
        self.state = "idle"
        self.facing_left = False

        self.stats = {
            "Damage": 1,
            "Health": 1
        }
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

    def set_image_with_bow(self):
        if "Asja" in self.image_path:
            new_path = self.image_path.replace("Asja", "Asja_bow")
        elif "Tofu" in self.image_path:
            new_path = self.image_path.replace("Tofu", "Tofu_bow")
        elif "Tommy" in self.image_path:
            new_path = self.image_path.replace("Tommy", "Tommy_bow")
        elif "Kira" in self.image_path:
            new_path = self.image_path.replace("Kira", "Kira_bow")
        else:
            return  # No match, exit

        # Reload the sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.normpath(new_path)).convert_alpha()

        #Recreate animation frames
        self.idle_frames = self.load_frames(start_index=0, count=4, scale=self.scale_smaller)
        self.walk_frames = self.load_frames(start_index=4, count=3, scale=self.scale)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]

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
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2) # for debugging
        screen.blit(self.image, self.rect)