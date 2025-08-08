import pygame
import os
from assets.media.text.fonts import get_big_font, get_small_font

class BossFight:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.name = None
        self.state = 'intro'  # intro, love1, love2, love3, win_black, win, lose_black, lose, done
        self.timer = 0
        self.last_advance = pygame.time.get_ticks()
        self.ending_type = self.get_ending_type()
        self.images = {
            'intro': self.load_and_scale_image('ending.PNG'),
            'love1': self.load_and_scale_image('love_ending_1.PNG'),
            'love2': self.load_and_scale_image('love_ending_2.PNG'),
            'love3': self.load_and_scale_image('love_ending_3.PNG'),
            'win': self.load_and_scale_image('win_ending.PNG'),
            'lose': self.load_and_scale_image('lose_ending.PNG'),
        }
        self.texts = {
            'intro': 'The cat approaches! Did you prepare well enough...?',
            'love1': 'The cat notices your bow...',
            'love2': '',
            'love3': '',
            'win': 'You have defeated the boss cat! Congratulations!',
            'lose': 'You were defeated by the boss cat...'
        }
        self.black_surface = pygame.Surface(self.screen.get_size())
        self.black_surface.fill((0, 0, 0))
        self.black_surface.set_alpha(255)
        self.advance_ready = True

    def load_and_scale_image(self, filename):
        path = os.path.join('..', 'assets', 'media', 'endings', filename)
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, self.screen.get_size())

    def get_ending_type(self):
        if any(item.name == "Bow" for item in self.game.inventory):
            return 'love'
        elif self.game.stats["Health"] >= 2 or self.game.stats["Damage"] >= 3:
            return 'win'
        else:
            return 'lose'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            self.advance_sequence()

    def advance_sequence(self):
        now = pygame.time.get_ticks()

        if self.state == 'intro':
            if self.ending_type == 'love':
                self.state = 'love1'
            elif self.ending_type == 'win':
                self.state = 'win_black'
                self.last_advance = now
            else:
                self.state = 'lose_black'
                self.last_advance = now
        elif self.state == 'love1':
            self.state = 'love2'
        elif self.state == 'love2':
            self.state = 'love3'
        elif self.state == 'love3':
            self.state = 'done'
        elif self.state == 'win_black':
            self.state = 'win'
        elif self.state == 'win':
            self.state = 'done'
        elif self.state == 'lose_black':
            self.state = 'lose'
        elif self.state == 'lose':
            self.state = 'done'

    def update(self):
        # For black screen delay
        now = pygame.time.get_ticks()
        if self.state in ['win_black', 'lose_black']:
            if now - self.last_advance > 1000:
                if self.state == 'win_black':
                    self.state = 'win'
                else:
                    self.state = 'lose'

    def draw_inventory(self):
        pass

    def draw_text_box(self, text):
        # Text Box
        width = self.screen.get_width()
        height = 100
        y = self.screen.get_height() - height
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, y))
        pygame.draw.rect(self.screen, (255, 255, 255), (0, y, width, height), 3)
        if text:
            font = get_small_font(18)
            rendered = font.render(text, True, (255, 255, 255))
            text_rect = rendered.get_rect(center=(width // 2, y + height // 2))
            self.screen.blit(rendered, text_rect)

    def draw(self):
        # Draw the current step
        if self.state == 'intro':
            self.screen.blit(self.images['intro'], (0, 0))
            self.draw_text_box(self.texts['intro'])
        elif self.state == 'love1':
            self.screen.blit(self.images['love1'], (0, 0))
            self.draw_text_box(self.texts['love1'])
        elif self.state == 'love2':
            self.screen.blit(self.images['love2'], (0, 0))
        elif self.state == 'love3':
            self.screen.blit(self.images['love3'], (0, 0))
        elif self.state == 'win_black':
            self.screen.blit(self.black_surface, (0, 0))
        elif self.state == 'win':
            self.screen.blit(self.images['win'], (0, 0))
            self.draw_text_box(self.texts['win'])
        elif self.state == 'lose_black':
            self.screen.blit(self.black_surface, (0, 0))
        elif self.state == 'lose':
            self.screen.blit(self.images['lose'], (0, 0))
            self.draw_text_box(self.texts['lose'])
        elif self.state == 'done':

            self.game.quit_game()
