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

    def __init__(self, lvlName):
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
        # create empty variables for font and screen
        self.font = None
        self.screen = None
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
        # call running
        self.running()
        # stop pygame
        pygame.quit()

    # this methods handles all the game interactions
    def running(self):
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
            # FIXME wait 10s for debugging
            # sleep(1)
            # update all objects
            self.update()
            # TODO fix key inputs for debugging just option to close the window
            events = pygame.event.get()
            for event in events:
                # detect if window has been closed
                if event.type == pygame.QUIT:
                    running = False

    # this method draws the screen
    def draw(self):
        self.lvl.field.draw(self.screen)
        pygame.display.update()

    # this method updates everything
    def update(self):
        self.lvl.field.move()

g = Game('lvlTest')
sys.exit()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

isRunning = True

# TODO fix sounds
# fail_sound = pygame.mixer.Sound('crash.wav')
# music = pygame.mixer.music.load('music.wav')

# pygame.mixer.music.play(-1)

# TODO move this to lvl data set
player = Player(150, 390, 10, 10)
enemy = Enemy(250, 200, 5, 5, 15)
enemy2 = Enemy(250, 250, 5, 5, 15)
enemy3 = Enemy(500, 250, 5, 5, 15)
enemy4 = Enemy(500, 300, 5, 5, 15)

# TODO create lvl not only from image because is bad to scale
fieldImage = pygame.image.load('field.png')
fieldImage = pygame.transform.scale(fieldImage, (550, 290))

fieldStart = Field(113, 359, 100, 70)
fieldFinish = Field(540, 160, 100, 70)

font = pygame.font.Font('freesansbold.ttf', 32)


def update():
    # TODO change player movement to flags so scalable for genetic Algorithm
    keys = pygame.key.get_pressed()
    player.move(keys)
    # TODO move enemy movement to class update and invoke update as lists or lambda functions not after
    enemy.move(250, 500)
    enemy2.move(250, 500)
    enemy3.move(250, 500)
    enemy4.move(250, 500)

    if player.draw(screen).collidelist([enemy.draw(screen), enemy2.draw(screen), enemy3.draw(screen), enemy4.draw(screen)]) != -1:
        # fail_sound.play()
        player.reset()
        player.deaths += 1
    # TODO fix that only won when whole player in finish
    if player.draw(screen).collidelist([fieldFinish.draw(screen)]) != -1:
        draw()
        print("Finished")
        global isRunning
        isRunning = False

# TODO check if it is possible to not always draw everything because slows down the game


def draw():
    screen.fill((183, 175, 250))
    screen.blit(fieldImage, (100, 150))
    fieldStart.draw(screen)
    fieldFinish.draw(screen)
    pygame.display.update()
    player.draw(screen)
    pygame.display.update()
    enemy.draw(screen)
    enemy2.draw(screen)
    enemy3.draw(screen)
    enemy4.draw(screen)

    deathCounter = font.render(
        "Deaths: " + str(player.deaths), True, (255, 255, 255))
    screen.blit(deathCounter, (300, 50))

    pygame.display.update()


draw()


while isRunning:
    # TODO add score decrease delay feels laggy
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    update()

    if not isRunning:
        break

    draw()

pygame.quit()
