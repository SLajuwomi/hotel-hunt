import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        bullet_img1 = pygame.image.load("game-art/player_bullet.png").convert_alpha()
        bullet_img2 = pygame.image.load("game-art/player_bullet2.png").convert_alpha()
        self.images = [bullet_img1, bullet_img2]

        self.current_frame = 0
        self.image = self.images[self.current_frame]

        self.animation_interval = 150
        self.last_update_time = pygame.time.get_ticks()

        self.rect = self.image.get_rect(center=(x, y))

    def update(self, speed):
        self.rect.y -= speed
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update_time > self.animation_interval:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.images)

            self.image = self.images[self.current_frame]
