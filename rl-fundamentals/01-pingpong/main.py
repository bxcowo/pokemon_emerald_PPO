import pygame
import sys
from game_environment import PongEnvironment

# Configuration
CONFIG = {
    'window_width': 800,
    'window_height': 600,
    'paddle_width': 15,
    'paddle_height': 90,
    'ball_size': 15,
    'paddle_speed': 5,
    'ball_speed': 7,
    'colors': {
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((CONFIG['window_width'], CONFIG['window_height']))
    pygame.display.set_caption("Ping Pong RL")
    clock = pygame.time.Clock()
    
    # Initialize environment
    env = PongEnvironment(CONFIG)
    
    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get human player action (-1: up, 0: stay, 1: down)
        keys = pygame.key.get_pressed()
        action = 0
        if keys[pygame.K_w]:
            action = -1
        elif keys[pygame.K_s]:
            action = 1

        # Step environment
        state, reward, done, info = env.step(action)
        
        # Simple opponent AI (will be replaced with RL agent)
        if env.opponent.rect.centery < env.ball.rect.centery:
            env.opponent.move(1)
        elif env.opponent.rect.centery > env.ball.rect.centery:
            env.opponent.move(-1)

        # Render
        env.render(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
