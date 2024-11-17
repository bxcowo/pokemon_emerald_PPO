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
        return (self.rect.centery / self.screen_height, self.score)

class Ball:
    def __init__(self, x: int, y: int, size: int, speed: int, screen_width: int, screen_height: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def move(self) -> None:
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.speed_y *= -1

    def reset(self) -> None:
        self.rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.speed_x = self.speed * random.choice((1, -1))
        self.speed_y = self.speed * random.choice((1, -1))

    def get_state(self) -> Tuple[float, float, float, float]:
        """Return normalized ball position and velocity"""
        return (
            self.rect.centerx / self.screen_width,
            self.rect.centery / self.screen_height,
            self.speed_x / self.speed,
            self.speed_y / self.speed
        ) 