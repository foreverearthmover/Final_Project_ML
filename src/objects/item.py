import pygame

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
