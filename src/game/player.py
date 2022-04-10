import pygame
from field import Field

class Player:
    def __init__(self, pos: (int, int), size, speed=5, color=(255, 0, 0), deaths=0):
        # safe the start position and current
        self.initPos = pos
        self.currentPos = pos
        self.size = size
        self.color = color
        self.speed = speed
        self.deaths = deaths
        # have a collision box
        self.object = None

    # FIXME implemet in bound control
    # this method handles the human player movement
    def moveHuman(self, keys):
        if keys[pygame.K_LEFT] and self.x > 100 + self.width:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < 630:
            self.x += self.vel
        if keys[pygame.K_DOWN] and self.y < 420:
            self.y += self.vel
        if keys[pygame.K_UP] and self.y > 150 + self.height:
            self.y -= self.vel

    # this method handles the AI movement
    def moveAI(self, keys):
        pass

    def draw(self, screen):
        # use the drawn boarder as a collision boy
        self.object = pygame.draw.rect(screen, (0,0,0), (self.x-2, self.y-2, self.width+4, self.height+4), 2)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    # this method resets the player and increases death counter
    def reset(self):
        self.currentPos = self.initPos
        self.deaths += 1

    # this method checks if the new position of the player is in a wall if yes set player back in the field
    def forceInBounds(self, field: Field):
        #TODO implement method use check three corners of player to calculate witch wallit it and force back in boundary
        pass
