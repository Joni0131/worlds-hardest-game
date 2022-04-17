import pygame
from worlds_hardest_game.src.game.field import Field
import numpy as np


class Player:
    def __init__(self, pos: [int, int], size, speed=5, color=(255, 0, 0), deaths=0):
        # safe the start position and current
        self.initPos = [pos[0], pos[1]]
        self.currentPos = pos
        self.size = size
        self.color = color
        self.speed = speed
        self.deaths = deaths
        # have a collision box
        self.object = None
        self.goal = False

    # this method handles the human player movement
    def moveHuman(self, keys, screen, field):
        if self.goal:
            return
        if keys[pygame.K_LEFT]:
            self.currentPos[0] -= self.speed
        if keys[pygame.K_RIGHT]:
            self.currentPos[0] += self.speed
        if keys[pygame.K_DOWN]:
            self.currentPos[1] += self.speed
        if keys[pygame.K_UP]:
            self.currentPos[1] -= self.speed
        # draw the interims' player for in bound forcing
        self.draw(screen)
        # check if valid movement
        self.forceInBounds(field)
        self.draw(screen)

    # this method handles the AI movement
    def moveAI(self, keys, screen, field):
        # calculate new xcoordinate
        self.currentPos[0] += keys[0]
        # calcualte new y coordinate
        self.currentPos[1] += keys[1]
        # draw the interims' player for in bound forcing
        self.draw(screen)
        # check if valid movement
        self.forceInBounds(field)
        self.draw(screen)

    def draw(self, screen):
        # use the drawn boarder as a collision boy
        self.object = pygame.Rect(self.currentPos[0], self.currentPos[1], self.size, self.size)
        pygame.draw.rect(screen, (0, 0, 0), self.object, 2)
        pygame.draw.rect(screen, self.color, (self.currentPos[0] + 2, self.currentPos[1] + 2, self.size - 4, self.size - 4))

    # this method resets the player and increases death counter
    def reset(self):
        self.currentPos = [self.initPos[0], self.initPos[1]]
        self.deaths += 1

    # this method checks if the new position of the player is in a wall if yes set player back in the field
    # corner names northWest, northEast, southWest, southEast
    # NW     NE
    #   *---*
    #   |   |
    #   *---*
    # SW     SE
    def forceInBounds(self, field: Field):
        # calculate the center of the player and the corresponding tile indices
        centerPixel = np.add(self.currentPos, self.size // 2)
        (centerMatrixX, centerMatrixY) = np.subtract(centerPixel, (field.x, field.y)) // field.tileSize
        # check all surrounding tiles by iterating over them the middle tile doesn't have to be checked because
        # it will be impossible to have a collision with a wall
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0 or not field.field[centerMatrixX + i][centerMatrixY + j].wall:
                    continue
                checkingTile = field.field[centerMatrixX + i][centerMatrixY + j].object
                # check tile for collision:
                if self.object.colliderect(checkingTile):
                    # check collision on the bottom side
                    if abs(checkingTile.top - self.object.bottom) <= self.speed:
                        # if player is out of bound reset it to boarder position
                        if checkingTile.top - self.object.bottom <= 0:
                            self.currentPos[1] += checkingTile.top - self.object.bottom
                    # check collision on the top side
                    if abs(checkingTile.bottom - self.object.top) <= self.speed:
                        # if player is out of bound reset it to boarder position
                        if checkingTile.bottom - self.object.top >= 0:
                            self.currentPos[1] += checkingTile.bottom - self.object.top
                    # check collision on the left side
                    if abs(checkingTile.right - self.object.left) <= self.speed:
                        # if player is out of bound reset it to boarder position
                        if checkingTile.right - self.object.left >= 0:
                            self.currentPos[0] += checkingTile.right - self.object.left
                    # check collision on the bottom side
                    if abs(checkingTile.left - self.object.right) <= self.speed:
                        # if player is out of bound reset it to boarder position
                        if checkingTile.left - self.object.right <= 0:
                            self.currentPos[0] += checkingTile.left - self.object.right
