import pygame


class Enemy(pygame.rect.Rect):
    def __init__(self, x, y, width, height, point_value):
        pygame.rect.Rect.__init__(self, x, y, width, height)
        self.point_value = point_value

    def __str__(self):
        return f"X: {self.x}\nY: {self.y}\nWidth: {self.width}\nHeight: {self.height}\nPoint Value: {self.point_value}"
