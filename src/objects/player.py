import pygame

class Cat:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/sprites/my_cat.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4

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
