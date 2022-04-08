import pygame
from worlds_hardest_game.src.game.field import Field
import stringFormat
from time import sleep


class Editor:

    def __init__(self, screenWidth=-1, screenHeight=-1, xOff=-1, yOff=-1, numberOfPlayableTilesWidth=20, numberOfPlayableTilesHeight=10, tileSize=50, enemyColor=(0, 0, 255)):
        # check that the field has a minimum of 2 tiles and the tile is at least 9*9 pixel
        if not (numberOfPlayableTilesWidth > 0 and numberOfPlayableTilesHeight > 0 and tileSize > 9 and numberOfPlayableTilesHeight * numberOfPlayableTilesWidth >= 2):
            raise Exception('Invalid field sizes.')
        # check if the screenWidth was set if not set to default
        if screenWidth == -1:
            self.screenWidth = (numberOfPlayableTilesWidth + 4) * tileSize
        # if it was set check it can hold all tiles and a border around it
        elif (numberOfPlayableTilesWidth + 2) * tileSize > screenWidth:
            print("The screen size is too small for the playing field. Was changed to valid size.")
            self.screenWidth = (numberOfPlayableTilesWidth + 4) * tileSize
        else:
            self.screenWidth = screenWidth
        # check if the screenWidth was set if not set to default
        if screenHeight == -1:
            self.screenHeight = (numberOfPlayableTilesHeight + 4) * tileSize
        # if it was set check it can hold all tiles and a border around it
        elif (numberOfPlayableTilesWidth + 2) * tileSize > screenHeight:
            print("The screen size is too small for the playing field. Was changed to valid size.")
            self.screenHeight = (numberOfPlayableTilesHeight + 4) * tileSize
        else:
            self.screenHeight = screenWidth
        # check it is a valid offset
        if yOff < 0:
            self.yOff = tileSize
        else:
            self.yOff = yOff
        # check if is a valid offset not set to tileSize
        if xOff < 0:
            self.xOff = tileSize
        else:
            self.xOff = xOff
        # save constant parameters
        self.enemyColor = enemyColor
        self.tileSize = tileSize
        # set number of created tiles
        self.numberOfTilesWidth = numberOfPlayableTilesWidth + 2
        self.numberOfTilesHeight = numberOfPlayableTilesHeight + 2
        # prepare empty variable for screen, font, modes, modeText, field
        self.screen = None
        self.font = None
        self.modes = []
        self.modeText = None
        self.field = None
        # start the editor
        self.startEditor()

    # this method handles the whole pygame instance and keeps track of all the process
    def startEditor(self):
        # init pygame
        pygame.init()
        # init the screen
        self.initScreen()
        # handle different action depending on mode add for loop
        # TODO
        sleep(60)
        # stop pygame
        pygame.quit()

    # IDEA first version increase performance by updating only portions maybe
    # this method draws everything
    def draw(self):
        # IDEA change color to same as out of bounds leave it like this to see difference
        # fill whole screen
        self.screen.fill((183, 175, 250))
        # add mode information to screen
        self.screen.blit(self.modeText, (5, 5))
        # draw field
        self.field.draw(self.screen)
        # update screen
        pygame.display.update()

    # this method handles the starting creation of the editor
    def initScreen(self):
        # start the screen
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        # IDEA maybe different font
        # set font
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        # initialize modes
        self.initModes()
        # init field
        self.field = Field(self.xOff, self.yOff, self.numberOfTilesWidth, self.numberOfTilesHeight, self.tileSize, self.enemyColor)
        # draw screen for the first time
        self.draw()

    # this method initializes all modes
    def initModes(self):
        self.setModes()
        self.createModeInformationSurface()

    # this method is creating the action information object
    def createModeInformationSurface(self):
        # create list for all surfaces
        listOfSurfaces = []
        # init commonly used signs
        openBracket = self.font.render('(', True, (0, 0, 0))
        closeBracket = self.font.render(')', True, (0, 0, 0))
        tripleSpace = self.font.render('   ', True, (0, 0, 0))
        # iterate over all modes and create needed surfaces
        for (info, key) in self.modes:
            # create surface for the information part
            informationSurface = self.font.render(f'{info} ', True, (0, 0, 0))
            # append all Surfaces in right order
            listOfSurfaces.append(informationSurface)
            # create key info surface by calling method
            listOfSurfaces.append(self.keyInfoPygame(key, openBracket, closeBracket))
            # append a space in the end as spacer
            listOfSurfaces.append(tripleSpace)
        # drop last space
        listOfSurfaces.pop()
        # combine all surfaces on one
        self.modeText = self.combineSurface(listOfSurfaces)

    # CLEAN legacy method can be removed also remove stringFormat if not necessary any more
    # method to get a string of a key for the info example key s in pygame is pygame.K_s and this should convert to (S͟)
    def keyInfoCommandPrompt(self, key: int):
        string = f"({stringFormat.escapeSequence['UNDERLINE']}{chr(key).upper()}{stringFormat.escapeSequence['END']})"
        return string

    # method returns a rendered object where the text has been underlined
    # because pygame doesn't support escape chars this is a workaround
    # to not unnecessary create the same object multiple times pass it to the method
    def keyInfoPygame(self, key: int, openBracket, closeBracket):
        # use same font but set underline
        self.font.set_underline(True)
        under = self.font.render(chr(key).upper(), True, (0, 0, 0))
        # revert font back
        self.font.set_underline(False)
        # combine all three objects in one and set background as transparent
        actionKey = self.combineSurface([openBracket, under, closeBracket])
        return actionKey

    # this method combines multiple surfaces in one
    def combineSurface(self, listOfSurface):
        # init width
        width = 0
        # the height is always the same
        height = listOfSurface[0].get_height()
        # calculate total length
        for x in listOfSurface:
            width += x.get_width()
        # init new Surface with transparent background
        combined = pygame.Surface((width, height), pygame.SRCALPHA)
        # reset width as new pos to blit at
        width = 0
        # iterate over all Surfaces and blint them
        for x in listOfSurface:
            combined.blit(x, (width, 0))
            # increment width
            width += x.get_width()
        # return combined object
        return combined

    # this method setsSupported Actions and the corresponding keys
    def setModes(self):
        # append save
        self.modes.append(('Save', pygame.K_s))
        # append change tile outOfBounds / playable
        self.modes.append(('ChangeTile', pygame.K_c))
        # append setStart
        self.modes.append(('StartTile', pygame.K_a))
        # append setGoal
        self.modes.append(('GoalTile', pygame.K_g))
        # append setEnemyStart
        self.modes.append(('NewEnemy', pygame.K_e))
        # append setLastEnemyAim
        self.modes.append(('EnemyMovement', pygame.K_m))
        # append detectEdges
        self.modes.append(('CreateEdges', pygame.K_w))

    # TODO all this
    # plan for editor:
    # first init a field of playable tiles width = 20 height = 10
    # that means in reality there are 22*12 tiles
    # set the others as out of bounds
    # set certain keys for actions:
        # remove tile from playing field on click
        # set start
        # set goal
        # set start enemyPos all enemies are always starting and stopping in the middle of a tile
        # set enemyAim points add transparent enemy draw, so it can be seen
        # detect edges and add to corresponding tile
            # draw edges afterwards
        # save level
            # ask for initial level name
    # close editor


e = Editor()
