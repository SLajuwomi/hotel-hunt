from re import S
import pygame
import random

pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

player_x = screen_width // 2
player_y_top = screen_height - 20
player_speed = 2
triangle_color = (255, 255, 255)
clock = pygame.time.Clock()

enemy_width = 40
enemy_height = 30
enemy_bullets = []
enemy_shot_interval = 2000
enemies_that_can_shoot = []
last_enemy_shot_time = 0
spacing = 10
left_margin = 50
right_margin = 50

usable_width = screen_width - left_margin - right_margin
max_enemies = (usable_width + spacing) // (enemy_width + spacing)

enemies = []
num_rows = 5
enemy_start_y = 50
enemy_direction = 1
enemy_speed = 1
enemy_move_interval = 125
last_enemy_move_time = 0
for row in range(num_rows):
    row_enemies = []
    for col in range(max_enemies):
        enemy_x = left_margin + col * (enemy_width + spacing)
        enemy_y = enemy_start_y + row * (enemy_height + spacing)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        row_enemies.append(enemy_rect)
    enemies.append(row_enemies)

bullets = []


running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x, player_y_top, 5, 5))

    current_time = pygame.time.get_ticks()

    for col in range(max_enemies):
        for row in reversed(range(len(enemies))):
            if col < len(enemies[row]):
                enemy = enemies[row][col]
                if enemy is not None:
                    enemies_that_can_shoot.append(enemy)
                    break
    if current_time - last_enemy_shot_time > enemy_shot_interval:
        if enemies_that_can_shoot:
            shooter = random.choice(enemies_that_can_shoot)
            enemy_bullets.append(pygame.Rect(shooter.centerx, shooter.bottom, 5, 5))
            last_enemy_shot_time = current_time

    # if current_time - last_enemy_shot_time > enemy_shot_interval:
    #     for row in list(enemies):
    #         picked_enemy = random.choice(row)
    #         if picked_enemy:
    #             enemy_bullets.append(
    #                 pygame.Rect(picked_enemy.centerx, picked_enemy.bottom, 5, 5)
    #             )
    #             last_enemy_shot_time = current_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    screen.fill((0, 0, 0))

    top_of_triangle = (player_x, screen_height - 20)
    bot_left_triangle = (player_x - 10, screen_height)
    bot_right_triangle = (player_x + 10, screen_height)
    triangle_vertices = [top_of_triangle, bot_left_triangle, bot_right_triangle]

    pygame.draw.polygon(screen, triangle_color, triangle_vertices)

    reverse_needed = False
    if current_time - last_enemy_move_time > enemy_move_interval:
        for row in enemies:
            for enemy in row:
                if enemy is not None:
                    enemy.x += enemy_direction * enemy_speed
        for row in enemies:
            if row[0].bottomleft[0] <= 0 or row[-1].bottomright[0] >= screen_width:
                reverse_needed = True
        if reverse_needed:
            enemy_direction *= -1
            for nested_row in enemies:
                for enemy in nested_row:
                    if enemy is not None:
                        enemy.y += 5
        last_enemy_move_time = current_time

    for row in enemies:
        for enemy in row:
            if enemy is not None:
                pygame.draw.rect(screen, (255, 0, 0), enemy)

    for enemy_bullet in list(enemy_bullets):
        enemy_bullet.y += 5
        pygame.draw.rect(screen, (0, 255, 0), enemy_bullet)
        if enemy_bullet.y > screen_height or enemy_bullet.y < 0:
            enemy_bullets.remove(enemy_bullet)

    for bullet in list(bullets):
        bullet.top -= 5
        pygame.draw.rect(screen, (255, 0, 0), bullet)
        if bullet.top > screen_height or bullet.top < 0:
            bullets.remove(bullet)
        for row in range(len(enemies)):
            for col in range(len(enemies[row])):
                if enemies[row][col] is not None:
                    if bullet.colliderect(enemies[row][col]):
                        bullets.remove(bullet)
                        enemies[row][col] = None
                        break

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
