import pygame
from game import Game

screen = pygame.display.set_mode((640, 480))
game = Game(screen)
game.run()
