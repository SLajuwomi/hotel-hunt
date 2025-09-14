import pygame
import random
import sys
from player import Player
from enemy import Enemy
from barrier import Barrier
import settings


class Game:

    def __init__(self, screen, state):
        self.screen = screen
        self.screen_h = self.screen.get_height()
        self.screen_w = self.screen.get_width()
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.state = state

        self.player_bullets = []

        self.player = Player(
            self.screen_w // 2,
            self.screen_h - 60,
            settings.PLAYER_SPEED,
            settings.PLAYER_LIVES,
            self.player_bullets,
        )
        self.player_bullet_speed = settings.PLAYER_BULLET_SPEED

        self.enemies = []
        self.enemy_bullets = []
        self.enemies_that_can_shoot = []
        self.enemy_direction = 1
        self.enemy_speed = settings.ENEMY_SPEED
        self.enemy_width = settings.ENEMY_WIDTH
        self.enemy_height = settings.ENEMY_HEIGHT
        self.enemy_spacing = settings.ENEMY_SPACING
        self.enemy_side_margin = settings.ENEMY_SIDE_MARGIN
        self.enemy_rows = settings.ENEMY_ROWS
        self.enemy_start_y = settings.ENEMY_STARY_Y
        self.last_enemy_shot_time = 0
        self.enemy_shot_interval = settings.ENEMY_SHOT_INTERVAL
        self.enemy_move_interval = settings.ENEMY_MOVE_INTERVAL
        self.enemy_max_speed_interval = settings.ENEMY_MAX_SPEED_INTERVAL
        self.enemy_bullet_speed = settings.ENEMY_BULLET_SPEED
        self.enemy_killed = False

        self.last_enemy_move_time = 0

        self.usable_width = (
            self.screen_w - self.enemy_side_margin - self.enemy_side_margin
        )
        self.max_enemies = (self.usable_width + self.enemy_spacing) // (
            self.enemy_width + self.enemy_spacing
        )

        self.enemy_alive_count = self.max_enemies * self.enemy_rows

        self.total_enemies = self.max_enemies * self.enemy_rows

        self.triangle_color = settings.PLAYER_LIVES_TRI_COLOR
        self.player_lives_triangle_x = settings.PLAYER_LIVES_TRI_X

        self.score = 0
        self.level = 1
        self.current_time = 0

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)

        self.barrier1 = Barrier(settings.BARRIER_X, settings.BARRIER_Y)
        self.barrier2 = Barrier(
            self.barrier1.orig_barrier_img.get_width() + self.barrier1.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier3 = Barrier(
            self.barrier2.orig_barrier_img.get_width() + self.barrier2.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier4 = Barrier(
            self.barrier3.orig_barrier_img.get_width() + self.barrier3.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier5 = Barrier(
            self.barrier4.orig_barrier_img.get_width() + self.barrier4.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier6 = Barrier(
            self.barrier5.orig_barrier_img.get_width() + self.barrier5.x + 40,
            settings.BARRIER_Y,
        )

        self.all_barriers = []
        self.all_barriers.append(self.barrier1)
        self.all_barriers.append(self.barrier2)
        self.all_barriers.append(self.barrier3)
        self.all_barriers.append(self.barrier4)
        self.all_barriers.append(self.barrier5)
        self.all_barriers.append(self.barrier6)

        self.player_ship = pygame.image.load(
            "game-art/space-invaders-ship.png"
        ).convert_alpha()
        self.player_ship_rect = self.player_ship.get_rect()
        self.player_ship_rect.center = (self.screen_w // 2, self.screen_h - 60)
        print(self.player_ship_rect.x)

        self.create_enemy_grid()

    def run(self, state):
        self.player.lives = 3
        while self.is_running:
            if state == "menu":
                self.draw_menu()
            if state == "playing":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.shoot()
                        if event.key == pygame.K_s:
                            self.level += 1
                            self.start_new_level()
                self.enemy_killed = False

                self.update()
                self.draw()
            if state == "game_over":
                # print game over and final score
                self.game_over_screen()
            if state == "restart":
                self.restart_game()
        pygame.quit()

    def draw_menu(self):
        start = self.font.render("START", True, settings.FONT_COLOR)
        quit = self.font.render("QUIT", True, settings.FONT_COLOR)
        quit_rect = quit.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 40))
        start_rect = start.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 - 20)
        )
        self.screen.fill((0, 0, 0))
        self.screen.blit(start, start_rect)
        self.screen.blit(quit, quit_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    self.run("playing")
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
        pygame.display.flip()

    def restart_game(self):
        self.is_running = True
        self.clock = pygame.time.Clock()

        self.player_bullets = []

        self.player = Player(
            self.screen_w // 2,
            self.screen_h - 60,
            settings.PLAYER_SPEED,
            settings.PLAYER_LIVES,
            self.player_bullets,
        )
        self.player_bullet_speed = settings.PLAYER_BULLET_SPEED

        self.enemies = []
        self.enemy_bullets = []
        self.enemies_that_can_shoot = []
        self.enemy_direction = 1
        self.enemy_speed = settings.ENEMY_SPEED
        self.enemy_width = settings.ENEMY_WIDTH
        self.enemy_height = settings.ENEMY_HEIGHT
        self.enemy_spacing = settings.ENEMY_SPACING
        self.enemy_side_margin = settings.ENEMY_SIDE_MARGIN
        self.enemy_rows = settings.ENEMY_ROWS
        self.enemy_start_y = settings.ENEMY_STARY_Y
        self.last_enemy_shot_time = 0
        self.enemy_shot_interval = settings.ENEMY_SHOT_INTERVAL
        self.enemy_move_interval = settings.ENEMY_MOVE_INTERVAL
        self.enemy_max_speed_interval = settings.ENEMY_MAX_SPEED_INTERVAL
        self.enemy_bullet_speed = settings.ENEMY_BULLET_SPEED
        self.enemy_killed = False

        self.last_enemy_move_time = 0

        self.usable_width = (
            self.screen_w - self.enemy_side_margin - self.enemy_side_margin
        )
        self.max_enemies = (self.usable_width + self.enemy_spacing) // (
            self.enemy_width + self.enemy_spacing
        )

        self.enemy_alive_count = self.max_enemies * self.enemy_rows

        self.total_enemies = self.max_enemies * self.enemy_rows

        self.triangle_color = settings.PLAYER_LIVES_TRI_COLOR
        self.player_lives_triangle_x = settings.PLAYER_LIVES_TRI_X

        self.score = 0
        self.level = 1
        self.current_time = 0

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)

        self.barrier1 = Barrier(settings.BARRIER_X, settings.BARRIER_Y)
        self.barrier2 = Barrier(
            self.barrier1.orig_barrier_img.get_width() + self.barrier1.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier3 = Barrier(
            self.barrier2.orig_barrier_img.get_width() + self.barrier2.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier4 = Barrier(
            self.barrier3.orig_barrier_img.get_width() + self.barrier3.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier5 = Barrier(
            self.barrier4.orig_barrier_img.get_width() + self.barrier4.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier6 = Barrier(
            self.barrier5.orig_barrier_img.get_width() + self.barrier5.x + 40,
            settings.BARRIER_Y,
        )

        self.all_barriers = []
        self.all_barriers.append(self.barrier1)
        self.all_barriers.append(self.barrier2)
        self.all_barriers.append(self.barrier3)
        self.all_barriers.append(self.barrier4)
        self.all_barriers.append(self.barrier5)
        self.all_barriers.append(self.barrier6)

        self.create_enemy_grid()
        self.run("playing")

    def game_over_screen(self):
        game_over = self.font.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 - 60)
        )
        final_score = self.font.render(f"{self.score}", True, settings.FONT_COLOR)
        final_score_rect = final_score.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 - 20)
        )
        start_over = self.font.render("START OVER!", True, settings.FONT_COLOR)
        start_over_rect = start_over.get_rect(
            center=(self.screen_w // 2, self.screen_h // 2 + 40)
        )
        quit = self.font.render("QUIT", True, settings.FONT_COLOR)
        quit_rect = quit.get_rect(center=(self.screen_w // 2, self.screen_h // 2 + 80))

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(final_score, final_score_rect)
        self.screen.blit(start_over, start_over_rect)
        self.screen.blit(quit, quit_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_over_rect.collidepoint(event.pos):
                    self.run("restart")
                if quit_rect.collidepoint(event.pos):
                    print("Thanks for playing!")
                    pygame.quit()
            pygame.display.flip()

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.player.move()

        for row in self.enemies:
            for enemy in row:
                if enemy.is_alive:
                    enemy.update()

        for player_bullet in list(self.player_bullets):
            player_bullet.update(self.player_bullet_speed)
            bullet_removed = False
            if not bullet_removed and (player_bullet.rect.bottom < 0):
                self.player_bullets.remove(player_bullet)
                bullet_removed = True
            if not bullet_removed:
                for barrier in self.all_barriers:
                    if barrier.barrier_list:
                        if player_bullet.rect.colliderect(barrier.barrier_list[0]):
                            self.player_bullets.remove(player_bullet)
                            barrier.barrier_list.pop(0)
                            barrier.barrier_imgs_list.pop(0)
                            bullet_removed = True
                            break
            if not bullet_removed:
                hit_enemy = False
                for row in range(len(self.enemies)):
                    for col in range(len(self.enemies[row])):
                        if self.enemies[row][col].is_alive:
                            if player_bullet.rect.colliderect(
                                self.enemies[row][col].rect
                            ):
                                self.enemy_killed = True
                                self.player_bullets.remove(player_bullet)
                                self.score += self.enemies[row][col].point_value
                                self.enemy_alive_count -= 1
                                self.enemies[row][col].is_alive = False
                                if (
                                    self.enemies[row][col]
                                    in self.enemies_that_can_shoot
                                ):
                                    self.enemies_that_can_shoot.remove(
                                        self.enemies[row][col]
                                    )
                                    if self.enemies[row - 1][col].is_alive:
                                        self.enemies_that_can_shoot.append(
                                            self.enemies[row - 1][col]
                                        )
                                hit_enemy = True
                                break
                    if hit_enemy:
                        break

        self.percent_enemies_killed = (
            self.total_enemies - self.enemy_alive_count
        ) / self.total_enemies

        speed_range = self.enemy_move_interval - self.enemy_max_speed_interval
        interval_reduction = 0
        if self.enemy_killed:
            interval_reduction = speed_range * self.percent_enemies_killed
        self.enemy_move_interval = self.enemy_move_interval - interval_reduction

        reverse_needed = False
        if self.current_time - self.last_enemy_move_time > self.enemy_move_interval:
            for row in self.enemies:
                for enemy in row:
                    if enemy.is_alive:
                        enemy.rect.x += self.enemy_direction * self.enemy_speed
                        if enemy.rect.colliderect(self.player.rect):
                            print("You have been hit!")
                            self.run("game_over")
            for row in range(len(self.enemies)):
                for col in range(len(self.enemies[row])):
                    if self.enemies[row][col].is_alive:
                        if (
                            self.enemies[row][col].rect.bottomleft[0] <= 0
                            or self.enemies[row][col].rect.bottomright[0]
                            >= self.screen_w
                        ):
                            reverse_needed = True
            if reverse_needed:
                self.enemy_direction *= -1
                for nested_row in self.enemies:
                    for enemy in nested_row:
                        if enemy.is_alive:
                            enemy.rect.y += 5
            self.last_enemy_move_time = self.current_time

        print("current time", self.current_time)

        if self.current_time - self.last_enemy_shot_time > self.enemy_shot_interval:
            if self.enemies_that_can_shoot:
                shooter = random.choice(self.enemies_that_can_shoot)
                self.enemy_bullets.append(shooter.shoot())
                self.last_enemy_shot_time = self.current_time

        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.update(self.enemy_bullet_speed)
            if enemy_bullet.rect.colliderect(self.player.rect):
                self.player.lives -= 1
                self.enemy_bullets.remove(enemy_bullet)
                if self.player.lives == 0:
                    print("GAME OVER!")
                    self.run("game_over")
            for barrier in self.all_barriers:
                if barrier.barrier_list:
                    if enemy_bullet.rect.colliderect(barrier.barrier_list[0]):
                        self.enemy_bullets.remove(enemy_bullet)
                        barrier.barrier_list.pop(0)
                        barrier.barrier_imgs_list.pop(0)
                        break

            if (
                enemy_bullet.rect.y > self.screen.get_height()
                or enemy_bullet.rect.y < 0
            ):
                self.enemy_bullets.remove(enemy_bullet)
        if self.enemy_alive_count == 0:
            self.level += 1
            self.start_new_level()

        pygame.display.flip()
        self.clock.tick(60)

    def start_new_level(self):
        self.is_running = True
        self.clock = pygame.time.Clock()

        self.player_bullets = []

        self.player = Player(
            self.screen_w // 2,
            self.screen_h - 60,
            settings.PLAYER_SPEED,
            settings.PLAYER_LIVES,
            self.player_bullets,
        )
        self.player_bullet_speed = settings.PLAYER_BULLET_SPEED

        self.enemies = []
        self.enemy_bullets = []
        self.enemies_that_can_shoot = []
        self.enemy_direction = 1
        self.enemy_speed = settings.ENEMY_SPEED
        self.enemy_width = settings.ENEMY_WIDTH
        self.enemy_height = settings.ENEMY_HEIGHT
        self.enemy_spacing = settings.ENEMY_SPACING
        self.enemy_side_margin = settings.ENEMY_SIDE_MARGIN
        self.enemy_rows = settings.ENEMY_ROWS
        self.enemy_start_y = settings.ENEMY_STARY_Y + ((self.level - 1) * 10)
        self.last_enemy_shot_time = 0
        self.enemy_shot_interval = settings.ENEMY_SHOT_INTERVAL
        self.enemy_move_interval = settings.ENEMY_MOVE_INTERVAL
        self.enemy_max_speed_interval = settings.ENEMY_MAX_SPEED_INTERVAL
        self.enemy_bullet_speed = settings.ENEMY_BULLET_SPEED
        self.enemy_killed = False

        self.last_enemy_move_time = 0

        self.usable_width = (
            self.screen_w - self.enemy_side_margin - self.enemy_side_margin
        )
        self.max_enemies = (self.usable_width + self.enemy_spacing) // (
            self.enemy_width + self.enemy_spacing
        )

        self.enemy_alive_count = self.max_enemies * self.enemy_rows

        self.total_enemies = self.max_enemies * self.enemy_rows

        self.triangle_color = settings.PLAYER_LIVES_TRI_COLOR
        self.player_lives_triangle_x = settings.PLAYER_LIVES_TRI_X

        self.score = self.score
        self.current_time = 0

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)

        self.barrier1 = Barrier(settings.BARRIER_X, settings.BARRIER_Y)
        self.barrier2 = Barrier(
            self.barrier1.orig_barrier_img.get_width() + self.barrier1.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier3 = Barrier(
            self.barrier2.orig_barrier_img.get_width() + self.barrier2.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier4 = Barrier(
            self.barrier3.orig_barrier_img.get_width() + self.barrier3.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier5 = Barrier(
            self.barrier4.orig_barrier_img.get_width() + self.barrier4.x + 40,
            settings.BARRIER_Y,
        )
        self.barrier6 = Barrier(
            self.barrier5.orig_barrier_img.get_width() + self.barrier5.x + 40,
            settings.BARRIER_Y,
        )

        self.all_barriers = []
        self.all_barriers.append(self.barrier1)
        self.all_barriers.append(self.barrier2)
        self.all_barriers.append(self.barrier3)
        self.all_barriers.append(self.barrier4)
        self.all_barriers.append(self.barrier5)
        self.all_barriers.append(self.barrier6)

        self.create_enemy_grid()
        self.run("playing")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen, self.triangle_color)

        for barrier in self.all_barriers:
            if barrier.barrier_list:
                current_rect = barrier.barrier_list[0]
                current_img = barrier.barrier_imgs_list[0]
                self.screen.blit(current_img, current_rect)

        score_surface = self.font.render(f"{self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))
        for row in self.enemies:
            for enemy in row:
                if enemy.is_alive:
                    self.screen.blit(enemy.image, enemy.rect)

        for enemy_bullet in list(self.enemy_bullets):
            # make into images
            self.screen.blit(enemy_bullet.image, enemy_bullet.rect)

        for player_bullet in list(self.player.bullets):
            self.screen.blit(player_bullet.image, player_bullet.rect)

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
        alien_level = 0

        for row in range(self.enemy_rows):
            row_enemies = []
            for col in range(self.max_enemies):
                enemy_x = self.enemy_side_margin + col * (
                    self.enemy_width + self.enemy_spacing
                )
                enemy_y = self.enemy_start_y + row * (
                    self.enemy_height + self.enemy_spacing
                )
                if row == 0:
                    point_val = 30
                    alien_level = 3
                elif row == 1 or row == 2:
                    point_val = 20
                    alien_level = 2
                else:
                    point_val = 10
                    alien_level = 1
                enemy_rect = Enemy(enemy_x, enemy_y, point_val, alien_level)
                row_enemies.append(enemy_rect)

            self.enemies.append(row_enemies)
        self.enemies_that_can_shoot = list(self.enemies[-1])
