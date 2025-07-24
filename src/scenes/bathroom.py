class Bathroom:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat

        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "bathroom.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()
        self.width = self.background.get_width()
        #self.name = "bathroom"

    def handle_event(self, event):
        # No event-specific behavior here (yet) --> later add click detection logic
        pass

    def update(self):
        self.cat.update()
        self.cat.check_boundaries()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.cat.draw(self.screen)

    def check_boundaries(self):
        # Can only exit to the right (back to living room)
        if self.cat.rect.right > self.width:
            self.game.change_scene("living_room", "left")

