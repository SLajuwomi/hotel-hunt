import pygame


# barrier spacing - 40
# barrier width - 60
# barrier height - 40
class Barrier:
    def __init__(self, x, y, width, height):
        self.barrier_list = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        for i in range(0, 40, 5):
            self.barrier_list.append(pygame.rect.Rect(x, y, width - i, height - i))

    def __str__(self):
        return f"{self.barrier_list}"
