import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, point_value, alien_level):
        super().__init__()

        self.x = x
        self.y = y

        self.images = []

        if alien_level == 1:
            current_alien = pygame.image.load(
                "game-art/level-one-alien.png"
            ).convert_alpha()
        if alien_level == 2:
            current_alien = pygame.image.load(
                "game-art/level-two-alien.png"
            ).convert_alpha()
        if alien_level == 3:
            current_alien = pygame.image.load(
                "game-art/level-three-alien.png"
            ).convert_alpha()

        frame1 = current_alien.subsurface((0, 0, 64, 64))
        frame2 = current_alien.subsurface((64, 0, 64, 64))

        self.images.append(frame1)
        self.images.append(frame2)

        self.current_frame = 0
        self.image = self.images[self.current_frame]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.point_value = point_value
        self.is_alive = True

        self.last_update_time = pygame.time.get_ticks()
        self.animation_interval = 500

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_interval:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        return pygame.Rect(self.rect.midbottom[0], self.rect.midbottom[1], 5, 5)
