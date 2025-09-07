import pygame
import sys
from game import Game

FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 500)) # display resolution
    pygame.display.set_caption("Catventure") # caption for window
    clock = pygame.time.Clock()

    # main game loop
    game = Game(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
