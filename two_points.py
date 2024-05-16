import pygame
import sys
import math

# https://www.desmos.com/calculator/cxa0ov2lmv

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# solve x = 1 - y and x^2 = (x - A)^2 + (1 - x - B)^2 for x and y
# x = -sqrt(2) sqrt(-A (B - 1)) + A - B + 1 and y = sqrt(2) sqrt(-A (B - 1)) - A + B
def up_left(blocker1):
    A, B = blocker1

    x = -math.sqrt(-2 * A * (B - 1)) + A - B + 1
    y = math.sqrt(-2 * A * (B - 1)) - A + B

    return (x, y), x

# solve x = y and (1 - x)^2 = (x - A)^2 + (y - B)^2 for x and y
# x = sqrt(2) sqrt((A - 1) (B - 1)) + A + B - 1 ∧ y = sqrt(2) sqrt((A - 1) (B - 1)) + A + B - 1
def up_right(blocker1):
    A, B = blocker1

    x = y = math.sqrt(2 * (A - 1) * (B - 1)) + A + B - 1

    return (x, y), 1 - x

# solve x = 1 - y and y^2 = (1 - y - A)^2 + (y - B)^2 for x and y
# x = -sqrt(2) sqrt(-(A - 1) B) + A - B and y = sqrt(2) sqrt(-(A - 1) B) - A + B + 1
def down_right(blocker1):
    A, B = blocker1

    x = math.sqrt(-2 * (A - 1) * B) + A - B
    y = -math.sqrt(-2 * (A - 1) * B) - A + B + 1

    return (x, y), y

# from one point
def down_left(blocker1):
    A, B = blocker1

    x = y = -math.sqrt(2 * A * B) + A + B 
    
    return (x, y), x

