import pygame
import sys
import os
import subprocess

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Choose a Game Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)
LIGHT_RED = (255, 182, 193)
DARK_RED = (178, 34, 34)

# Fonts
font_title = pygame.font.Font(None, 48)
font_button = pygame.font.Font(None, 36)

# Draw text function
def draw_text(text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

# Button function
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Button background color change on hover
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Button text
    draw_text(text, font_button, BLACK, x + width / 2, y + height / 2)

# File runner function
def run_file(filename):
    if os.path.exists(filename):
        subprocess.run(["python", filename], check=True)
    else:
        print(f"The file '{filename}' does not exist.")

# Main function
def main():
    while True:
        # Background color gradient
        for y in range(SCREEN_HEIGHT):
            gradient_color = (173 - y // 5, 216 - y // 7, 230)
            pygame.draw.line(screen, gradient_color, (0, y), (SCREEN_WIDTH, y))

        # Title
        draw_text("Choose a Game Mode", font_title, BLACK, SCREEN_WIDTH // 2, 50)

        # Buttons
        draw_button("FRIEND", 200, 150, 200, 50, LIGHT_BLUE, DARK_BLUE, lambda: run_file("game1.py"))
        draw_button("AI", 200, 220, 200, 50, LIGHT_GREEN, DARK_GREEN, lambda: run_file("game2.py"))
        draw_button("EXIT", 200, 290, 200, 50, LIGHT_RED, DARK_RED, pygame.quit)

        # Update display
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
