import pygame
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Food types with weights and durations (in seconds)
FOOD_TYPES = [
    {"color": RED, "weight": 70, "points": 1, "duration": None},  # Normal food (no timer)
    {"color": YELLOW, "weight": 20, "points": 3, "duration": 8},  # Bonus food
    {"color": PURPLE, "weight": 10, "points": 5, "duration": 5}   # Special food
]

class Snake:
    def __init__(self):
        """Initialize the snake with starting position and length"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        """Return the position of the snake's head"""
        return self.positions[0]

    def update(self):
        """Update the snake's position based on current direction"""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        
        # Check for self collision
        if (new_x, new_y) in self.positions[:-1]:
            return True  # Game over
        
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False  # Game continues

    def reset(self):
        """Reset the snake to initial state"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.score = 0

    def render(self, surface):
        """Draw the snake on the game surface"""
        for position in self.positions:
            rect = pygame.Rect((position[0] * GRID_SIZE, position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

class Food:
    def __init__(self, snake_positions):
        """Initialize food with random type and position"""
        self.type = random.choices(FOOD_TYPES, weights=[f["weight"] for f in FOOD_TYPES])[0]
        self.color = self.type["color"]
        self.points = self.type["points"]
        self.spawn_time = time.time()
        self.duration = self.type["duration"]
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Generate random position for food that doesn't overlap with snake"""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break

    def is_expired(self):
        """Check if timed food has expired"""
        if self.duration is None:
            return False
        return time.time() - self.spawn_time > self.duration

    def render(self, surface):
        """Draw the food on the game surface with timer indicator if applicable"""
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        
        # Draw timer for timed food
        if self.duration is not None:
            time_left = max(0, self.duration - (time.time() - self.spawn_time))
            timer_width = (time_left / self.duration) * GRID_SIZE
            timer_rect = pygame.Rect(
                (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + GRID_SIZE - 3),
                (timer_width, 3)
            )
            pygame.draw.rect(surface, WHITE, timer_rect)

def draw_grid(surface):
    """Draw grid lines on the game surface"""
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, rect, 1)

def show_game_over(surface, score):
    """Display game over screen with final score"""
    font = pygame.font.SysFont('arial', 36)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to restart", True, WHITE)
    
    surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
    surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    surface.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 60))

def show_score(surface, score):
    """Display current score during gameplay"""
    font = pygame.font.SysFont('arial', 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

def main():
    """Main game function"""
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enhanced Snake Game")
    
    snake = Snake()
    food = Food(snake.positions)
    
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            
            elif event.type == KEYDOWN:
                if game_over:
                    if event.key == K_r:
                        # Reset game
                        snake.reset()
                        food = Food(snake.positions)
                        game_over = False
                else:
                    # Handle direction changes
                    if event.key == K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
        
        if not game_over:
            # Update snake position
            game_over = snake.update()
            
            # Check if food expired
            if food.is_expired():
                food = Food(snake.positions)
            
            # Check if snake ate food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += food.points
                food = Food(snake.positions)
            
            # Clear screen
            screen.fill(BLACK)
            draw_grid(screen)
            
            # Draw game elements
            snake.render(screen)
            food.render(screen)
            show_score(screen, snake.score)
        else:
            # Show game over screen
            show_game_over(screen, snake.score)
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()