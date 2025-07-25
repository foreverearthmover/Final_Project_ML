import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 500))
    pygame.display.set_caption("Catventure")
    clock = pygame.time.Clock()

    game = Game(screen)
    game.state = "character_select"  # set this to start directly there
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
