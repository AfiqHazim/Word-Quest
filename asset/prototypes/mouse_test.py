import pygame
pygame.init()

# Window setup
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame Button Example")
font = pygame.font.SysFont(None, 32)

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Button properties
button_rect = pygame.Rect(150, 120, 100, 50)
button_color = GRAY
button_text = font.render("Click Me", True, BLACK)

running = True
while running:
    screen.fill(WHITE)

    # Get mouse position and click status
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Hover effect
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, DARK_GRAY, button_rect)
        if mouse_click[0]:  # Left click
            print("Button clicked!")
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    # Draw text
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()