import pygame
import random
import sys
from enemy import Enemy


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

screen_width = 640
screen_height = 480
footer_height = 40
screen = pygame.display.set_mode((screen_width, screen_height))


player_x = screen_width // 2
player_y_top = screen_height - footer_height - 20
player_speed = 2
player_lives = 3
player_lives_triangle_x = 20
player_score = 0
point_val = 0
triangle_color = (255, 255, 255)

clock = pygame.time.Clock()

enemy_width = 40
enemy_height = 30
enemy_bullets = []
enemy_shot_interval = 1000
enemies_that_can_shoot = []
last_enemy_shot_time = 0
spacing = 10
left_margin = 50
right_margin = 50

usable_width = screen_width - left_margin - right_margin
max_enemies = (usable_width + spacing) // (enemy_width + spacing)
# 540 + 10 // 40 + 10 == 11
enemies = []
num_rows = 5
enemy_start_y = 50
enemy_direction = 1
enemy_alive_count = max_enemies * num_rows
enemy_speed = 1
enemy_move_interval = 125
last_enemy_move_time = 0
for row in range(num_rows):
    row_enemies = []
    for col in range(max_enemies):
        enemy_x = left_margin + col * (enemy_width + spacing)
        enemy_y = enemy_start_y + row * (enemy_height + spacing)
        if row == 0 or row == 1:
            point_val = 30
        elif row == 2 or row == 3:
            point_val = 20
        else:
            point_val = 10
        enemy_rect = Enemy(enemy_x, enemy_y, enemy_width, enemy_height, point_val)
        row_enemies.append(enemy_rect)
    enemies.append(row_enemies)

bullets = []


running = True

decremented45 = False
decremented35 = False
decremented25 = False
decremented15 = False
decremented5 = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_x, player_y_top, 5, 5))

    current_time = pygame.time.get_ticks()

    # Enemy shooting
    enemies_that_can_shoot = []
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

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    screen.fill((0, 0, 0))

    # Print Player score
    score_surface = font.render(f"{player_score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    top_of_triangle = (player_x, screen_height - footer_height - 20)
    bot_left_triangle = (player_x - 10, screen_height - footer_height)
    bot_right_triangle = (player_x + 10, screen_height - footer_height)
    triangle_vertices = [top_of_triangle, bot_left_triangle, bot_right_triangle]

    player = pygame.draw.polygon(screen, triangle_color, triangle_vertices)

    if enemy_alive_count <= 45 and enemy_alive_count > 35 and not decremented45:
        print("here2")
        enemy_move_interval -= 45
        decremented45 = True
    elif enemy_alive_count <= 35 and enemy_alive_count > 25 and not decremented35:
        print("here3")
        enemy_move_interval -= 45
        decremented35 = True
    elif enemy_alive_count <= 25 and enemy_alive_count > 15 and not decremented25:
        print("here4")
        enemy_move_interval -= 45
        decremented25 = True
    elif enemy_alive_count <= 15 and enemy_alive_count > 5 and not decremented15:
        print("here5")
        enemy_move_interval -= 45
        decremented15 = True
    elif enemy_alive_count <= 5 and not decremented5:
        print("here6")
        enemy_move_interval -= 45
        decremented5 = True
    # print("move interval", enemy_move_interval)
    # print("alive count", enemy_alive_count)

    # Enemy movement and reversal
    # print("will move", current_time)
    # print("last enemy move time", last_enemy_move_time)
    # print("enemy_move_interval", enemy_move_interval)
    reverse_needed = False
    if current_time - last_enemy_move_time > enemy_move_interval:
        for row in enemies:
            for enemy in row:
                if enemy is not None:
                    enemy.x += enemy_direction * enemy_speed
        for col in range(max_enemies):
            for row in range(len(enemies)):
                if enemies[row][col] is not None:
                    if (
                        enemies[row][col].bottomleft[0] <= 0
                        or enemies[row][col].bottomright[0] >= screen_width
                    ):
                        reverse_needed = True
        if reverse_needed:
            enemy_direction *= -1
            for nested_row in enemies:
                for enemy in nested_row:
                    if enemy is not None:
                        enemy.y += 5
        last_enemy_move_time = current_time

    # Drawing enemies to screen
    for row in enemies:
        for enemy in row:
            if enemy is not None:
                pygame.draw.rect(screen, (255, 0, 0), enemy)

    # Drawing enemy bullets and damaging player
    for enemy_bullet in list(enemy_bullets):
        enemy_bullet.y += 5
        pygame.draw.rect(screen, (0, 255, 0), enemy_bullet)
        if enemy_bullet.colliderect(player):
            player_lives -= 1
            enemy_bullets.remove(enemy_bullet)
            if player_lives == 0:
                print("GAME OVER!")
                sys.exit()
        if enemy_bullet.y > screen_height or enemy_bullet.y < 0:
            enemy_bullets.remove(enemy_bullet)

    for i in range(player_lives):
        if player_lives > 0:
            life_tri_x = player_lives_triangle_x + (20 * i)
            life_tri_top = (life_tri_x, screen_height - 20)
            life_tri_bot_left = (life_tri_x - 10, screen_height)
            life_tri_bot_right = (life_tri_x + 10, screen_height)
            life_tri_vertices = [life_tri_top, life_tri_bot_left, life_tri_bot_right]
            pygame.draw.polygon(screen, triangle_color, life_tri_vertices)

    # Player shooting and killing enemies
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
                        player_score += enemies[row][col].point_value
                        enemy_alive_count -= 1
                        enemies[row][col] = None
                        break

    fps_surface = font.render(f"{str(int(clock.get_fps()))}", True, (255, 255, 255))
    screen.blit(fps_surface, (590, 10))
    pygame.display.flip()

    clock.tick(60)


pygame.quit()
