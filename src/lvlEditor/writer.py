import os
from worlds_hardest_game.src.game.tile import Tile
from worlds_hardest_game.src.game.enemy import Enemy
from worlds_hardest_game.src.game.field import Field


# this class uses the information of the editor to generate a new python file that represents the lvl
class Writer:

    # the writer only needs a lvl name and a field that has to be recorded
    # py having a keywordArgument we make sure field is an instance of the class Field
    def __init__(self, lvlName: str, field: Field, windowWidth: int, windowHeight: int):
        # verify types
        if not isinstance(lvlName, str):
            raise TypeError('Expected str; got %s' % type(lvlName).__name__)
        if not isinstance(field, Field):
            raise TypeError('Expected Field; got %s' % type(field).__name__)
        if not isinstance(windowWidth, int):
            raise TypeError('Expected int; got %s' % type(windowWidth).__name__)
        if not isinstance(windowHeight, int):
            raise TypeError('Expected int; got %s' % type(windowHeight).__name__)
        self.lvlName = lvlName
        # define path relative to this module
        self.filePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, ("lvl/" + self.lvlName + ".py"))
        self.field = field
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

    # open the file for write access if the file already exists ask if it should be overwritten or give a new name
    # then start writing
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

    # TODO later also add starting point of player not relevant at the moment
    # first write the class of the level and as well as the needed imports
    def writeLvlClass(self, fp):
        startComment = '# THIS IS A AUTOGENERATED FILE\n'
        # define the imports if only one argument just import if 2 from [0] import [1]
        imports = [['worlds_hardest_game.src.game.tile', 'Tile'],
                   ['worlds_hardest_game.src.game.enemy', 'Enemy'],
                   ['worlds_hardest_game.src.game.field', 'Field']]
        # create import as string
        importString = ''
        for x in imports:
            if len(x) == 2:
                inter = f'from {x[0]} import {x[1]} \n'
                importString += inter
            else:
                inter = f'import {x[0]}\n'
                importString += inter
        # add two new lines before call creation as standard
        importString += '\n\n'
        # create class declaration and name from lvlName but with uppercase starting letter
        classString = f'class {self.lvlName[0].upper()}{self.lvlName[1::]}:\n'
        # define function __init__(self):
        initFuncString = '\tdef __init__(self):\n'
        # fill the init function with parameters from field
        # add xStart
        initFuncString += f'\t\tself.xStart = {self.field.x}\n'
        # add yStart
        initFuncString += f'\t\tself.yStart = {self.field.y}\n'
        # add windowWidth
        initFuncString += f'\t\tself.windowWidth = {self.windowWidth}\n'
        # add windowHeight
        initFuncString += f'\t\tself.windowHeight = {self.windowHeight}\n'
        # add numberOfTilesWidth
        initFuncString += f'\t\tself.numberOfTilesWidth = {self.field.width}\n'
        # add numberOfTilesHeight
        initFuncString += f'\t\tself.numberOfTilesHeight = {self.field.height}\n'
        # add tileSize
        initFuncString += f'\t\tself.tileSize = {self.field.tileSize}\n'
        # add enemyColor
        initFuncString += f'\t\tself.enemyColor = {self.field.enemyColor}\n'
        # create init field
        initFuncString += f'\t\tself.field = Field(self.xStart, self.yStart, self.numberOfTilesWidth, self.numberOfTilesHeight, self.tileSize, self.enemyColor)\n'
        # call fill Tiles
        initFuncString += '\t\tself.fillTiles()\n'
        # call add enemies
        initFuncString += '\t\tself.fillEnemies()\n'
        # append one more lin so it matches convention
        initFuncString += '\n'
        # now write all prepared strings to the file and continue with the next
        fp.write(startComment)
        fp.write(importString)
        fp.write(classString)
        fp.write(initFuncString)
        self.writeTiles(fp)
        self.writeEnemy(fp)
        self.writeDraw(fp)

    # add all existing tiles to the lvl
    def writeTiles(self, fp):
        # define function
        funcString = f'\tdef fillTiles(self):\n'
        fp.write(funcString)
        # iterate over all tiles
        for idx, tiles in enumerate(self.field.field):
            for jdy, tile in enumerate(tiles):
                # create the tile object
                tileString = f'\t\tself.field.field[{idx}][{jdy}] = Tile({idx}, {jdy}, self.tileSize, self.xStart, self.yStart)\n'
                # fill the tile object with the right parameters
                if tile.safe:
                    tileString += f'\t\tself.field.field[{idx}][{jdy}].safe = True\n'
                if tile.goal:
                    tileString += f'\t\tself.field.field[{idx}][{jdy}].goal = True\n'
                if tile.outOfBounds:
                    tileString += f'\t\tself.field.field[{idx}][{jdy}].outOfBounds = True\n'
                if tile.wall:
                    tileString += f'\t\tself.field.field[{idx}][{jdy}].wall = True\n'
                    # if it is a wall i also has edges so save them as well
                    tileString += f'\t\tself.field.field[{idx}][{jdy}].edges = {tile.edges}\n'
                # write this tile to the level
                fp.write(tileString)
        # for convention write one more empty line
        fp.write('\n')

    # write all the enemies
    def writeEnemy(self, fp):
        # define function
        functionString = f'\tdef fillEnemies(self):\n'
        fp.write(functionString)
        # iterate over each enemy create standard and fill aimPoints
        for enemy in self.field.enemy:
            # initilize inter enemy
            enemyString = f'\t\tinterEnemy = Enemy({enemy.pos[0]}, {enemy.pos[1]}, {enemy.radius}, {enemy.speed}, {enemy.color})\n'
            aims = ''
            # now we know we have to add the aimPoints
            if len(enemy.aimPoints) > 1:
                aims += f'\t\tinterEnemy.addMovementPoints({enemy.aimPoints[1::]})\n'
            # append to all enemies
            appendString = f'\t\tself.field.enemy.append(interEnemy)\n'
            # write to file
            fp.write(enemyString)
            fp.write(aims)
            fp.write(appendString)
        # write one more empty line for convention
        fp.write('\n')

    def writeDraw(self, fp):
        # define draw function add two new lines in the end for convention
        funcString = f'\tdef draw(self, screen):\n' \
                     f'\t\tself.field.draw(screen)\n\n'
        fp.write(funcString)

    # keep this information for now until at least one lvl is created
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
