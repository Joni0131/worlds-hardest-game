import pygame
from worlds_hardest_game.src.game.field import Field
from worlds_hardest_game.src.game.enemy import Enemy
from worlds_hardest_game.src.lvlEditor.writer import Writer
import numpy as np
import stringFormat
from time import sleep


class Editor:

    def __init__(self, screenWidth=-1, screenHeight=-1, xOff=-1, yOff=-1, numberOfPlayableTilesWidth=20, numberOfPlayableTilesHeight=10, tileSize=50, enemySpeed=5, enemyColor=(0, 0, 255)):
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
        self.enemySpeed = enemySpeed
        # set enemy radius as as percentege of tileSizee
        self.enemyRadius = int((tileSize // 2) * 0.6)
        # set number of created tiles
        self.numberOfTilesWidth = numberOfPlayableTilesWidth + 2
        self.numberOfTilesHeight = numberOfPlayableTilesHeight + 2
        # prepare empty variable for screen, font, modes, modeText, field, lastEnemyAims
        self.screen = None
        self.font = None
        self.modes = []
        self.modeText = None
        self.field = None
        self.lastEnemyAims = []
        # start the editor
        self.startEditor()

    # this method handles the whole pygame instance and keeps track of all the process
    def startEditor(self):
        # init pygame
        pygame.init()
        # init the screen
        self.initScreen()
        # start the real editor
        self.running()
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
        # draw last movementpoints of an enemy
        for i in self.lastEnemyAims:
            i.draw(self.screen)
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
        # append change tile outOfBounds / playable
        self.modes.append(('ChangeTile', pygame.K_c))
        # append detectEdges
        self.modes.append(('CreateWalls', pygame.K_w))
        # append setSafe
        self.modes.append(('SafeTile', pygame.K_a))
        # append setGoal
        self.modes.append(('GoalTile', pygame.K_g))
        # append setEnemyStart
        self.modes.append(('NewEnemy', pygame.K_e))
        # append setLastEnemyAim
        self.modes.append(('EnemyMovement', pygame.K_m))
        # append save
        self.modes.append(('Save', pygame.K_s))

    # this method handles the different mode functionalities
    def running(self):
        # set roughly the speed for the game in frames per second
        fps = 30
        # calculate how long to wait by dividing 1000 ms / fps because function needs int round it
        delay = int(1000 / fps)
        # keep track off the current mode and init is to change tiles
        currentMode = self.modes[0][1]
        # keep the editor running until the save mode has been accessed
        while True:
            # add a pygame delay so the game is not always updating
            pygame.time.delay(delay)
            # set flag if mouse was pressed
            click = False
            # get all pressed keys on this frame
            events = pygame.event.get()
            # iterate over all events
            for event in events:
                # detect pressed key event and record key
                if event.type == pygame.KEYDOWN:
                    currentMode = event.key
                # detect click and remember it has been clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                # detect if window has been closed
                if event.type == pygame.QUIT:
                    currentMode = -1
            # python seems like it is not supporting switch cases so do it as if ... elif ...
            # window close
            if currentMode == -1:
                break
            # save mode
            elif currentMode == self.modes[6][1]:
                self.safeFile()
                break
            # change tile mode outOfBound / playable
            elif currentMode == self.modes[0][1]:
                # only if clicked
                if click:
                    self.changeTile()
            # find and walls mode
            elif currentMode == self.modes[1][1]:
                self.setWalls()
            # set safeTiles mode
            elif currentMode == self.modes[2][1]:
                # only if clicked
                if click:
                    self.setSafe()
            # set goal Tiles mode
            elif currentMode == self.modes[3][1]:
                # only if clicked
                if click:
                    self.setGoal()
            # add newEnemy mode
            elif currentMode == self.modes[4][1]:
                # only if clicked
                if click:
                    self.createNewEnemy()
            # add movementPoint to enemy mode
            elif currentMode == self.modes[5][1]:
                # only if clicked
                if click:
                    # IDEA do this and draw a enemy on the point with a alpha value not trivial only surface object has alpha value
                    self.addMovementPoint()
            # if nothing or something unexpected happened don't draw
            else:
                continue
            # redraw display
            self.draw()

    # this methode changes the outOfBoundsValue from a tile and set everything else to the initial parameters the courser is on
    def changeTile(self):
        # get courser position
        (x, y) = self.position()
        # check the position is valid if not just do nothing
        if x == -1:
            return
        # chenge out of bounds flag for relevent tile and reset everything else
        self.field.field[x][y].reset()
        self.field.field[x][y].outOfBounds = not self.field.field[x][y].outOfBounds

    # this method finds all theoretical walls
    def setWalls(self):
        # IDEA if it is to slow improve algorithm
        # because the game does not consists of that many tiles it is valid to just iterate over all tiles
        # corners can be skipped because it is impossible to have a wall
        # edges only need to check one side because the other three are outOfBounds by convention
        for i in range(0, self.numberOfTilesWidth):
            for j in range(0, self.numberOfTilesHeight):
                # only check if tile is outOfBounds
                if not self.field.field[i][j].outOfBounds:
                    continue
                # check only certain tiles if at edge fewer of course
                if i == 0:
                    # is a corner
                    if j == 0 or j == self.numberOfTilesHeight - 1:
                        continue
                    # is left boarder
                    else:
                        # set edge flag if side is not out of bound
                        self.field.field[i][j].edges[1] = not self.field.field[i+1][j].outOfBounds
                elif i == self.numberOfTilesWidth - 1:
                    # is a corner
                    if j == 0 or j == self.numberOfTilesHeight - 1:
                        continue
                    # is right boarder
                    else:
                        # set edge flag if side is not out of bound
                        self.field.field[i][j].edges[3] = not self.field.field[i-1][j].outOfBounds
                else:
                    # is upper boarder
                    if j == 0:
                        # set edge flag if side is not out of bound
                        self.field.field[i][j].edges[2] = not self.field.field[i][j+1].outOfBounds
                    # is lower boarder
                    elif j == self.numberOfTilesHeight - 1:
                        # set edge flag if side is not out of bound
                        self.field.field[i][j].edges[0] = not self.field.field[i][j-1].outOfBounds
                    # is middle
                    else:
                        # we have to check all sides
                        self.field.field[i][j].edges[0] = not self.field.field[i][j-1].outOfBounds
                        self.field.field[i][j].edges[1] = not self.field.field[i+1][j].outOfBounds
                        self.field.field[i][j].edges[2] = not self.field.field[i][j+1].outOfBounds
                        self.field.field[i][j].edges[3] = not self.field.field[i-1][j].outOfBounds
                # set tile is wall if any edge has been set
                self.field.field[i][j].wall = any(self.field.field[i][j].edges)

    # this methode changes the goal from a tile the courser is on
    def setGoal(self):
        # get courser position
        (x, y) = self.position()
        # check the position is valid if not just do nothing
        if x == -1:
            return
        self.field.field[x][y].goal = not self.field.field[x][y].goal

    # this methode changes the start from a tile the courser is on
    def setSafe(self):
        # get courser position
        (x, y) = self.position()
        # check the position is valid if not just do nothing
        if x == -1:
            return
        self.field.field[x][y].safe = not self.field.field[x][y].safe

    # this method creates a new enemy on the tile the courser is on
    def createNewEnemy(self):
        # get courser position
        (x, y) = self.position()
        # check the position is valid if not just do nothing
        if x == -1:
            return
        # find starting pixel of tile and find middle
        (pixelX, pixelY) = self.field.field[x][y].pixelPos
        (pixelX, pixelY) = (pixelX + self.tileSize // 2, pixelY + self.tileSize // 2)
        # create enemy at position
        self.field.enemy.append(Enemy(pixelX, pixelY, self.enemyRadius, self.enemySpeed, self.enemyColor))
        # reset last enemy aims
        self.lastEnemyAims = []

    # this method adds a movement point for the last enemy on the tile the courser is on
    def addMovementPoint(self):
        # get courser position
        (x, y) = self.position()
        # check the position is valid if not just do nothing
        if x == -1:
            return
        # check if at least one enemy exists
        if len(self.field.enemy) == 0:
            return
        # find starting pixel of tile and find middle
        (pixelX, pixelY) = self.field.field[x][y].pixelPos
        (pixelX, pixelY) = (pixelX + self.tileSize // 2, pixelY + self.tileSize // 2)
        # append to last enemy movement point
        self.field.enemy[-1].addMovementPoint(pixelX, pixelY)
        # create inter enemy for aims in lighter color
        # half all color vals
        newCol = tuple(np.add(self.enemyColor,np.multiply(np.subtract((255,255,255),self.enemyColor), 0.5)).astype(int))
        self.lastEnemyAims.append(Enemy(pixelX, pixelY,self.enemyRadius,self.enemySpeed, newCol))

    # this method returns the indices on which the mouse courser is on
    # return (xIdx, yIdx) if it is invalid return (-1, -1)
    def position(self):
        # get pixel position relative to the display
        (x, y) = pygame.mouse.get_pos()
        # calculate which tile in the matrix the courser is on
        xIdx = (x - self.xOff) // self.tileSize
        yIdx = (y - self.yOff) // self.tileSize
        # verify that the courser is in a valid position
        if xIdx <= 0 or yIdx <= 0 or xIdx >= self.numberOfTilesWidth - 1 or yIdx >= self.numberOfTilesHeight - 1:
            return -1, -1
        return xIdx, yIdx

    # this method handles the file saving process
    def safeFile(self):
        print("Please input level name.")
        lvlName = input()
        Writer(lvlName, self.field, self.screenWidth, self.screenHeight)

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

    # TODO think if tis ok to have multiple enemies at the same point
e = Editor()
