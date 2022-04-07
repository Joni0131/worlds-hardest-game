from worlds_hardest_game.src.game.tile import Tile
from worlds_hardest_game.src.game.enemy import Enemy


# this class handles the state of the playing field except the player
class Field:
    # parameter x and y is the starting pixel
    # parameter tileSize defines the length of an edge of a tile
    # parameter enemyColor defines the enemy color
    # parameter width and height define the number of tiles in that direction
    def __init__(self, x, y, width, height, tileSize=50, enemyColor=(0, 0, 255)):
        self.x = x
        self.y = y
        self.tileSize = tileSize
        self.enemyColor = enemyColor
        self.width = width
        self.height = height
        self.enemyRadius = tileSize * 0.3  # defines the radius of an enemy as 1/3 of the tileSize
        self.field = [[None] * height] * width  # list of list that keeps track of all tiles as field[x][y]
        self.enemy = []  # list that keeps track of all enemies

    # define draw function
    def draw(self, screen):
        # call the drawing of all fields
        for i in self.field:
            for j in i:
                j.draw(screen)
        # draw all enemies
        for i in self.enemy:
            i.draw(screen)

    # a function that calls the move update for all enemies
    def move(self):
        for x in self.enemy:
            x.move()





