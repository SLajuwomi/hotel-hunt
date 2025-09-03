import pygame

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

top_of_triangle = (screen_width // 2, screen_height - 30)
bot_left_triangle = (screen_width // 2 - 20, screen_height)
bot_right_triangle = (screen_width // 2 + 20, screen_height)
triangle_vertices = [top_of_triangle, bot_left_triangle, bot_right_triangle]
triangle_color = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, triangle_color, triangle_vertices)
    pygame.display.flip()

pygame.quit()
