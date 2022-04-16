import numpy as np
from worlds_hardest_game.src.geneticAlgorithm.creature import Creature
from worlds_hardest_game.src.game.player import Player


class Population:

    # this class initializes and handles the whole population
    def __init__(self, populationSize, defaultPlayer, mutationRate, moveIncreasePerFiveRounds, field, maxGenerations):
        self.populationSize = populationSize
        self.defaultPlayer = defaultPlayer
        self.mutationRate = mutationRate
        self.moveIncrease = moveIncreasePerFiveRounds
        self.field = field
        self.maxGeneration = maxGenerations
        # prepare variables
        self.creatures = []
        self.goalCentroid = []
        self.currentGeneration = 0
        # init the first gen
        self.initGeneration()

    # this method init the first generation
    def initGeneration(self):
        # first calculate the centroid
        self.calcCentroid()
        # create enough new creatures
        for i in range(0, self.populationSize):
            # create a player for the creature from the default player
            player = Player([self.defaultPlayer.initPos[0],self.defaultPlayer.initPos[1]], self.defaultPlayer.size, self.defaultPlayer.speed, self.defaultPlayer.color)
            # create creature
            creature = Creature(self.goalCentroid[0], self.goalCentroid[1], self.moveIncrease, self.defaultPlayer.speed,
                                self.mutationRate, [], player)
            # safe the creature
            self.creatures.append(creature)

    # this method draws the whole population
    def draw(self, screen):
        # draw every creature
        for creature in self.creatures:
            creature.draw(screen)

    # this method creates a new generation
    def newGeneration(self):
        # create a list of parents because 2 parents make 2 childs it is enough to iterate over half the length
        parentList = []
        # search for the best creature and safe it
        best = None
        for creature in self.creatures:
            if best is None or best.fitness < creature.fitness:
                best = creature
        # reset best creature
        best.currentMove = 0
        best.player.reset()
        best.player.deaths = 0
        # create enough parent pairs
        for i in range(0, self.populationSize//2,1):
            # choose 2 more or less random parents
            inter = [self.selection(), self.selection()]
            parentList.append(inter)
        # create a new list of creatures
        nextGen = []
        # iterate over all parents and generate 2 children with cross over
        for p1, p2 in parentList:
            newMovementSet = self.reproduce(self.creatures[p1], self.creatures[p2])
            # iterate over both movements
            for movement in newMovementSet:
                # check that population is not too big
                if len(nextGen) < self.populationSize:
                    # create the player that is moved
                    player = Player([self.defaultPlayer.initPos[0],self.defaultPlayer.initPos[1]], self.defaultPlayer.size, self.defaultPlayer.speed, self.defaultPlayer.color)
                    # init the new creature
                    nextGen.append(Creature(self.goalCentroid[0], self.goalCentroid[1],
                                            self.moveIncrease * ((self.currentGeneration // 5) + 1), self.defaultPlayer.speed,
                                            self.mutationRate, movement, player))
        # to not lose the best from last gen copy it to the new gen
        nextGen.append(best)
        # delete the old gen
        self.creatures = nextGen
        # increase generation count
        self.currentGeneration += 1

    # TODO make crossover point number variable not static at half
    # this method generates a baby from two parents by doing cross over
    def reproduce(self, parent1, parent2):
        movements = [[],[]]
        for move in parent1.movements:
            movements[0].append(move)
        for move in parent2.movements:
            movements[1].append(move)
        # swap half the movements
        movements[0][:len(movements[0])//2], movements[1][:len(movements[0])//2] = movements[1][:len(movements[0])//2], movements[0][:len(movements[0])//2]
        return movements

    # this method moves every creature return False once all creatures finished moving
    def move(self, screen):
        # parameter to keep track of all results
        param = False
        # iterate over all creatures
        for creature in self.creatures:
            param = creature.move(screen, self.field) or param
        # return the param
        return param

    # this method implements a tournament based selection algorithm
    # returns the index of a selected creature
    def selection(self, numberOfCompares=3):
        # select starting creature randomly
        startIdx = np.random.randint(0, len(self.creatures), 1)[0]
        # compare the fitness score of the creature to multiple creatures
        for idx in np.random.randint(0,  len(self.creatures), numberOfCompares):
            # take the better creature
            if self.creatures[idx].fitness > self.creatures[startIdx].fitness:
                startIdx = idx
        return startIdx

    # this method calculates the centroid of the goal
    def calcCentroid(self):
        # create list of all relevant pixel coordinates
        pixels = []
        # iterate over all tiles in the field and generate the pixel coordinates
        for tiles in self.field.field:
            for tile in tiles:
                if tile.goal:
                    # if the tile is a goal append all 4 corner pixel
                    pixels.append([tile.pixelPos[0], tile.pixelPos[1]])
                    pixels.append([tile.pixelPos[0] + tile.size, tile.pixelPos[1]])
                    pixels.append([tile.pixelPos[0], tile.pixelPos[1] + tile.size])
                    pixels.append([tile.pixelPos[0] + tile.size, tile.pixelPos[1] + tile.size])
        # sum all x coordinates and y coordinates
        coords = np.sum(pixels, 0)
        # divide the coords by the number of pixel points and round to int
        self.goalCentroid = list(coords // len(pixels))

    # this method calculates all fitness values
    def calcFitness(self):
        # iterate over each creature
        for creature in self.creatures:
            creature.calcFitness()
