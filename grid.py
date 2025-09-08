from enemy import Enemy


class Grid:
    def __init__(self, num_rows, max_enemies, left_margin, enemy_width, spacing):
        self.num_rows = num_rows
        self.max_enemies = max_enemies
        self.left_margin = left_margin
        self.enemy_width = enemy_width
        self.spacing = spacing

    def make_grid(self):
        for row in range(self.num_rows):
            row_enemies = []
            for col in range(self.max_enemies):
                enemy_x = self.left_margin + col * (self.enemy_width + self.spacing)
                enemy_y = self.enemy_start_y + row * (self.enemy_height + self.spacing)
                if row == 0 or row == 1:
                    point_val = 30
                elif row == 2 or row == 3:
                    point_val = 20
                else:
                    point_val = 10
                enemy_rect = Enemy(
                    self.enemy_x, enemy_y, self.enemy_width, enemy_height, point_val
                )
                row_enemies.append(enemy_rect)
            enemies.append(row_enemies)
