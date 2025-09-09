import pygame
import random
import sys
from player import Player
from enemy import Enemy


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.screen_h = self.screen.get_height()
        self.screen_w = self.screen.get_width()
        self.is_running = True

        self.player_bullets = []

        self.player = Player(
            self.screen.get_width() // 2,
            self.screen.get_height() - 60,
            2,
            3,
            self.player_bullets,
        )
        self.player_bullet_speed = 5

        self.enemies = []
        self.enemy_bullets = []
        self.enemies_that_can_shoot = []
        self.enemy_direction = 1
        self.enemy_speed = 1
        self.enemy_width = 40
        self.enemy_height = 30
        self.enemy_spacing = 10
        self.enemy_rows = 5
        self.enemy_start_y = 50
        self.enemy_side_margin = 50
        self.last_enemy_shot_time = 0
        self.enemy_shot_interval = 1000
        self.enemy_move_interval = 125
        self.enemy_bullet_speed = 5
        self.last_enemy_move_time = 0

        self.usable_width = (
            self.screen_w - self.enemy_side_margin - self.enemy_side_margin
        )
        self.max_enemies = (self.usable_width + self.enemy_spacing) // (
            self.enemy_width + self.enemy_spacing
        )

        self.enemy_alive_count = self.max_enemies * self.enemy_rows

        self.triangle_color = (255, 255, 255)
        self.player_lives_triangle_x = 20

        self.score = 0
        self.level = 1
        self.current_time = pygame.time.get_ticks()

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)

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
        self.player.move()

        for player_bullet in list(self.player_bullets):
            player_bullet.top -= self.player_bullet_speed
            if player_bullet.top > self.screen_h or player_bullet.top < 0:
                self.player_bullets.remove(player_bullet)
            for row in range(len(self.enemies)):
                for col in range(len(self.enemies[row])):
                    if self.enemies[row][col].is_alive:
                        if player_bullet.colliderect(self.enemies[row][col]):
                            self.player_bullets.remove(player_bullet)
                            self.score += self.enemies[row][col].point_value
                            self.enemy_alive_count -= 1
                            self.enemies[row][col].is_alive = False
                            break
        reverse_needed = False
        if self.current_time - self.last_enemy_move_time > self.enemy_move_interval:
            for row in self.enemies:
                for enemy in row:
                    if enemy.is_alive:
                        enemy.x += self.enemy_direction * self.enemy_speed
            for row in range(len(self.enemies)):
                for col in range(len(self.enemies[row])):
                    if self.enemies[row][col].is_alive
                

        if self.current_time - self.last_enemy_shot_time > self.enemy_shot_interval:
            if self.enemies_that_can_shoot:
                shooter = random.choice(self.enemies_that_can_shoot)
                self.enemy_bullets.append(shooter.shoot())
                self.last_enemy_shot_time = self.current_time

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.y += self.enemy_bullet_speed
            if enemy_bullet.colliderect(self.player.rect):
                self.player.lives -= 1
                self.enemy_bullets.remove(enemy_bullet)
                if self.player.lives == 0:
                    print("GAME OVER!")
                    sys.exit()
            if enemy_bullet.y > self.screen.get_height() or enemy_bullet.y < 0:
                self.enemy_bullets.remove(enemy_bullet)

        pygame.display.flip()

    def draw(self):
        self.screen.fill((0, 0, 0))

        Player.draw(self.screen, self.triangle_color)

        score_surface = self.font.render(f"{self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface)

        for row in self.enemies:
            for enemy in row:
                if enemy.is_alive:
                    pygame.draw.rect(self.screen, (255, 0, 0), enemy)

        for enemy_bullet in list(self.enemy_bullets):
            pygame.draw.rect(self.screen, (0, 255, 0), enemy_bullet)

        for player_bullet in list(self.player.bullets):
            pygame.draw.rect(self.screen, (255, 0, 0), player_bullet)

        for i in range(self.player.lives):
            if self.player.lives > 0:
                life_tri_x = self.player_lives_triangle_x + (20 * i)
                life_tri_top = (life_tri_x, self.screen.get_height() - 20)
                life_tri_bot_left = (life_tri_x - 10, self.screen.get_height())
                life_tri_bot_right = (life_tri_x + 10, self.screen.get_height())
                life_tri_vertices = [
                    life_tri_top,
                    life_tri_bot_left,
                    life_tri_bot_right,
                ]
                pygame.draw.polygon(self.screen, self.triangle_color, life_tri_vertices)

    def create_enemy_grid(self):
        self.enemies.clear()
        point_val = 0

        for row in range(self.enemy_rows):
            row_enemies = []
            for col in range(self.max_enemies):
                enemy_x = self.enemy_side_margin + col * (
                    self.enemy_width + self.enemy_spacing
                )
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
                    enemy_x,
                    enemy_y,
                    self.enemy_width,
                    self.enemy_height,
                    point_val,
                    is_alive=True,
                )
                row_enemies.append(enemy_rect)

            self.enemies.append(row_enemies)
            self.enemies_that_can_shoot = self.enemies[-1]
