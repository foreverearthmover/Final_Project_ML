import pygame
from objects.player import Cat
import os

class CharacterSelect:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, "..", "..", "assets", "media", "text", "8-bit_wonder.ttf")
        font_path = os.path.normpath(font_path)

        self.title_font = pygame.font.Font(font_path, 36)
        self.label_font = pygame.font.Font(font_path, 10)

        #cat skins
        self.cat_options = [
            {"name": "Tofu", "image_path": "../assets/media/sprites/Tofu.png"},
            {"name": "Asja", "image_path": "../assets/media/sprites/Asja.png"},
            {"name": "Kira", "image_path": "../assets/media/sprites/Kira.png"},
            {"name": "Tommy", "image_path": "../assets/media/sprites/Tommy.png"},
            {"name": "Jimmy", "image_path": "../assets/media/sprites/Jimmy.png"},
        ]

        self.cat_objects = []
        for i, cat_data in enumerate(self.cat_options):
            # Each cat starts at a fixed Y position, with different X offset
            cat = Cat(x=100 + i * 120, y=200, image_path=cat_data["image_path"], game=self.game)
            cat.rect = pygame.Rect(70 + i * 120, 200, 120, 120)  # override for UI layout
            self.cat_objects.append({
                "cat": cat,
                "name": cat_data["name"],
                "image_path": cat_data["image_path"]
            })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for entry in self.cat_objects:
                if entry["cat"].rect.collidepoint(pos):
                    self.game.cat = Cat(x=100, y=250, image_path=entry["image_path"], game=self.game)
                    self.game.state = "menu"

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for cat_entry in self.cat_objects:
            cat = cat_entry["cat"]
            rect = cat.rect

            if rect.collidepoint(mouse_pos):
                if cat.state != "walk":
                    cat.state = "walk"
                    cat.current_frames = cat.walk_frames
            else:
                if cat.state != "idle":
                    cat.state = "idle"
                    cat.current_frames = cat.idle_frames

            cat.animate()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Choose a Cat", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 100))

        for entry in self.cat_objects:
            cat = entry["cat"]
            name = entry["name"]

            cat.draw(self.screen)  # Draw animated cat first

            label = self.label_font.render(name, True, (200, 200, 200))
            # draw label BELOW the cat
            self.screen.blit(label, (cat.rect.x + 25, cat.rect.y + cat.image.get_height() + 5))
