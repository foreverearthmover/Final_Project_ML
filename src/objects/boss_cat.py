import os
import random
import pygame


def load_random_skin(exclude=None):
    all_skins = ["Asja", "Tommy", "Tofu", "Kira"]
    if exclude and exclude in all_skins:
        all_skins.remove(exclude)
    selected = random.choice(all_skins)

    path = os.path.join("..", "assets", "media", "sprites", f"{selected}.png")
    return pygame.image.load(path).convert_alpha()


class BossCat(pygame.sprite.Sprite):
    def __init__(self, player_skin):
        super().__init__()
        self.image = load_random_skin(player_skin)
        self.rect = self.image.get_rect(topleft=(100, 100))  # Set position as needed



    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass  # static for now
