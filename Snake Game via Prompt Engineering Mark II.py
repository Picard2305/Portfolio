import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 2.5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont("arial", 24)
game_over_font = pygame.font.SysFont("arial", 40)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Utility functions
def draw_snake(snake_blocks):
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, (*block, BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_position):
    pygame.draw.rect(screen, RED, (*food_position, BLOCK_SIZE, BLOCK_SIZE))

def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, [10, 10])

def show_game_over(score):
    screen.fill(BLACK)
    msg1 = game_over_font.render("Game Over", True, RED)
    msg2 = font.render(f"Score: {score}", True, WHITE)
    msg3 = font.render("Press R to Restart or Q to Quit", True, BLUE)
    screen.blit(msg1, [WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 3])
    screen.blit(msg2, [WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2])
    screen.blit(msg3, [WIDTH // 2 - msg3.get_width() // 2, HEIGHT // 1.5])
    pygame.display.update()

def random_food():
    return [
        random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    ]

def main():
    snake = [[100, 50], [80, 50], [60, 50]]
    direction = 'RIGHT'
    food = random_food()
    score = 0
    game_over = False

    while True:
        change_to = direction  # Start with current direction

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r and game_over:
                    main()

        # Block reverse direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        elif change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move the snake
        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= BLOCK_SIZE
        elif direction == 'DOWN':
            head_y += BLOCK_SIZE
        elif direction == 'LEFT':
            head_x -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head_x += BLOCK_SIZE

        new_head = [head_x, head_y]
        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()

        # Check for collisions
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake[1:]
        ):
            game_over = True

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)

        if game_over:
            show_game_over(score)

        pygame.display.update()
        clock.tick(FPS + score // 5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
