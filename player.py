import pygame


class Player:
    def __init__(self, x, y, speed, lives):
        self.x = x
        self.y = y
        self.speed = speed
        self.lives = lives

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
