import components
import pygame #in built library

win_height = 550
win_width = 550
window = pygame.display.set_mode((win_width, win_height))

ground = components.Ground(win_width)
pipes = []