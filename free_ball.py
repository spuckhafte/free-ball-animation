# at high speeds and conditions, the game breaks

import pygame as py
import keyboard as key
from random import randint

# initialising pygame
py.init()

# setting up the pygame window
window = py.display.set_mode((1200, 600))
on = True

# clock - manages the time of the animation
clock = py.time.Clock()

# coordinates of ball
cx = 80
cy = 529

# positive 'y' coordinates are downwards and negative are upward and 'x' coordinates are normal (right '+' ; left '-')

# velocity in x direction _
vel_i = 13

# velocity in y direction |
vel_j = -25

# wind in x direction _
wind_i = -0.005

# wind in y direction |
wind_j = 0.005

# radius of ball
r = 10

# distance of camera from ball to watch the borders
focal = 20

# coefficient of restitution
e = 0.8

# strength of gravity
gravity = 1


# returns the rate of slowing the ball due to friction
def off_course():
    values = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11]
    random = randint(0, 6)
    return values[random]


# slows down the velocity of ball in certain directions
def slow_down(rate, veli=0, velj=0):
    if veli != 0:
        if veli > 0:
            veli -= rate
            return veli
        if veli < 0:
            veli += rate
            return veli
    if velj != 0:
        if velj > 0:
            velj -= rate
            return velj
        if velj < 0:
            velj += rate
            return velj


# infinite game loop
while on:
    try:
        # ticks the clock slower for the animation
        clock.tick(60)

        # change in velocity due to wind and gravity
        vel_i += wind_i
        vel_j += wind_j
        vel_j += gravity

        # change in y-velocity and gravity when the ball lands on floor at last
        if 0 < vel_j < 0.7 and 529.0 < cy < 529.9:
            vel_j = 0
            cy = 529
            gravity = 0
            wind_j = 0

        # all the changes occur if the ball is in motion
        if vel_i != 0 or vel_j != 0:
            
            # change in velocity of ball due to air resistance
            if vel_i == 0:
                vel_j = slow_down(0.01, velj=vel_j)
            elif vel_j == 0:
                vel_i = slow_down(0.01, veli=vel_i)
            else:
                vel_i = slow_down(0.005, veli=vel_i)
                vel_j = slow_down(0.005, velj=vel_j)

            # change in 'x' and 'y' coordinate of the ball
            cx += vel_i
            cy += vel_j

            # camera looking for the border to avoid crossing it
            pxl_up = window.get_at((int(cx), int(cy) - focal))[1]
            pxl_down = window.get_at((int(cx), int(cy) + focal))[1]
            pxl_right = window.get_at((int(cx) + focal, int(cy)))[1]
            pxl_left = window.get_at((int(cx) - focal, int(cy)))[1]

            # change in direction of velocity after colliding with the border
            if pxl_up == 255 or pxl_down == 255 or pxl_right == 255 or pxl_left == 255:

                # change in velocity due to friction
                if vel_i == 0:
                    vel_j = slow_down(off_course(), velj=vel_j)
                elif vel_j == 0:
                    vel_i = slow_down(off_course(), veli=vel_i)
                else:
                    vel_i = slow_down(off_course(), veli=vel_i)
                    vel_j = slow_down(off_course(), velj=vel_j)

                # all the logics down change the direction of velocity according after the ball collides
                if vel_i > 0 and vel_j < 0:
                    if pxl_up == 255:
                        vel_j = -e * vel_j
                    if pxl_right == 255:
                        vel_i = -e * vel_i

                if vel_i < 0 and vel_j < 0:
                    if pxl_up == 255:
                        vel_j = -e * vel_j
                    if pxl_left == 255:
                        vel_i = -e * vel_i

                if vel_i < 0 and vel_j > 0:
                    if pxl_down == 255:
                        vel_j = -e * vel_j
                    if pxl_left == 255:
                        vel_i = -e * vel_i

                if vel_i > 0 and vel_j > 0:
                    if pxl_down == 255:
                        vel_j = -vel_j
                    if pxl_right == 255:
                        vel_i = -vel_i

                if vel_i == 0:
                    vel_j = -vel_j

                if vel_j == 0:
                    vel_i = -vel_i

        # clears off the tail of the of the ball created when it moves
        window.fill((0, 0, 0))

        # creates different objects in the window
        py.draw.rect(window, (128, 255, 0), py.Rect(444, 253, 144, 53))
        py.draw.rect(window, (0, 255, 0), py.Rect(30, 50, 1100, 500), 20)
        pointer = py.draw.circle(window, (255, 0, 0), (cx, cy), r)
        py.display.update()

        # reload with default conditions
        if key.is_pressed('r'):
            cx = 80
            cy = 529
            vel_i = 13
            vel_j = -25
            continue

        # keeps the window responding
        for event in py.event.get():
            if event.type == py.QUIT:
                on = False
    except:
        # if the animation breaks, the conditions will be set to default
        cx = 80
        cy = 529
        vel_i = 13
        vel_j = -25
        continue
