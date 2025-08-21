import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Timed Line Drawing")

# Clock
clock = pygame.time.Clock()

# Define line endpoints
lines = [
    ((50, 50), (200, 50)),
    ((200, 50), (200, 200)),
    ((200, 200), (50, 200)),
    ((50, 200), (50, 50))
]

# Variables for timing
drawn_lines = []
line_index = 0
draw_interval = 1000  # milliseconds
last_draw_time = pygame.time.get_ticks()

running = True
while running:
    screen.fill((30, 30, 30))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if it's time to draw the next line
    current_time = pygame.time.get_ticks()
    if line_index < len(lines) and current_time - last_draw_time >= draw_interval:
        drawn_lines.append(lines[line_index])
        line_index += 1
        last_draw_time = current_time

    # Draw the lines that are ready
    for line in drawn_lines:
        pygame.draw.line(screen, (0, 200, 255), line[0], line[1], 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()