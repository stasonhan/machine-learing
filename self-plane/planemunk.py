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
from turtledemo import planet_and_moon
from _codecs import charmap_build
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
        self.create_plane(0, 0, 0.5)
        
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
        
    def get_state(self,x,y,angle):
        """
        """
        reading = []
        arm_left = self.make_sensor_arm(x,y)
        arm_middle = arm_left
        arm_right = arm_left
        reading.append()
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
        self.target_body = pymunk.Body(pymunk.inf,pymunk.inf)
        self.target_shape = pymunk.Circle(self.target_body,r)
        self.target_shape.elasticity = 1.0
        self.target_body.position = x,y
        self.target_body.angle = Vec2d(x,y).get_angle()
        self.target_shape.color = THECOLORS['blue']
        self.space.add(self.target_body,self.target_shape)
                    
    def frame_step(self,action):
        if action == 0:
            self.plane_body.angle -= .2
        elif action == 1:
            self.plane_body.angle += .2
        #else:
        #    self.plane_body.angle = Vec2d()
        #flying_direction = Vec2d(1,0).rotated(self.plane_body.angle)
        planet_position_vector = Vec2d(self.plane_body.position).normalized()
        target_pisition_vector = Vec2d(self.target_body.position).normalized()
        
        angle = target_pisition_vector.get_angle_between(target_pisition_vector)
        
        #flying_direction = Vec2d(1,0).rotated(self.target_body.angle)
        flying_direction = target_pisition_vector.rotated(angle)
        self.plane_body.angle = flying_direction.get_angle()
        print (self.plane_body.angle)
        self.plane_body.velocity = 100 * flying_direction
        
        screen.fill(THECOLORS["black"])
        draw(screen,self.space)
        self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()

if __name__ == "__main__":
    plane = Demo()
    plane.set_target(1900, 1060,50)
    while True:
        #plane.frame_step(random.randint(0,2))
        plane.frame_step(2)
        time.sleep(0.05)
