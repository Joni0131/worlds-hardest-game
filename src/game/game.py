import pygame
import os
import sys
import importlib
import inspect
from player import Player
from worlds_hardest_game.src.geneticAlgorithm.population import Population
from enemy import Enemy
from field import Field
from time import sleep


# IDEA make a new class for the lvl choosing
class Game:

    def __init__(self, lvlName, humanPlayer=True):
        # verify types
        if not isinstance(lvlName, str):
            raise TypeError('Expected str; got %s' % type(lvlName).__name__)
        # check if it is a valid lvlName
        if not self.validFileName(lvlName):
            raise Exception('The level name %s is not valid.' % type(lvlName).__name__)
        # check if lvl exists
        self.lvlPath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ("lvl/" + lvlName + ".py"))
        # if the file doesn't exist raise exception
        if not os.path.exists(self.lvlPath):
            raise Exception('The lvl %s doesn\'t exist.' % lvlName)
        # if the lvl exists safe lvl name
        self.lvlName = lvlName
        # set relative module name valid to do only in the project
        self.modulePath = 'worlds_hardest_game.lvl'
        # import the lvl file
        self.importLvl = importlib.import_module('.'+self.lvlName, self.modulePath)
        # build the lvl class name and functionality
        self.lvlClassName = self.lvlName[0].upper() + self.lvlName[1::]
        # create the right class object so it can be used
        self.lvlClass = getattr(self.importLvl, self.lvlClassName)
        # create lvl instance
        self.lvl = self.lvlClass()
        # check if human player
        self.humanPlayer = humanPlayer
        # set default parameters for a population
        self.populationSize = 100
        self.mutationRate = 0.01
        self.moveIncreasePerFiveRounds = 30
        self.maxGenerations = 500
        # create empty variables for font and screen and players, and for all goal objects
        self.font = None
        self.screen = None
        self.players = []
        self.goals = []
        self.population = None
        self.stop = False
        # start the game screen
        self.initGame()

    @staticmethod
    def validFileName(name):
        # list off illegal characters as well as - and .
        illegalChars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/', ' ', '$', '!',
                        '\'', '\"', ':', '@', '+', '`', '|', '=', '-', '.']
        # iterate over all illegal chas and check if any is part of the name
        for char in illegalChars:
            if char in name:
                print(f"The character {char} is not allowed to be part of the fileName")
                return False
        # check that the file name starts with a lower case character
        if not name[0].islower():
            print("The first character has to be lower case")
            return False
        return True

    # this method initiate the game
    def initGame(self):
        # start pygame
        pygame.init()
        # IDEA later add Deathcounter below has to increase the size
        # start the screen
        self.screen = pygame.display.set_mode((self.lvl.windowWidth, self.lvl.windowHeight))
        # set font
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        # draw first time
        self.drawHuman()
        # safe all goal tiles
        for colum in self.lvl.field.field:
            for tile in colum:
                if tile.goal:
                    self.goals.append(tile.object)
        # initiate player and difference for human and genetic
        if self.humanPlayer:
            self.players.append(Player(list(self.lvl.playerStartingPos), self.lvl.playerSize))
            self.runningHuman()
        else:
            # create a default player
            self.players.append(Player(list(self.lvl.playerStartingPos), self.lvl.playerSize))
            self.population = Population(self.populationSize, self.players[0], self.mutationRate, self.moveIncreasePerFiveRounds, self.lvl.field, self.maxGenerations)
            self.runningAI()
        # stop pygame
        pygame.quit()

    # this methods handles all the game interactions
    def runningHuman(self):
        # set roughly the speed for the game in frames per second
        fps = 30
        # calculate how long to wait by dividing 1000 ms / fps because function needs int round it
        delay = int(1000 / fps)
        running = True
        # keep the editor running until the save mode has been accessed
        while running:
            # add a pygame delay so the game is not always updating
            pygame.time.delay(delay)
            # draw everything
            self.drawHuman()
            # update all objects
            running = self.updateHuman()

    # this method draws the screen
    def drawHuman(self):
        self.screen.fill((183, 175, 250))
        self.lvl.field.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        pygame.display.update()

    # this method updates everything
    def updateHuman(self):
        self.lvl.field.move()
        events = pygame.event.get()
        for event in events:
            # detect if window has been closed
            if event.type == pygame.QUIT:
                return False
        # get all down pressed keys
        keys = pygame.key.get_pressed()
        # update the player
        self.players[0].moveHuman(keys, self.screen, self.lvl.field)
        # check for collision
        if self.collisionHuman():
            return False
        return True

    # this method checks for collision with enemies and the goal
    def collisionHuman(self):
        collision = [False] * len(self.players)
        # list enemy objects
        enemies = list(map(lambda x: x.object, self.lvl.field.enemy))
        # check if collision with enemy
        for idx, player in enumerate(self.players):
            if player.object.collidelist(enemies) != -1:
                print("You died.")
                player.reset()
                collision[idx] = True
        # if all players collided reset lvl
        if all(collision):
            self.lvl = self.lvlClass()
            self.goals = []
            self.drawHuman()
            # safe all goal tiles just in cas
            for colum in self.lvl.field.field:
                for tile in colum:
                    if tile.goal:
                        self.goals.append(tile.object)
            return False
        # check if any player reached the goal
        for idx, player in enumerate(self.players):
            if player.object.collidelist(self.goals) != -1:
                print("Reached goal")
                print(f'Player died {player.deaths} times.')
                player.goal = True
                collision[idx] = True
                return True

    def runningAI(self):
        # set roughly the speed for the game in frames per second
        fps = 30
        # calculate how long to wait by dividing 1000 ms / fps because function needs int round it
        delay = int(1000 / fps)
        running = True
        # keep the editor running until the save mode has been accessed
        while running:
            # add a pygame delay so the game is not always updating
            pygame.time.delay(delay)
            # draw everything
            self.drawAI()
            # update all objects
            running = self.updateAI()
        # the generation finished
        self.population.calcFitness()
        # check if the maximum gernerations have been reached
        if not self.stop and self.population.currentGeneration < self.population.maxGeneration:
            # finished n-th population
            print(f'Finished {self.population.currentGeneration}-th generation.')
            # reset the field
            self.lvl = self.lvlClass()
            self.goals = []
            self.drawAI()
            # safe all goal tiles just in cas
            for colum in self.lvl.field.field:
                for tile in colum:
                    if tile.goal:
                        self.goals.append(tile.object)
            # gernerat next Gen
            self.population.newGeneration()
            # rerun running
            return self.runningAI()
        if self.stop:
            print("User stopped the program.")
        else:
            print("Reached Population limit")

    # this method draws everything for the ai
    def drawAI(self):
        self.screen.fill((183, 175, 250))
        self.lvl.field.draw(self.screen)
        self.population.draw(self.screen)
        pygame.display.update()
        return

    # this method updates everything
    def updateAI(self):
        self.lvl.field.move()
        events = pygame.event.get()
        for event in events:
            # detect if window has been closed
            if event.type == pygame.QUIT:
                self.stop = True
                return False
        # move all creatures
        result = self.population.move(self.screen)
        # check for collisions
        self.collisionAI()
        # return result
        return result

    # this method calculates the colsision for the ai
    def collisionAI(self):
        # list enemy objects
        enemies = list(map(lambda x: x.object, self.lvl.field.enemy))
        # check if collision with enemy
        for idx, player in enumerate(self.population.creatures):
            if player.player.object.collidelist(enemies) != -1:
                print("You died.")
                player.player.reset()
        # check if any player reached the goal
        for idx, player in enumerate(self.population.creatures):
            if player.player.object.collidelist(self.goals) != -1:
                print("Reached goal")
                print(f'Player died {player.player.deaths} times.')
                player.player.goal = True

q = Game('lvlTest', humanPlayer=False)
