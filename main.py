import pygame

pygame.init()
screen_width = 800
screen_height = 600
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
num_rows = 3
enemy_start_y = 50

for row in range(num_rows):
    row_enemies = []
    for col in range(max_enemies):
        x = left_margin + col * (enemy_width + spacing)
        y = enemy_start_y + row * (enemy_height + spacing)
        enemy_rect = pygame.Rect(x, y, enemy_width, enemy_height)
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

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
