import pygame
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
            self.screenHeight = (numberOfPlayableTilesHeight + 4) * tileSize#
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
        self.enemyColor = enemyColor
        # prepare empty variable for screen, font, modes, modeText
        self.screen = None
        self.font = None
        self.modes = []
        self.modeText = None
        # start the editor
        self.startEditor()

    # this method handles the whole pygame instance and keeps track of all the process
    def startEditor(self):
        # init pygame
        pygame.init()
        # start the screen
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        # set font
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        # initialize modes
        self.initModes()

        # FIXME just draw text and field to check
        self.screen.fill((183, 175, 250))
        # add mode information to screen
        self.screen.blit(self.modeText, (5, 5))
        pygame.display.update()
        sleep(10)
        # stop pygame
        pygame.quit()

    # this method initializes all modes
    def initModes(self):
        self.setModes()
        self.drawModeInformation()

    # this method is creating the action information object
    def drawModeInformation(self):
        # FIXME using escape sequence works for command prompt but not for rendered image
        stringMode = ''
        for (info, key) in self.modes:
            stringMode += f'{info}{self.keyInfo(key)} '
        # convert to string
        stringMode = str(stringMode)
        print(stringMode)
        self.modeText = self.font.render(stringMode, True, (0, 0, 0))

    # method to get a string of a key for the info example key s in pygame is pygame.K_s and this should convert to (S͟)
    def keyInfo(self, key: int):
        string = f"({stringFormat.escapeSequence['UNDERLINE']}{chr(key).upper()}{stringFormat.escapeSequence['END']})"
        return string

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
