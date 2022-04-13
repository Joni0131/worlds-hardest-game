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
        # create enough parent pairs
        for i in range(0, self.populationSize//2,1):
            # choose 2 more or less random parents
            inter = [self.selection(), self.selection()]
            parentList.append(inter)
        # create a new list of creatures
        nextGen = []
        # iterate over all parents and generate 2 children with cross over
        for p1, p2 in parentList:
            newMovmentSet = self.reproduce(p1, p2)
            # iterate over both movments
            for movment in newMovmentSet:
                # check that population is not too big
                if len(nextGen) < self.populationSize:
                    # create the player that is moved
                    player = Player(self.defaultPlayer.initPos, self.defaultPlayer.size, self.defaultPlayer.speed, self.defaultPlayer.color)
                    # init the new creature
                    nextGen.append(Creature(self.goalCentroid[0],self.goalCentroid[1],
                                            self.moveIncrease * (self.currentGeneration // 5), self.defaultPlayer.speed,
                                            self.mutationRate, movment, player))
        # to not loose the best from last gen copy it to the new gen
        nextGen.append(best)
        # delete the old gen
        self.creatures = nextGen

    # this method generates a baby from two parents
    def reproduce(self, parent1, parent2):
        pass

    # this method moves every creature return False once all creatures finished moving
    def move(self, screen):
        # parameter to keep track of all results
        param = False
        # iterate over all creatures
        for creature in self.creatures:
            param = param or creature.move(screen, self.field)
        # return the param
        return param

    # this method implements a tournament based selection algorithm
    # returns the index of a selected creature
    def selection(self, numberOfCompares=3):
        # select starting creature randomly
        startIdx = np.random.randint(0, len(self.creatures), 1)
        # compare the fitness score of the creature to multiple creatures
        for idx in np.random.randint(0,  len(self.creatures), numberOfCompares):
            # take the better creature
            if self.creatures[idx].fitness > self.creatures[startIdx].fitness:
                startIdx = idx
        return startIdx
