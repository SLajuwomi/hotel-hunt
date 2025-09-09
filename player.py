import pygame


class Player:
    def __init__(self, x, y, speed, lives, bullets):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = speed
        self.lives = lives
        self.bullets = bullets

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def draw(self):
        top_of_tri = (self.rect.centerx, self.rect.top)
        bot_left_tri = (self.rect.left, self.rect.bottom)
        bot_right_tri = (self.rect.right, self.rect.bottom)
        pygame.draw.polygon(top_of_tri, bot_left_tri, bot_right_tri)

    def shoot(self):
        self.bullets.append(pygame.Rect(self.rect.x, self.rect.y, 5, 5))
