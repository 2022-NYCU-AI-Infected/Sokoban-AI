from sokoban import startGame, Game, displayEnd, printGame
import pygame

class API:
    def __init__(self, level):
        self.level = level
        wall = pygame.image.load('images/wall.png')
        floor = pygame.image.load('images/floor.png')
        box = pygame.image.load('images/box.png')
        box_docked = pygame.image.load('images/box_docked.png')
        worker = pygame.image.load('images/worker.png')
        worker_docked = pygame.image.load('images/worker_dock.png')
        docker = pygame.image.load('images/dock.png')
        background = 255, 226, 191
        self.assets = {'wall': wall, 'floor': floor, 'box': box, 'box_docked': box_docked, 'worker': worker, 'worker_docked': worker_docked, 'docker': docker, 'background': background}
        pygame.init()
    
    def start(self):
        # level = startGame()
        self.game = Game('levels', self.level)
        size = self.game.loadSize()
        self.screen = pygame.display.set_mode(size)
        printGame(self.game.getMatrix(), self.screen, self.assets)
        pygame.display.update()

    def move(self, direction):
        if self.game.isCompleted():
            displayEnd(self.screen)
        if direction == 'up':
            self.game.move(0, -1, True)
        elif direction == 'down':
            self.game.move(0, 1, True)
        elif direction == 'left':
            self.game.move(-1, 0, True)
        elif direction == 'right':
            self.game.move(1, 0, True)
        printGame(self.game.getMatrix(), self.screen, self.assets)
        pygame.display.update()
