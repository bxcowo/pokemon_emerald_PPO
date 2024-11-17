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
        self.font = pygame.font.Font(None, 74)
        self.training_mode = False  # New flag for fast training

    def reset(self) -> Dict[str, float]:
        """Reset the environment and return initial state"""
        self.ball.reset()
        return self.get_state()

    def set_training_mode(self, training: bool = True) -> None:
        """Toggle training mode for faster execution"""
        self.training_mode = training

    def step(self, player_action: int, opponent_action: int = None) -> Tuple[Dict[str, float], float, bool, Dict]:
        """
        Execute one step with actions for both paddles
        Args:
            player_action: Action for left paddle
            opponent_action: Action for right paddle (if None, use basic AI)
        """
        # Execute actions
        self.player.move(player_action)
        if opponent_action is not None:
            self.opponent.move(opponent_action)
        elif not self.training_mode:  # Basic AI for human play
            if self.opponent.rect.centery < self.ball.rect.centery:
                self.opponent.move(1)
            elif self.opponent.rect.centery > self.ball.rect.centery:
                self.opponent.move(-1)
        
        # Move ball (faster in training mode)
        if self.training_mode:
            for _ in range(2):  # Speed up ball movement
                self.ball.move()
        else:
            self.ball.move()
        
        # Initialize reward and done flag
        reward = 0  # TODO: Define your reward structure
        done = False
        
        # Handle collisions
        if self.ball.rect.colliderect(self.player.rect) or \
           self.ball.rect.colliderect(self.opponent.rect):
            self.ball.speed_x *= -1
            self.ball.increase_speed()
            # TODO: Define reward for ball hits

        # Handle scoring
        if self.ball.rect.left <= 0:
            self.opponent.score += 1
            # TODO: Define penalty for losing point
            self.ball.reset()
            done = True
        elif self.ball.rect.right >= self.screen_width:
            self.player.score += 1
            # TODO: Define reward for scoring
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