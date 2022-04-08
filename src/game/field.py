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
        self.field = [[None]*height for _ in range(width)]  # list of list that keeps track of all tiles as field[x][y]
        self.enemy = []  # list that keeps track of all enemies
        # initialize field
        self.initTiles()
        print("finished init")

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

    # this method initializes all tiles
    # the outermost tiles as outOfBounds
    def initTiles(self):
        # iterate over all possible tiles
        for i in range(0, self.width):
            for j in range(0, self.height):
                # create tile
                self.field[i][j] = Tile(i, j, self.tileSize, self.x, self.y)
                # if outermost tile set outOfBounds
                if i == 0 or j == 0 or i == self.width - 1 or j == self.height - 1:
                    self.field[i][j].outOfBounds = True
