import pygame
import os

class BossFight:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.name = None

        self.ending = self.get_ending()
        original_image = pygame.image.load(f"../assets/media/endings/{self.ending}.png").convert()
        self.image = pygame.transform.scale(original_image, self.screen.get_size())

    def get_ending(self):
        inventory_names = [item.name for item in self.game.inventory]
        if any(item.name == "Bow" for item in self.game.inventory):
            # Secret love ending
            self.update_sprite_with_bow()
            return "love_ending_3"
        elif self.game.stats["Health"] >= 2 or self.game.stats["Damage"] >= 3:
            return "win_ending"
        else:
            return "lose_ending"

    def update_sprite_with_bow(self):
        self.name = self.game.cat.name
        if self.name in ["Asja", "Tofu", "Tommy", "Kira", "Jimmy"]:
            bow_path = f"../assets/media/sprites/{self.name}_bow.png"
            if os.path.exists(bow_path):
                self.game.cat.image = pygame.image.load(bow_path).convert_alpha()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.quit_game()  # or restart

    def update(self):
        pass

    def draw_inventory(self):
        pass #this is not supposed to show anything, but without there is an error

    def draw(self):
        self.screen.blit(self.image, (0, 0))
