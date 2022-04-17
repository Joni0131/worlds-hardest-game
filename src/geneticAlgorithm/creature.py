import random
import numpy as np
from scipy.optimize import minimize
import scipy.spatial.distance
import math


# this class handels one creature
class Creature:
    # initilize the creature
    def __init__(self, goalX, goalY, field, maxMoveNumber, maxSpeed, mutationRate, initMovement, player):
        self.goalCoords = [goalX, goalY]
        self.field = field
        self.maxSpeed = maxSpeed
        self.mutationRate = mutationRate
        self.maxMoveNumber = maxMoveNumber
        self.movements = initMovement
        self.player = player
        # initiate next move
        self.currentMove = 0
        # init fitness parameters
        self.fitness = 0
        self.calculateAllMovements()
        self.center = []

    # calculate all movements
    def calculateAllMovements(self):
        # check the previous movements
        currentLength = len(self.movements)
        i = 0
        # and mutate every new movement imput
        while i < currentLength:
            self.mutate(i)
            i += 1
        # if the player is allowed to execute more movements generate new ones randomly and append them
        while currentLength < self.maxMoveNumber:
            self.randomMove(currentLength)
            currentLength += 1

    # this methode handles the mutation
    def mutate(self, idx):
        # generate random number between 0 and 1
        ran = random.random()
        # if the random number is smaller than the mutation rate then generate random movement
        if ran <= self.mutationRate:
            self.randomMove(idx)

    # this method generates a new move
    def randomMove(self, idx):
        # variable for init movement
        start = None
        # check if at index a movement exists
        if idx < len(self.movements):
            start = self.movements[idx]
        # generate movement movemnts that does not match the previous
        inter = [random.randrange(-self.maxSpeed, self.maxSpeed + 1, 1), random.randrange(-self.maxSpeed, self.maxSpeed + 1, 1)]
        while start is not None and inter[0] == start[0] and inter[1] == start[1]:
            inter = [random.randrange(-self.maxSpeed, self.maxSpeed + 1, 1), random.randrange(-self.maxSpeed, self.maxSpeed + 1, 1)]
        # safe the new movement
        # if it is completly new append it else exchange it
        if start is None:
            self.movements.append(inter)
            return
        self.movements[idx] = inter

    # this method handels the movement return false if no movement happend
    def move(self, screen, field):
        # check if it exceeds the maxMovements
        if self.currentMove >= self.maxMoveNumber:
            return False
        # if the player already died no more movements
        if self.player.deaths != 0:
            return False
        # send the next move to the player
        self.player.moveAI(self.movements[self.currentMove], screen, field)
        self.currentMove += 1
        return True

    # TODO change distance calculation to distance to region or something
    # this method calculates the fitness of a creature
    # the function is a derivation of code bullets fitness function
    # https://github.com/Code-Bullet/WorldsHardestGameAI/blob/gh-pages/WHG/Player.js
    def calcFitness(self):
        # if the player reached the goal
        if self.player.goal:
            self.fitness = 1.0/16.0 + 10000.0/((self.currentMove-1) ** 2)
        else:
            # calculate the center of the player
            self.center = np.add(self.player.currentPos, self.player.size // 2)
            # calculate the distance by minimizing the function calc distance with the initial guess as the goal centroid
            parameter = minimize(self.calcDistance, self.goalCoords, method='Nelder-Mead')
            # use the parameter to calculate the distance
            distance = self.calcDistance(list(parameter.x))
            # if the player died of course the fitness has to be worse then if it survieved
            if self.player.deaths != 0:
                distance += 0.9
            self.fitness = 1 / (distance ** 2)
        # square the fitness so small changes are seen bigger
        self.fitness *= self.fitness

    # this method is just a interface to the underlying draw method
    def draw(self, screen):
        if self.player.deaths != 0:
            return
        self.player.draw(screen)

    # this method defines the distance calculation
    def calcDistance(self, coordinats):
        x = coordinats[0]
        y = coordinats[1]
        # check if x, y are in the region of the goals by calculating the tile and checking if it is a goal
        xIdx = (x - self.field.x) // self.field.tileSize
        yIdx = (y - self.field.y) // self.field.tileSize
        # check if tile is NOT a goal then the position is invalid
        if not self.field.field[int(xIdx)][int(yIdx)].goal:
            return math.inf
        # calculate the eucleadian distance if valid
        return scipy.spatial.distance.euclidean([x, y], self.center)
