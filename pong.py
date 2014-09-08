import pygame
import time
import os

size = (1000,600)

pos_x = 1366/2 - size[0]/2
pos_y = 768 - 700

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Keyboard")

image1 = pygame.image.load("ball.png")
image2 = pygame.image.load("paddle.png")

screen.blit(image1,(100,100))
screen.blit(image2,(200,200))

pygame.display.flip()
time.sleep(15)
