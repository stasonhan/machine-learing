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
        self.num_steps = 0
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
        
        self.obstacles = []
        self.obstacles.append(self.create_obstacle(400, 350, 100))
        self.obstacles.append(self.create_obstacle(1000, 562, 125))
        self.obstacles.append(self.create_obstacle(600, 600, 35))        
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
        self.target_shape.color = THECOLORS['green']
        self.space.add(self.target_body,self.target_shape)
        
    def create_obstacle(self, x, y, r):
        c_body = pymunk.Body(pymunk.inf, pymunk.inf)
        c_shape = pymunk.Circle(c_body, r)
        c_shape.elasticity = 1.0
        c_body.position = x, y
        c_shape.color = THECOLORS["blue"]
        self.space.add(c_body, c_shape)
        return c_body
    
    def move_obstacles(self):
        # Randomly move obstacles around.
        for obstacle in self.obstacles:
            speed = random.randint(1, 5)
            direction = Vec2d(1, 0).rotated(self.plane_body.angle + random.randint(-2, 2))
            obstacle.velocity = speed * direction
                        
    def frame_step(self,action):
        self.num_steps += 1
        if action == 0:
            self.plane_body.angle -= .2
        elif action == 1:
            self.plane_body.angle += .2
        else:
        #    self.plane_body.angle = Vec2d()
        #flying_direction = Vec2d(1,0).rotated(self.plane_body.angle)
            plane_position_vector = Vec2d(self.plane_body.position)
            target_pisition_vector = Vec2d(self.target_body.position)
            #angle = planet_position_vector.get_angle_between(target_pisition_vector)
            angle = (target_pisition_vector - plane_position_vector).normalized().get_angle()
            
            self.plane_body.angle =  angle
            
        #flying_direction = Vec2d(1,0).rotated(self.target_body.angle)
        #flying_direction = target_pisition_vector.rotated(angle)
        flying_direction = Vec2d(1,0).rotated(self.plane_body.angle)
        self.plane_body.angle = flying_direction.get_angle()
        
        self.plane_body.velocity = 100 * flying_direction
        
        screen.fill(THECOLORS["black"])
        draw(screen,self.space)
        self.space.step(1./10)
        if draw_screen:
            pygame.display.flip()
        clock.tick()
        x,y = self.plane_body.position
        readings,readings_position = self.get_sonar_readings(x,y,self.plane_body.angle)
        #print (readings,readings_position)
        #if 1 in readings:
        #    print("reached the target!")
        if self.num_steps % 100 == 0:
            print (self.num_steps)
            self.move_obstacles() 
        
    def get_sonar_readings(self,x,y,angle):
        readings = []
        readings_position = []
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        # Rotate them and get readings.
        #readings is the sonar number
        #readings_position is the sonar position
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.75)[0])
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0)[0])
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.75)[0])
        
        readings_position.append(self.get_arm_distance(arm_left, x, y, angle, 0.75)[1])
        readings_position.append(self.get_arm_distance(arm_middle, x, y, angle, 0)[1])
        readings_position.append(self.get_arm_distance(arm_right, x, y, angle, -0.75)[1])
        
        if show_sensors:
            pygame.display.update()

        return readings,readings_position
    
    def make_sonar_arm(self, x, y):
        spread = 10  # Default spread.
        distance = 10  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))
        
        return arm_points
    
    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0
        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1
            #import pdb;pdb.set_trace()
            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= WIDTH or rotated_p[1] >= HEIGHT:
                return i,rotated_p  # Sensor is off the screen.
            else:
                obs = screen.get_at(rotated_p)
                if self.get_track_or_not(obs) == 1:
                    import pdb;pdb.set_trace()
                    print (i,rotated_p)
                    return i,rotated_p
                    
                elif self.get_track_or_not(obs) == -1:
                    #import pdb;pdb.set_trace()
                    return i,rotated_p

            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return i,rotated_p
    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
            (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
            (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = HEIGHT - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading):
        if reading == THECOLORS['black']:
            return 0
        elif reading == THECOLORS['green']:
            return -1
        elif reading == THECOLORS['blue']:
            return 1
        
if __name__ == "__main__":
    plane = Demo()
    plane.set_target(1900, 1060,50)
    i = 0
    while True:
        i += 1
        if i <= 100:
            plane.frame_step(random.randint(0,1))
        else:plane.frame_step(2)
        time.sleep(0.05)
