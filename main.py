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

    for bullet in list(bullets):
        bullet.top -= 5
        pygame.draw.rect(screen, (255, 0, 0), bullet)
        if bullet.top > screen_height or bullet.top < 0:
            bullets.remove(bullet)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