# solve solve (1 - x)^2 = (x - A)^2 + (y - B)^2 and (1 - x)^2 = (x - C)^2 + (y - D)^2 for y and x for y and x
# y = (sqrt((A - 1) (C - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + A D + B (-C) + B - D)/(A - C) and x = (A^3 - 2 B sqrt((A - 1) (C - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + 2 D sqrt((A - 1) (C - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - A^2 C + A B^2 - 2 A B D - A C^2 + A D^2 + B^2 C - 2 B^2 - 2 B C D + 4 B D + C^3 + C D^2 - 2 D^2)/(2 (A - C)^2) and A - C!=0 and A - 1!=0
def right_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if (A - C) == 0 or (A - 1) == 0 or (C - 1) == 0:
        print("Error: A - C, A - 1, and C - 1 must not be zero")
        return None, None

    inner_expression = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = (A**3 - 2 * B * inner_expression + 2 * D * inner_expression - A**2 * C + A * B**2 - 2 * A * B * D - A * C**2 + A * D**2 + B**2 * C - 2 * B**2 - 2 * B * C * D + 4 * B * D + C**3 + C * D**2 - 2 * D**2)
    denominator = 2 * (A - C)**2
    x =  numerator / denominator

    inner_expression = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = math.sqrt((A - 1) * (C - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) + A * D + B * (-C) + B - D
    denominator = A - C
    y =  numerator / denominator

    return (x, y), 1 - x 

# solve A + (y - B)^2/A = C + (y - D)/C and x^2 = (x - A)^2 + (y - B)^2 for y and x
# y = -(sqrt(A C (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - A D + B C)/(A - C) and x = (A^3 + 2 B (sqrt(A C (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - C D) - 2 D sqrt(A C (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - A^2 C + A (B^2 - 2 B D - C^2 + D^2) + B^2 C + C^3 + C D^2)/(2 (A - C)^2) and A!=C and A!=0 and C!=0
def left_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if A == C or A == 0 or C == 0:
        print("Error: A must not be equal to C, A must not be zero, and C must not be zero")
        return None, None

    numerator = -math.sqrt(A * C * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) - A * D + B * C
    denominator = A - C
    y = numerator / denominator

    inner_expression = math.sqrt(A * C * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = (A**3 + 2 * B * (inner_expression - C * D) - 2 * D * inner_expression - A**2 * C + A * (B**2 - 2 * B * D - C**2 + D**2) + B**2 * C + C**3 + C * D**2)
    denominator = 2 * (A - C)**2
    x = numerator / denominator

    return (x, y), x

# solve y^2 = (x - A)^2 + (y - B)^2 and y^2 = (x - C)^2 + (y - D)^2 for x and y
# x = -(sqrt(B D (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + A D - B C)/(B - D) and y = (2 A (sqrt(B D (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - B C - C D) - 2 C sqrt(B D (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + A^2 (B + D) + B^3 - B^2 D + B (C^2 - D^2) + C^2 D + D^3)/(2 (B - D)^2) and B!=D and B!=0
def down_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if B == D or B == 0:
        print("Error: B must not be equal to D and B must not be zero")
        return None, None

    numerator = math.sqrt(B * D * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) - A * D + B * C
    denominator = B - D
    x = numerator / denominator

    inner_expression = math.sqrt(B * D * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2))
    numerator = (-2 * A * (inner_expression + B * C + C * D) + 2 * C * inner_expression + A**2 * (B + D) + B**3 - B**2 * D + B * (C**2 - D**2) + C**2 * D + D**3)
    denominator = 2 * (B - D)**2
    y = numerator / denominator

    return (x, y), y

# solve (1 - y)^2 = (x - A)^2 + (y - B)^2 and (1 - y)^2 = (x - C)^2 + (y - D)^2 for x and y
# x = (-sqrt((B - 1) (D - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + A (-D) + A + (B - 1) C)/(B - D) and y = (2 A (sqrt((B - 1) (D - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) - C (B + D - 2)) - 2 C sqrt((B - 1) (D - 1) (A^2 - 2 A C + B^2 - 2 B D + C^2 + D^2)) + A^2 (B + D - 2) + B^3 - B^2 D + B (C^2 - D^2) + C^2 D - 2 C^2 + D^3)/(2 (B - D)^2) and B!=D and B!=1
def up_case(blocker1, blocker2):
    A, B = blocker1
    C, D = blocker2

    if B == D or B == 1:
        raise ValueError("B must not be equal to D or 1")
    
    numerator_x = (-math.sqrt((B - 1) * (D - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) + A * (-D) + A + (B - 1) * C)
    denominator_x = B - D
    x = numerator_x / denominator_x
    
    numerator_y = (2 * A * (math.sqrt((B - 1) * (D - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) - C * (B + D - 2)) - 2 * C * math.sqrt((B - 1) * (D - 1) * (A**2 - 2 * A * C + B**2 - 2 * B * D + C**2 + D**2)) + A**2 * (B + D - 2) + B**3 - B**2 * D + B * (C**2 - D**2) + C**2 * D - 2 * C**2 + D**3)
    denominator_y = 2 * (B - D)**2
    y = numerator_y / denominator_y

    return (x, y), 1 - y

def within_bounds(center, radius):
    return center[0] - radius >= 0 and center[0] + radius <= 1 and center[1] - radius >= 0 and center[1] + radius <= 1

def check_solution(blocker, center, radius):
    return ((blocker[0] - center[0]) ** 2 + (blocker[1] - center[1]) ** 2) > radius ** 2

def two_blockers(blocker1, blocker2):
    two_blocker_cases = [up_case, down_case, right_case, left_case]
    one_blocker_cases = [up_left, up_right, down_left, down_right]
    
    two_blocker_solutions = [func(blocker1, blocker2) if within_bounds(*func(blocker1, blocker2)) else ((0, 0), 0) for func in two_blocker_cases] + [func(blocker2, blocker1) if within_bounds(*func(blocker2, blocker1)) else ((0, 0), 0) for func in two_blocker_cases]
    one_blocker_solutinos = [func(blocker1) if check_solution(blocker2, *func(blocker1)) else ((0, 0), 0) for func in one_blocker_cases] + [func(blocker2) if check_solution(blocker1, *func(blocker2)) else ((0, 0), 0) for func in one_blocker_cases]
    maximum = max(two_blocker_solutions + one_blocker_solutinos, key=lambda x: x[1])
    if maximum[1] == 0:
        raise Exception()
    print(two_blocker_solutions)
    print(maximum)
    return ((0.5, 0.5), 0.5) if maximum[1] > 0.5 else maximum

def draw_scene(screen, center, radius, blocker1, blocker2):
    # Clear the screen
    screen.fill(WHITE)
    # Draw the square
    pygame.draw.rect(screen, BLACK, (0, 0, SCALE_FACTOR, SCALE_FACTOR), 2)
    # Draw the circle
    pygame.draw.circle(screen, BLACK, center, int(radius), 2)
    # Draw the points
    pygame.draw.circle(screen, RED, blocker1, 5, 5)
    pygame.draw.circle(screen, BLUE, blocker2, 5, 5)

    # Display the area of the circle
    font = pygame.font.Font(None, 36)
    text = font.render(f"Circle Area: {math.pi * (radius / SCALE_FACTOR) ** 2:.3f}", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT - 50))
    screen.blit(text, text_rect)

def scale_coordinates(coords, scale):
    return coords[0] * scale, coords[1] * scale

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
SCALE_FACTOR = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Largest Circle in Square")

clock = pygame.time.Clock()
running = True

selected = 1

blocker1 = scale_coordinates((0.4, 0.6), SCALE_FACTOR)
blocker2 = scale_coordinates((0.7, 0.1), SCALE_FACTOR)
center, radius = two_blockers(scale_coordinates(blocker1, 1/SCALE_FACTOR), scale_coordinates(blocker2, 1/SCALE_FACTOR))

draw_scene(screen, scale_coordinates(center, SCALE_FACTOR), radius * SCALE_FACTOR, blocker1, blocker2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if selected == 1:
                blocker1 = pygame.mouse.get_pos()
            elif selected == 2:
                blocker2 = pygame.mouse.get_pos()
            else:
                raise Exception()
            
            center, radius = two_blockers(scale_coordinates(blocker1, 1/SCALE_FACTOR), scale_coordinates(blocker2, 1/SCALE_FACTOR))
            draw_scene(screen, scale_coordinates(center, SCALE_FACTOR), radius * SCALE_FACTOR, blocker1, blocker2)

            pygame.display.flip()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected = 1
            if event.key == pygame.K_2:
                selected = 2

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()

