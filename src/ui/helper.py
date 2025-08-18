import pygame
from assets.media.text.fonts import get_small_font
from src.objects.item import (
    INVENTORY_COLOR, 
    INVENTORY_BORDER_COLOR, 
    INVENTORY_POSITION, 
    ITEM_SPACING, 
    WHITE
)

DROPBUTTON_POS_Y = 10

def draw_inventory(screen, game, selected_inventory_item):
    """Draw the inventory panel and all items within it."""
    font = get_small_font(9)

    # Background and border
    pygame.draw.rect(screen, INVENTORY_COLOR, (INVENTORY_POSITION, 5, 350, 80))
    pygame.draw.rect(screen, INVENTORY_BORDER_COLOR, (INVENTORY_POSITION, 5, 350, 80), 2)

    # Draw items
    for i, item in enumerate(game.inventory):
        item_x = INVENTORY_POSITION + 20 + i * ITEM_SPACING

        # Item image
        inventory_img = pygame.transform.scale(item.image, (45, 45))
        screen.blit(inventory_img, (item_x, 20))

        # Item name
        text = font.render(item.name, True, WHITE)
        screen.blit(text, (item_x, 65))

        # Drop button
        if selected_inventory_item == item and item.movable == "yes":
            drop_font = get_small_font(11)
            drop_text = drop_font.render("Drop", True, (255, 0, 0))
            drop_rect = pygame.Rect(item_x, DROPBUTTON_POS_Y, 50, 20)
            pygame.draw.rect(screen, (50, 0, 0), drop_rect)
            screen.blit(drop_text, (item_x + 5, DROPBUTTON_POS_Y + 3))

def draw_hover_message(screen, game):
    """Draw hover message at the bottom of the screen."""
    if hasattr(game, "hover_message") and game.hover_message:
        font = get_small_font(12)
        msg_surface = font.render(game.hover_message, True, (255, 255, 255))

        bg_rect = msg_surface.get_rect(
            topleft=(screen.get_width() / 4, screen.get_height() - 30)
        )
        pygame.draw.rect(screen, (0, 0, 0), bg_rect.inflate(10, 10))
        screen.blit(msg_surface, bg_rect)