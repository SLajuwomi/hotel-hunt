import pygame


class Enemy(pygame.rect.Rect):
    def __init__(self, x, y, width, height, point_value, is_alive):
        pygame.rect.Rect.__init__(self, x, y, width, height)
        self.point_value = point_value
        self.is_alive = is_alive

    def shoot(self):
        return pygame.Rect(self.midbottom.x, self.midbottom.y, 5, 5)
