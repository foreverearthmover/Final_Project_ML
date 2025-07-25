import os
import pygame

class Garden:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.cat = game.cat
        self.button_font = game.button_font  # Use same font as in game

        # Load the garden background
        bg_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "media", "backgrounds", "garden.png")
        self.background = pygame.image.load(os.path.normpath(bg_path)).convert()
        self.scroll_offset = 0

        # Squirrel attributes
        self.squirrel_rect = pygame.Rect(self.screen.get_width() - 200, self.screen.get_height() // 2, 40, 40)
        self.squirrel_visible = True
        self.squirrel_running = False

        # Chase button attributes
        self.chase_button_rect = pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() - 50, 150, 40)
        self.show_chase_button = False

        # Boss cat scene attributes
        self.boss_cat_rect = pygame.Rect(0, self.cat.rect.y, 40, 40)
        self.boss_cat_visible = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle squirrel click
            if self.squirrel_visible and self.squirrel_rect.collidepoint(mouse_pos):
                self.squirrel_running = True

            # Handle chase button click
            if self.show_chase_button and self.chase_button_rect.collidepoint(mouse_pos):
                self.navigate_to_boss_area()

    def update(self):
        # Handle the squirrel running off-screen
        if self.squirrel_running:
            self.squirrel_rect.x += 5  # Squirrel runs to the right
            if self.squirrel_rect.left > self.screen.get_width():  # If squirrel goes off-screen
                self.squirrel_running = False
                self.squirrel_visible = False
                self.show_chase_button = True  # Show the chase button

        # Update the player cat animation
        self.cat.update()

    def navigate_to_boss_area(self):
        # Hide chase button and transition to the boss scene
        self.show_chase_button = False
        self.scroll_offset = self.background.get_width() // 2  # Move to the second half of the background
        self.cat.rect.x = 50  # Place cat near the left side of the screen
        self.boss_cat_visible = True
        self.boss_cat_rect.x = self.screen.get_width() - 100  # Boss cat appears on the right side

    def draw(self):
        # Draw the background with the offset
        self.screen.blit(self.background, (-self.scroll_offset, 0))

        # Draw the cat
        self.cat.draw(self.screen)

        # Draw the squirrel if visible
        if self.squirrel_visible:
            pygame.draw.rect(self.screen, (165, 42, 42), self.squirrel_rect)  # Red rectangle as squirrel

        # Draw the boss cat if visible
        if self.boss_cat_visible:
            pygame.draw.rect(self.screen, (0, 0, 255), self.boss_cat_rect)  # Blue rectangle as boss cat

        # Draw chase button
        if self.show_chase_button:
            pygame.draw.rect(self.screen, (200, 200, 200), self.chase_button_rect, border_radius=10)
            chase_text = self.button_font.render("Chase", True, (0, 0, 0))
            text_rect = chase_text.get_rect(center=self.chase_button_rect.center)
            self.screen.blit(chase_text, text_rect)