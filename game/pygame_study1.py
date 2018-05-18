import math
import pygame
import sys,time 
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("Drawing Arcs")

i=0
while True:
    i+=1
    for event in pygame.event.get():
        if event.type in (QUIT,):
            pygame.quit()
            sys.exit()
        if event.type in (MOUSEBUTTONDOWN,):
            screen.fill((0,200,0))
        else:
            screen.fill((0,0,200))
    time.sleep(0.5) 
    keys = pygame.key.get_pressed()
    if keys[K_0] == True:
        print(keys[K_0]) 
    #绘制弧形的代码
    color = 255,0,255
    position = 200,150,200,200
    start_angle = math.radians(0)
    end_angle = math.radians(180)
    
    width = 8
    pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
    
    pygame.display.update()
