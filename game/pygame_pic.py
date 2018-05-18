import sys,random,math,pygame
from pygame.locals import * 

pygame.init()

screen =pygame.display.set_mode((800,600))

pygame.display.set_caption("space")

font =pygame.font.Font(None,18)
clock = pygame.time.Clock()

plane = pygame.image.load("new.png").convert_alpha()
x,y = plane.get_size()
while True:
    for evnet in pygame.event.get():
        if evnet.type==QUIT:
            sys.exit()
    screen.fill((0,0,200))
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
         sys.exit()
    screen.blit(plane, (400-x/2,300-y/2))
    
    pygame.display.update()
    clock.tick(100)

