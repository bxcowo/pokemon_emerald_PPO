import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

# Game objects
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2,
                               WINDOW_HEIGHT // 2 - BALL_SIZE // 2,
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = BALL_SPEED * random.choice((1, -1))

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

def main():
    # Create game objects
    player = Paddle(50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    opponent = Paddle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    # Game font
    font = pygame.font.Font(None, 74)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(up=True)
        if keys[pygame.K_s]:
            player.move(up=False)

        # Simple AI for opponent
        if opponent.rect.centery < ball.rect.centery:
            opponent.move(up=False)
        if opponent.rect.centery > ball.rect.centery:
            opponent.move(up=True)

        # Ball movement
        ball.move()

        # Ball collision with paddles
        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect):
            ball.speed_x *= -1

        # Score points
        if ball.rect.left <= 0:
            opponent.score += 1
            ball.reset()
        if ball.rect.right >= WINDOW_WIDTH:
            player.score += 1
            ball.reset()

        # Drawing
        screen.fill(BLACK)
        player.draw()
        opponent.draw()
        ball.draw()

        # Draw scores
        player_text = font.render(str(player.score), True, WHITE)
        opponent_text = font.render(str(opponent.score), True, WHITE)
        screen.blit(player_text, (WINDOW_WIDTH // 4, 20))
        screen.blit(opponent_text, (3 * WINDOW_WIDTH // 4, 20))

        # Draw center line
        pygame.draw.aaline(screen, WHITE, 
                          (WINDOW_WIDTH // 2, 0),
                          (WINDOW_WIDTH // 2, WINDOW_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
