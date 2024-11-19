import pygame
import random
from typing import Tuple

class Paddle:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, screen_height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0
        self.speed = speed
        self.screen_height = screen_height

    def move(self, action: int) -> None:
        """
        Move paddle based on action
        action: -1 (up), 0 (stay), 1 (down)
        """
        if action == -1 and self.rect.top > 0:
            self.rect.y -= self.speed
        elif action == 1 and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def get_state(self) -> Tuple[float, float]:
        """Return normalized paddle position"""
        return self.rect.centery / self.screen_height, self.score

class Ball:
    def __init__(self, x: int, y: int, size: int, speed: int, screen_width: int, screen_height: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.initial_speed = speed * 0.6  # Slower initial speed
        self.base_speed = speed
        self.speed_multiplier = 1.0  # New: for progressive difficulty
        self.max_speed_multiplier = 2.0  # New: cap the maximum speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_delay = 30
        self.reset()

    def increase_speed(self):
        """Increase speed after paddle hits"""
        self.speed_multiplier = min(self.speed_multiplier * 1.1, self.max_speed_multiplier)
        current_speed = (self.speed_x**2 + self.speed_y**2)**0.5
        speed_ratio = current_speed / (self.base_speed * self.speed_multiplier)
        
        # Adjust current velocity to match new speed while maintaining direction
        self.speed_x *= (self.base_speed * self.speed_multiplier * speed_ratio) / current_speed
        self.speed_y *= (self.base_speed * self.speed_multiplier * speed_ratio) / current_speed

    def reset(self) -> None:
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_multiplier = 1.0  # Reset speed multiplier
        self.speed_x = self.initial_speed * random.choice((1, -1))
        self.speed_y = self.initial_speed * random.choice((1, -1))
        self.start_delay = 30

    def move(self) -> None:
        if self.start_delay > 0:
            self.start_delay -= 1
            return

        self.rect.x += self.speed_x * self.speed_multiplier
        self.rect.y += self.speed_y * self.speed_multiplier

        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.speed_y *= -1

    def get_state(self) -> Tuple[float, float, float, float]:
        """Return normalized ball position and velocity"""
        return (
            # Center x and y normalized to screen size
            self.rect.centerx / self.screen_width,
            self.rect.centery / self.screen_height,
            # Normalized speed
            self.speed_x / self.base_speed,
            self.speed_y / self.base_speed
        ) 