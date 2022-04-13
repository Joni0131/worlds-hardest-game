import pygame
import os
import sys
import importlib
import inspect
from player import Player
from enemy import Enemy
from field import Field
from time import sleep


# IDEA make a new class for the lvl choosing
class Game:

    def __init__(self, lvlName, humanPlayer=True ):
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
        # create empty variables for font and screen and players, and for all goal objects
        self.font = None
        self.screen = None
        self.players = []
        self.goals = []
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
        self.draw()
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
            # TODO make multiple players
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
            self.draw()
            # update all objects
            running = self.update()

    # this method draws the screen
    def draw(self):
        self.screen.fill((183, 175, 250))
        self.lvl.field.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
        pygame.display.update()

    # this method updates everything
    def update(self):
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
        if self.collision():
            return False
        return True

    # this method checks for collision with enemies and the goal
    def collision(self):
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
            self.draw()
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

    # TODO implement later
    def runningAI(self):
        pass

q = Game('lvlTest')
