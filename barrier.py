import pygame


class Barrier:
    def __init__(self, x, y):
        self.orig_barrier_img = pygame.image.load(
            "game-art/barrier.png"
        ).convert_alpha()
        self.barrier_list = []
        self.barrier_imgs_list = []
        self.x = x
        self.y = y
        self.orig_w, self.orig_h = self.orig_barrier_img.get_size()

        for i in range(10, 4, -1):
            float_val = i / 10.0
            new_w = int(self.orig_w * float_val)
            new_h = int(self.orig_h * float_val)

            new_rect = pygame.Rect(0, 0, new_w, new_h)
            new_rect.center = (x, y)
            self.barrier_list.append(new_rect)

            scaled_image = pygame.transform.scale(self.orig_barrier_img, (new_w, new_h))
            self.barrier_imgs_list.append(scaled_image)
