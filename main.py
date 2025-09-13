import pygame
from game import Game
from barrier import Barrier


screen = pygame.display.set_mode((640, 480))
game = Game(screen, "menu")
game.run("menu")
