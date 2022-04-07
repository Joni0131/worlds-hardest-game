import pygame as pg


# this file is heavily inspired by this file https://github.com/Code-Bullet/WorldsHardestGameAI/blob/gh-pages/WHG/Tile.js
class Tile:
    def __init__(self, x, y, size, start_x, start_y):
        self.matPos = (x, y)
        self.pixelPos = (x * size + start_x, y * size + start_y)
        self.size = size
        self.safe = False
        self.goal = False
        self.outOfBounds = False
        self.edges = [0, 0, 0, 0]  # Defined as Flags as [N, E, S, W]
        self.wall = False

    def draw(self, screen):
        # IDEA optimize with return and order
        # iterate over all tiles so the color is alternating
        if sum(self.matPos) % 2 == 0:
            pg.draw.rect(screen, (247, 247, 255), (self.pixelPos[0], self.pixelPos[1], self.size, self.size))
        else:
            pg.draw.rect(screen, (230, 230, 255), (self.pixelPos[0], self.pixelPos[1], self.size, self.size))
        # set color for safe areas
        if self.safe or self.goal:
            pg.draw.rect(screen, (181, 254, 180), (self.pixelPos[0], self.pixelPos[1], self.size, self.size))
        # set color for out of bounds
        if self.outOfBounds:
            pg.draw.rect(screen, (180, 181, 254), (self.pixelPos[0], self.pixelPos[1], self.size, self.size))

    def drawEdges(self, screen):
        # draw the given edges
        color = 0  # color is black
        width = 1  # width is 1 pixel
        # draw north edge
        if self.edges[0]:
            self.wall = True
            pg.draw.line(screen, color, self.pixelPos, (self.pixelPos[0] + self.size, self.pixelPos[1]), width)
        # draw east edge:
        if self.edges[1]:
            self.wall = True
            pg.draw.line(screen, color, (self.pixelPos[0] + self.size, self.pixelPos[1]), (self.pixelPos[0] + self.size, self.pixelPos[1] + self.size), width)
        # draw south edge:
        if self.edges[2]:
            self.wall = True
            pg.draw.line(screen, color, (self.pixelPos[0], self.pixelPos[1] + self.size), (self.pixelPos[0] + self.size, self.pixelPos[1] + self.size), width)
        # draw west edge:
        if self.edges[3]:
            self.wall = True
            pg.draw.line(screen, color, self.pixelPos[0], (self.pixelPos[0], self.pixelPos[1] + self.size), width)
