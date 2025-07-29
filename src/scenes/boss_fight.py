import pygame

class BossFight:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.ending = self.get_ending()
        self.image = pygame.image.load(f"../assets/media/endings/{self.ending}.png").convert()

    def get_ending(self):
        inventory_names = [item.name for item in self.game.inventory]
        if "Bow" in inventory_names and len(inventory_names) == 1:
            # Secret love ending
            self.update_sprite_with_bow()
            return "love"
        elif self.game.stats["Health"] >= 2 or self.game.stats["Damage"] >= 3:
            return "win"
        else:
            return "lose"

    def update_sprite_with_bow(self):
        if self.game.cat.name == "Asja":
            self.game.cat.image = pygame.image.load("../assets/media/characters/Asja_bow.png").convert_alpha()
        # Add cases for other characters here if needed

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.quit_game()  # or restart

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, (0, 0))
