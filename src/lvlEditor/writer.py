import os
from worlds_hardest_game.src.game.tile import Tile
from worlds_hardest_game.src.game.enemy import Enemy
from worlds_hardest_game.src.game.field import Field


# this class uses the information of the editor to generate a new python file that represents the lvl
class Writer:

    # the writer only needs a lvl name and a field that has to be recorded
    # py having a keywordArgument we make sure field is an instance of the class Field
    def __init__(self, lvlName: str, field: Field):
        # verify types
        if not isinstance(lvlName, str):
            raise TypeError('Expected str; got %s' % type(lvlName).__name__)
        if not isinstance(field, Field):
            raise TypeError('Expected Field; got %s' % type(field).__name__)
        self.lvlName = lvlName
        # define path relative to this module
        self.filePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ("lvl/" + self.lvlName + ".py"))
        self.field = field

    # open the file for write access if the file already exists ask if it should be overwritten or give a new name
    def prepareField(self):
        # first verify that lvlName is a valid file name
        if not self.validFileName(self.lvlName):
            print("The initial file name is not valid")
            self.askForNewFileName()
        # while the file already exists ask if it should be overwritten
        while self.fileExists():
            print(f"The file {self.lvlName}.py already exists. Do you wanna overwrite the existing file?")
            print("Y for Yes / N for No and input new file name")
            userInput = input()
            # if yes just continue to open as write
            if userInput == 'Y':
                break
            # if not ask for new file name and update path
            if userInput == 'N':
                self.askForNewFileName()
                self.filePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ("lvl/" + self.lvlName + ".py"))
        # open file path with writing access if the file doesn't exist it is created
        fp = open(self.filePath, 'w')
        # start the writing process
        self.writeLvlClass(fp)
        # close the file pointer for safe programming
        fp.close()

    # check if the file exists
    def fileExists(self):
        # check if the file already exists
        if os.path.exists(self.filePath):
            return True
        else:
            return False

    # make sure the file name doesn't have any invalid characters
    @staticmethod
    def validFileName(name):
        # list off illegal characters as well as - and .
        illegalChars = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/', ' ', '$', '!',
                        '\'', '\"', ':', '@', '+', '`', '|', '=', '-', '.']
        # iterate over all illegal chas and check if any is part of the name
        for char in illegalChars:
            if char in name:
                print("The character {char} is not allowed to be part of the fileName")
                return False
        # check that the file name starts with a lower case character
        if not name[0].islower():
            print("The first character has to be lower case")
            return False
        return True

    # this function handles the asking for a new file name
    def askForNewFileName(self):
        # IDEA maybe ask for new name in window not command prompt
        print("Please input a new file name without file extension")
        newName = input()
        # verify that it is a valid name if not ask again
        if self.validFileName(newName):
            self.lvlName = newName
        else:
            self.askForNewFileName()

    # first write the class of the level and as well as the needed imports
    def writeLvlClass(self, fp):
        return

    # add all existing tiles to the lvl
    def writeTiles(self, fp):
        return

    # write all the enemies
    def writeEnemy(self, fp):
        return

    # Imports of Level class
    # from worlds_hardest_game.src.game.field import Field
    # from worlds_hardest_game.src.game.enemy import Enemy
    # from worlds_hardest_game.src.game.tile import Tile
    #
    # Needed attributes of Level class:
    # field
    # windowWidth
    # windowHeight
    # xStart
    # yStart
    # numberOfTilesWidth
    # numberOfTilesHeight
    # tileSize
    # enemyColor
    #
    # Functions of Level class:
    # __init__(self) set all attributes
    # draw call to field
    # setTiles called in __init__ as function for easier implementation
    # setEnemies called in __init__ as function for easier implementation
