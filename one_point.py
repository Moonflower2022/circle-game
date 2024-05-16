import pygame
import sys
import math

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Function to calculate the largest radius of a circle avoiding a point
def largest_radius(x, y):
    if math.sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2) >= 0.5:
        return 0.5
    if x < 0.5:
        x = 1 - x
    if y < 0.5:
        y = 1 - y
    return x + y - math.sqrt(2 * x * y)

def circle_center(r, x, y):
    print(x, y)
    center_x = r if x >= 0.5 else 1 - r
    center_y = r if y >= 0.5 else 1 - r
    return (center_x, center_y)

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
SCALE_FACTOR = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Largest Circle in Square")

# Set up the clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clear the screen
            screen.fill(WHITE)
            # Draw the square
            pygame.draw.rect(screen, BLACK, (0, 0, SCALE_FACTOR, SCALE_FACTOR), 2)
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate the largest radius avoiding the clicked point
            radius = largest_radius(mouse_x / SCREEN_WIDTH, mouse_y / SCREEN_HEIGHT)
            # Calculate the center of the circle
            x, y = circle_center(radius, mouse_x / SCALE_FACTOR, mouse_y / SCALE_FACTOR)
            # Draw the circle
            pygame.draw.circle(screen, BLACK, (x * SCALE_FACTOR, y * SCALE_FACTOR), int(radius * SCALE_FACTOR), 2)

            pygame.draw.circle(screen, RED, (mouse_x, mouse_y), 5, 5)
            # Display the area of the circle
            font = pygame.font.Font(None, 36)
            text = font.render(f"Circle Area: {math.pi * radius ** 2:.2f}", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 50))
            screen.blit(text, text_rect)
            # Update the display
            pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
