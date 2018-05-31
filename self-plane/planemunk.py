#!/usr/bin/python

import random
import math
import pymunk
import numpy as np

import pygame
from pygame.color import THECOLORS

from pymunk.vec2d import Vec2d
from pymunk.pygame_util import draw
import time
# The size of the screen to display
WIDTH = 1920
HEIGHT= 1080


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Self-Flying Demo")

clock = pygame.time.Clock()
screen.set_alpha(None)

show_sensors = True
draw_screen = True

class Demo(object):
    def __init__(self):
        self.crashed = False
        self.space = pymunk.Space()
        self.space.gravity=Vec2d((0.,0.))
        self.create_plane(100, 100, 0.5)
        
        static = [
            pymunk.Segment(
                self.space.static_body,
                (0,1),(0,HEIGHT),1),
            pymunk.Segment(
                self.space.static_body,
                (1,HEIGHT),(WIDTH,HEIGHT),1),
            pymunk.Segment(
                self.space.static_body,
                (WIDTH-1,HEIGHT),(WIDTH-1,1),1),
            pymunk.Segment(
                self.space.static_body,
                (1,1),(WIDTH,1),1)
            ]
        for s in static:
            s.frition = 1.
            s.gropu = 1
            s.collision_type=1
            s.color = THECOLORS['red']
        self.space.add(static)
        
    def create_plane(self,x,y,r):
        """
        x,y positon ,r the angle
        """
        inertia = pymunk.moment_for_circle(1, 0, 14,(0,0))
        self.plane_body = pymunk.Body(1,inertia)
        self.plane_body.position = x,y
        self.plane_shape = pymunk.Circle(self.plane_body,25)
        self.plane_shape.color = THECOLORS['green']
        self.plane_shape.elasticity = 1.0
        self.plane_body.angle = r
        flying_direction = Vec2d(1,0).rotated(self.plane_body.angle)
        self.plane_body.apply_impulse(flying_direction)
        self.space.add(self.plane_body,self.plane_shape)
    
    def set_target(self,x,y,r):
        target_body = pymunk.Body(pymunk.inf,pymunk.inf)
        target_shape = pymunk.Circle(target_body,r)
        target_shape.elasticity = 1.0
        target_body.position = x,y
        target_shape.color = THECOLORS['blue']
        self.space.add(target_body,target_shape)
        return target_body
            
    def frame_step(self,action):
        if action == 0:
            self.plane_body.angle -= .2
        if action == 1:
            self.plane_body.angle += .2
        
        flying_direction = Vec2d(1,0).rotated(self.plane_body.angle)
        self.plane_body.velocity = 100 * flying_direction
        
        screen.fill(THECOLORS["black"])
        draw(screen,self.space)
        self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()

if __name__ == "__main__":
    plane = Demo()
    plane.set_target(1900, 600,50)
    while True:
        plane.frame_step(random.randint(0,2))
        time.sleep(0.05)
