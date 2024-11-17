from typing import Tuple, Dict, Any
import pygame
from game_objects import Paddle, Ball

class PongEnvironment:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.screen_width = config['window_width']
        self.screen_height = config['window_height']
        
        # Initialize game objects
        self.player = Paddle(
            50, 
            self.screen_height // 2 - config['paddle_height'] // 2,
            config['paddle_width'],
            config['paddle_height'],
            config['paddle_speed'],
            self.screen_height
        )
        
        self.opponent = Paddle(
            self.screen_width - 50 - config['paddle_width'],
            self.screen_height // 2 - config['paddle_height'] // 2,
            config['paddle_width'],
            config['paddle_height'],
            config['paddle_speed'],
            self.screen_height
        )
        
        self.ball = Ball(
            self.screen_width // 2,
            self.screen_height // 2,
            config['ball_size'],
            config['ball_speed'],
            self.screen_width,
            self.screen_height
        )

        self.reset()

    def reset(self) -> Dict[str, float]:
        """Reset the environment and return initial state"""
        self.ball.reset()
        return self.get_state()

    def step(self, action: int) -> Tuple[Dict[str, float], float, bool, Dict]:
        """
        Execute one step in the environment
        Returns: (state, reward, done, info)
        """
        # Execute action
        self.player.move(action)
        
        # Move ball
        self.ball.move()
        
        # Check collisions
        reward = 0
        done = False
        
        if self.ball.rect.colliderect(self.player.rect) or \
           self.ball.rect.colliderect(self.opponent.rect):
            self.ball.speed_x *= -1
            reward += 1  # Reward for hitting the ball

        # Check scoring
        if self.ball.rect.left <= 0:
            self.opponent.score += 1
            reward -= 5  # Penalty for losing point
            self.ball.reset()
            done = True
        elif self.ball.rect.right >= self.screen_width:
            self.player.score += 1
            reward += 5  # Reward for scoring
            self.ball.reset()
            done = True

        return self.get_state(), reward, done, {}

    def get_state(self) -> Dict[str, float]:
        """Return current state of the environment"""
        ball_state = self.ball.get_state()
        player_state = self.player.get_state()
        opponent_state = self.opponent.get_state()
        
        return {
            'ball_x': ball_state[0],
            'ball_y': ball_state[1],
            'ball_vx': ball_state[2],
            'ball_vy': ball_state[3],
            'player_y': player_state[0],
            'opponent_y': opponent_state[0],
            'player_score': player_state[1],
            'opponent_score': opponent_state[1]
        }

    def render(self, screen: pygame.Surface) -> None:
        """Render the current game state"""
        screen.fill(self.config['colors']['black'])
        
        # Draw paddles and ball
        pygame.draw.rect(screen, self.config['colors']['white'], self.player.rect)
        pygame.draw.rect(screen, self.config['colors']['white'], self.opponent.rect)
        pygame.draw.rect(screen, self.config['colors']['white'], self.ball.rect)
        
        # Draw center line
        pygame.draw.aaline(screen, self.config['colors']['white'],
                          (self.screen_width // 2, 0),
                          (self.screen_width // 2, self.screen_height)) 