import pygame
import numpy as np


class Enemy:
    def __init__(self, x, y, radius, speed, color):
        self.pos = (x, y)  # position as tuple
        self.radius = radius  # radius of the enemy
        self.speed = speed  # speed in pixel
        self.color = color  # main color
        self.aimPoints = [self.pos]  # list of aims as [(x1, y1), (x2, y2)] ...
        # the initial position is ofcourse a aim as well
        self.velocitiesToPoint = [(0, 0)]  # list of speed vectors as [(velx1, vely1), (velx2, vely2)] ...
        # the initial velocity is (0, 0) because it doesn't move
        self.toleranceWindow = speed // 2  # this is the tolerance for reaching the aim

    # draw the enemy at the current position
    def draw(self, screen):
        # first draw the line around the enemy in black
        pygame.draw.circle(screen, 0, self.pos, self.radius, 3)
        # second fill the inner with the enemy color
        pygame.draw.circle(screen, self.color, self.pos, self.radius - 3)

    # this function adds a new Point to where the object is moving in order
    # calculate the needed velocities so calculation is done before runtime
    def addMovementPoint(self, x, y):
        # just append the next position
        self.aimPoints.append((x, y))
        # first velocity depends on last aim
        # calculate the velocity by subtracting the last aim from the next one
        # get the needed directions and then set the speed
        velocity = tuple(np.sign(np.subtract((x, y), self.aimPoints[-2])) * self.speed)
        # update last velocity
        self.velocitiesToPoint[-1] = velocity
        # calculate returning velocity the same way sign of aim - current
        velocity = tuple(np.sign(np.subtract(self.aimPoints[0], (x, y))) * self.speed)
        # append returning velocity
        self.velocitiesToPoint.append(velocity)

    # this function adds multiple Points at once
    # calculate the needed velocities so calculation is done before runtime
    def addMovementPoints(self, pos):
        # the calculation is the same as in addMovementPoint
        # append the first point and overwrite the existing velocity
        self.aimPoints.append(pos[0])
        velocity = tuple(np.sign(np.subtract(pos[0], self.aimPoints[-2])) * self.speed)
        # update last velocity
        self.velocitiesToPoint[-1] = velocity
        # by just appending the second to last velocity we do not calculate the velocity unnessaserily offten
        for point in pos[1::]:
            self.aimPoints.append(point)
            velocity = tuple(np.sign(np.subtract(point, self.aimPoints[-2])) * self.speed)
            self.velocitiesToPoint.append(velocity)
        # but now we are still missing the last velocity
        velocity = tuple(np.sign(np.subtract(self.aimPoints[0], pos[-1])) * self.speed)
        # append returning velocity
        self.velocitiesToPoint.append(velocity)

    # create a move function that calculates the next position depending on the next aim and the velocity
    def move(self):
        # if there is no aimPoint it means the enemy is standing still so no update is happening
        if len(self.aimPoints) == 1:
            return
        # if the enemy reached the aim position switch the aim positions and update the next velocity
        if self.pos == self.aimPoints[0]:
            self.aimPoints.append(self.aimPoints.pop(self.aimPoints.index(0)))
            self.velocitiesToPoint.append(self.velocitiesToPoint.pop(self.velocitiesToPoint.index(0)))
            # by returning we make sure it stops shortly at the aim
            return
        # now we calculate the next position by simply adding the velocity vector on top
        newPos = np.add(self.pos, self.velocitiesToPoint[0])
        # calculate the difference to the aim if it is smaller than speed/2 we are the closet possible to the aim
        # so we set the new position to the aim
        (diffX, diffY) = tuple(np.subtract(self.aimPoints[0], newPos))
        if self.toleranceWindow * -1 < diffX <= self.toleranceWindow or self.toleranceWindow * -1 < diffY <= self.toleranceWindow:
            self.pos = self.aimPoints[0]
        else:
            self.pos = tuple(newPos)
