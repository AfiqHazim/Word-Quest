import pygame
import requests

pygame.init()

# Create screen
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Clue Box Demo")

# Font
font = pygame.font.Font("freesansbold.ttf", 30)

# Get clue (your function)
def get_clue(word):
    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests.get(url)
        word_json = response.json()
        word_definition = word_json[0]["meanings"][0]["definitions"][0]["definition"]
        return word_definition
    except Exception:
        return "None"

clue = get_clue("smoke")  # Example word

# Limit box dimensions
clue_box_rect = pygame.Rect(500, 100, 500, 500)  # (x, y, width, height)
clue_surface = pygame.Surface((clue_box_rect.width, clue_box_rect.height))
clue_surface.fill((44, 230, 99))  # Background color

# Function to render multiline text with word wrap
def render_multiline_text(text, font, color, surface):
    words = text.split(" ")
    space_width = font.size(" ")[0]
    x, y = 0, 0
    max_width = surface.get_width()

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()

        if x + word_width >= max_width:
            x = 0
            y += word_height
            if y + word_height > surface.get_height():
                break  # Clip overflow vertically

        surface.blit(word_surface, (x, y))
        x += word_width + space_width

# Render the clue into the clue_surface
render_multiline_text(clue, font, (192, 192, 192), clue_surface)

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw clue surface on screen
    screen.blit(clue_surface, (clue_box_rect.x, clue_box_rect.y))

    # Optional: Draw a border
    pygame.draw.rect(screen, (255, 255, 255), clue_box_rect, 2)

    pygame.display.flip()

pygame.quit()