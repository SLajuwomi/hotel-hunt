import pygame
import random
from player import Player
from enemy import Enemy


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.is_running = True

        self.player = Player()

        self.enemies = []
        self.enemy_bullets = []
        self.enemies_that_can_shoot = []

        self.enemy_width = 40
        self.enemy_height = 30
        self.enemy_spacing = 10
        self.enemy_rows = 5
        self.enemy_start_y = 50
        self.enemy_side_margin = 50
        self.last_enemy_shot_time = 0
        self.enemy_shot_interval = 125

        self.score = 0
        self.level = 1
        self.current_time = pygame.time.get_ticks()

        self.create_enemy_grid()

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

        self.update()

    def update(self):
        if self.current_time - self.last_enemy_shot_time > self.enemy_shot_interval:
            if self.enemies_that_can_shoot:
                shooter = random.choice(self.enemies_that_can_shoot)
                self.enemy_bullets.append(shooter.shoot())
                self.last_enemy_shot_time = self.current_time
        Player.move()

    def create_enemy_grid(self):
        self.enemies.clear()
        point_val = 0

        left_margin = self.enemy_side_margin
        right_margin = self.enemy_side_margin

        usable_width = self.screen.width - left_margin - right_margin
        max_enemies = (usable_width + self.enemy_spacing) // (
            self.enemy_width + self.enemy_spacing
        )

        for row in range(self.enemy_rows):
            row_enemies = []
            for col in range(max_enemies):
                enemy_x = left_margin + col * (self.enemy_width + self.enemy_spacing)
                enemy_y = self.enemy_start_y + row * (
                    self.enemy_height + self.enemy_spacing
                )
                if row == 0 or row == 1:
                    point_val = 30
                elif row == 2 or row == 3:
                    point_val = 20
                else:
                    point_val = 10
                enemy_rect = Enemy(
                    enemy_x, enemy_y, self.enemy_width, self.enemy_height, point_val
                )
                row_enemies.append(enemy_rect)

            self.enemies.append(row_enemies)
            self.enemies_that_can_shoot = self.enemies[-1]
