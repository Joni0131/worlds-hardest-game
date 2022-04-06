import os
from worlds_hardest_game.src.game.tile import Tile
from worlds_hardest_game.src.game.enemy import Enemy
from worlds_hardest_game.src.game.field import Field

# this class uses the information of the editor to generate a new python file that represents the lvl
class Writer:

    # the writer only needs a lvl name and a field that has to be recorded
    def __init__(self, lvlName, field):
        self.lvlName = lvlName
        self.field = field

    # open the file for write access if the file already exists ask if it should be overwritten or give a new name
    def prepareField(self):
        return

    # first write the class of the level and as well as the needed imports
    def writeLvlClass(self):
        return

    # add all existing tiles to the lvl
    def writeTiles(self):
        return

    # write all the enemies
    def writeEnemy(self):
        return


