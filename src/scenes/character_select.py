import pygame
from objects.player import Cat

class CharacterSelect:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        #cat skins
        self.cat_options = [
            {"name": "Gray Cat", "image_path": "../assets/media/sprites/cat_sprite.png"},
            {"name": "Orange Cat", "image_path": "../assets/media/sprites/cat_sprite.png"},
            {"name": "Black Cat", "image_path": "../assets/media/sprites/cat_sprite.png"},
        ]

        self.cat_objects = []
        for i, cat_data in enumerate(self.cat_options):
            # Each cat starts at a fixed Y position, with different X offset
            cat = Cat(x=100 + i * 120, y=200, image_path=cat_data["image_path"])
            cat.rect = pygame.Rect(100 + i * 120, 200, 80, 80)  # override for UI layout
            self.cat_objects.append({
                "cat": cat,
                "name": cat_data["name"],
                "image_path": cat_data["image_path"]
            })

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, cat in enumerate(self.cat_images):
                rect = pygame.Rect(100 + i * 120, 200, 80, 80)
                if rect.collidepoint(pos):
                    # Set selected cat
                    self.game.cat = Cat(x=100, y=250, image_path=cat["image_path"])
                    self.game.state = "menu"  # go to menu after choosing

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for cat_entry in self.cat_objects:
            cat = cat_entry["cat"]
            rect = cat.rect

            if rect.collidepoint(mouse_pos):
                cat.state = "walk"
                cat.current_frames = cat.walk_frames
            else:
                cat.state = "idle"
                cat.current_frames = cat.idle_frames

            cat.animate()


    def draw(self):
        self.screen.fill((20, 20, 30))
        font = pygame.font.SysFont(None, 40)
        title = font.render("Choose Your Cat", True, (255, 255, 255))
        self.screen.blit(title, (200, 100))

        for i, cat in enumerate(self.cat_images):
            self.screen.blit(cat["image"], (100 + i * 120, 200))
            label = pygame.font.SysFont(None, 20).render(cat["name"], True, (200, 200, 200))
            self.screen.blit(label, (100 + i * 120, 290))
