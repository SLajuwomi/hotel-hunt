import pygame

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
                enemy.x += enemy_direction * enemy_speed
        for row in enemies:
            if row[0].bottomleft[0] <= 0 or row[-1].bottomright[0] >= screen_width:
                reverse_needed = True
        if reverse_needed:
            enemy_direction *= -1
            for nested_row in enemies:
                for enemy in nested_row:
                    enemy.y += 5
        last_enemy_move_time = current_time

    for row in enemies:
        for enemy in row:
            pygame.draw.rect(screen, (255, 0, 0), enemy)

    for bullet in list(bullets):
        bullet.top -= 5
        pygame.draw.rect(screen, (255, 0, 0), bullet)
        if bullet.top > screen_height or bullet.top < 0:
            bullets.remove(bullet)
        for row in list(enemies):
            for enemy in list(row):
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    row.remove(enemy)
                    break

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
