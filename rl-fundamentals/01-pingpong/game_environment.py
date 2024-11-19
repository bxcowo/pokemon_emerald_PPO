from typing import Tuple, Dict, List, Any
import pygame
from game_objects import Paddle, Ball

class FixedOpponent:
    """Oponente fijo que sigue la posición de la pelota."""

    def __init__(self, paddle: Paddle, ball: Ball):
        self.paddle = paddle
        self.ball = ball

    def get_action(self) -> int:
        """Decide la acción basada en la posición de la pelota."""
        if self.ball.rect.centery < self.paddle.rect.centery:
            return -1  # Mover hacia arriba
        elif self.ball.rect.centery > self.paddle.rect.centery:
            return 1  # Mover hacia abajo
        else:
            return 0  # Mantenerse


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
        self.font = pygame.font.Font(None, 74)
        self.training_mode = False  # New flag for fast training

    def reset(self) -> Dict[str, float]:
        """Reset the environment and return initial state"""
        self.ball.reset()
        self.player.score = 0
        self.opponent.score = 0
        return self.get_state()

    def set_training_mode(self, training: bool = True) -> None:
        """Toggle training mode for faster execution"""
        self.training_mode = training
        if training:
            self.ball.speed_multiplier = 2.0
        else:
            self.ball.speed_multiplier = 1.0

    def step(self, player_action: int, opponent_action: int) -> Tuple[Dict[str, float], float, bool, Dict]:
        """
        Execute one step with actions for both paddles
        Args:
            player_action: Action for left paddle
            opponent_action: Action for right paddle
        """
        # Part for Human VS Computer
        # Execute actions
        # Initialize reward
        reward = 0
        self.player.move(player_action)
        if player_action == 0:
            reward -= 0.1

        self.opponent.move(opponent_action)

        # Part for Q-Learning
        self.ball.move()

        # Handle collisions
        if self.ball.rect.colliderect(self.player.rect):
            self.ball.speed_x *= -1
            self.ball.increase_speed()
            reward += 1

        if self.ball.rect.colliderect(self.opponent.rect):
            self.ball.speed_x *= -1
            self.ball.increase_speed()

        # Handle scoring
        if self.ball.rect.left <= 0:
            self.opponent.score += 1
            reward -= 5
            self.ball.reset()
        elif self.ball.rect.right >= self.screen_width:
            self.player.score += 1
            reward += 5
            self.ball.reset()

        # Initialize done flag
        done = self.player.score >= 5 or self.opponent.score >= 5

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
            'opponent_y': opponent_state[0]
        }

    def render(self, screen: pygame.Surface = None) -> None:
        """
        Render the current game state
        Args:
            screen: Pygame surface (optional in training mode)
        """
        if self.training_mode or screen is None:
            return
            
        screen.fill(self.config['colors']['black'])
        
        # Draw paddles and ball
        pygame.draw.rect(screen, self.config['colors']['white'], self.player.rect)
        pygame.draw.rect(screen, self.config['colors']['white'], self.opponent.rect)
        pygame.draw.rect(screen, self.config['colors']['white'], self.ball.rect)
        
        # Draw center line
        pygame.draw.aaline(screen, self.config['colors']['white'],
                          (self.screen_width // 2, 0),
                          (self.screen_width // 2, self.screen_height))
        
        # Draw scores
        player_text = self.font.render(str(self.player.score), True, self.config['colors']['white'])
        opponent_text = self.font.render(str(self.opponent.score), True, self.config['colors']['white'])
        screen.blit(player_text, (self.screen_width // 4, 20))
        screen.blit(opponent_text, (3 * self.screen_width // 4, 20))

        pygame.display.flip()