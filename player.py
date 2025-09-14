import pygame
from bullet import Bullet


class Player:
    def __init__(self, x, y, speed, lives, bullets):
        self.player_ship = pygame.image.load(
            "game-art/space-invaders-ship-selected.png"
        ).convert_alpha()
        self.player_ship_rect = self.player_ship.get_rect()
        self.player_ship_rect.center = (x, y)
        self.rect = self.player_ship_rect
        self.speed = speed
        self.lives = lives
        self.bullets = bullets

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def draw(self, screen, color):
        screen.blit(self.player_ship, self.player_ship_rect)

    def shoot(self):
        new_bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.append(new_bullet)
