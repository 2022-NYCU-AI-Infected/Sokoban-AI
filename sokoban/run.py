from sokoban import *
import pygame

wall = pygame.image.load('images/wall.png')
floor = pygame.image.load('images/floor.png')
box = pygame.image.load('images/box.png')
box_docked = pygame.image.load('images/box_docked.png')
worker = pygame.image.load('images/worker.png')
worker_docked = pygame.image.load('images/worker_dock.png')
docker = pygame.image.load('images/dock.png')
background = 255, 226, 191
pygame.init()
assets = {'wall': wall, 'floor': floor, 'box': box, 'box_docked': box_docked, 'worker': worker, 'worker_docked': worker_docked, 'docker': docker, 'background': background}
level = startGame()
game = Game('levels', level)
size = game.loadSize()
screen = pygame.display.set_mode(size)
while True:
    if game.isCompleted():
        displayEnd(screen)
    printGame(game.getMatrix(), screen, assets)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move(0, -1, True)
            elif event.key == pygame.K_DOWN:
                game.move(0, 1, True)
            elif event.key == pygame.K_LEFT:
                game.move(-1, 0, True)
            elif event.key == pygame.K_RIGHT:
                game.move(1, 0, True)
            elif event.key == pygame.K_q:
                sys.exit(0)
            elif event.key == pygame.K_d:
                game.unmove()
    pygame.display.update()