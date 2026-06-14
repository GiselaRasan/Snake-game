"""
Snake Game - Nokia Style
--------------------------------------------
Requirements: pygame must be installed
    py -3.12 -m pip install pygame

How to play:
    - Use arrow keys to move the snake
    - Eat the red squares (food) to grow and score points
    - If you hit yourself or the wall, you lose
    - Press ESC to quit
"""

import pygame
import random

# ------------------------------
# Initial setup
# ------------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

SPEED = 10  # frames per second (higher = faster)


def draw_grid(screen):
    """Draws grid lines so the board looks like a tile grid (optional)."""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))


def generate_food(snake):
    """Generates a random food position that doesn't overlap the snake."""
    while True:
        x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
        y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)


def show_message(screen, text, font, color, y_offset=0):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - Nokia Style")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    small_font = pygame.font.SysFont("Arial", 20)

    running = True
    while running:
        # ------------------------------
        # Initial game state
        # ------------------------------
        x, y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        direction = (CELL_SIZE, 0)  # starts moving right
        snake = [(x, y)]
        food = generate_food(snake)
        score = 0
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)
                    elif event.key == pygame.K_ESCAPE:
                        return

            # Move the snake
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                    new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
                game_over = True

            # Check self collision
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                # Check if it ate the food
                if new_head == food:
                    score += 1
                    food = generate_food(snake)
                else:
                    snake.pop()  # remove tail if it didn't eat

            # ------------------------------
            # Draw everything
            # ------------------------------
            screen.fill(BLACK)
            draw_grid(screen)

            # Draw food
            pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

            # Draw snake
            for segment in snake:
                pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

            # Show score
            score_text = small_font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(SPEED)

        # ------------------------------
        # Game Over screen
        # ------------------------------
        waiting = True
        while waiting:
            screen.fill(BLACK)
            show_message(screen, "Game Over!", font, WHITE, -30)
            show_message(screen, f"Final score: {score}", small_font, WHITE, 10)
            show_message(screen, "Press R to retry or ESC to quit", small_font, WHITE, 50)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        return
if __name__ == "__main__":
    main()