from sokoban import startGame, Game, displayEnd, printGame
import pygame, copy
import time

validValues = [' ', '#', '@', '.', '*', '$', '+']

class Matrix(list):
    size = None
    target_found = False
    _string = None
    moves = None
    actions = ""

    def getSize(self):
        return self.size

    def getPlayerPosition(self):
        for i in range(len(self)):
            for j in range(len(self[i]) - 1):
                if self[i][j] == "@":
                    return (j, i)

    def getBoxes(self):
        boxes = []
        for i in range(len(self)):
            for j in range(len(self[i]) - 1):
                if self[i][j] == "$":
                    boxes.append((j, i))
        return boxes

    def getTargets(self):
        targets = []
        for i in range(len(self)):
            for j in range(len(self[i]) - 1):
                if self[i][j] == ".":
                    targets.append((j, i))
        return targets

    def isSuccess(self):
        return len(self.getBoxes()) == 0

    def isFailure(self): # useless
        return False

    def getPossibleActions(self):
        x = self.getPlayerPosition()[0]
        y = self.getPlayerPosition()[1]

        def updateValid(item, move, getTwoStep):
            if item not in "*#$":
                return (move, 'Move')
            if item in "$*" and getTwoStep() not in "*#$":
                if item == '$':
                    return (move, 'Push')
                else:
                    return (move, 'PushOut')
            return None
        
        moves = []
        actionCost = updateValid(self[y][x - 1], 'L', lambda: self[y][x - 2])
        if actionCost is not None:
            moves.append(actionCost)
        actionCost = updateValid(self[y][x + 1], 'R', lambda: self[y][x + 2])
        if actionCost is not None:
            moves.append(actionCost)
        actionCost = updateValid(self[y - 1][x], 'U', lambda: self[y - 2][x])
        if actionCost is not None:
            moves.append(actionCost)
        actionCost = updateValid(self[y + 1][x], 'D', lambda: self[y + 2][x])
        if actionCost is not None:
            moves.append(actionCost)
        return moves

    def successor(self, direction, performOnSelf=False):
        if performOnSelf:
            return self.successorInternal(self, direction)
        matrix = copy.deepcopy(self)
        self.successorInternal(matrix, direction)
        matrix._string = None
        return matrix

    def toString(self, clear=False):
        if self._string != None and clear == False:
            return self._string
        self._string = "\n".join(["".join(row) for row in self])
        return self._string

    def getHash(self):
        return hash(self.toString())

    def __hash__(self):
        return self.getHash()

    def __str__(self):
        return self.toString()

    def successorInternal(self, matrix, direction):
        x = matrix.getPlayerPosition()[0]
        y = matrix.getPlayerPosition()[1]
        if direction == "L":
            if matrix[y][x - 1] == " ":
                matrix[y][x - 1] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "

            elif matrix[y][x - 1] == "$":
                if matrix[y][x - 2] == " ":
                    matrix[y][x - 2] = "$"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y][x - 2] == ".":
                    matrix[y][x - 2] = "*"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
            elif matrix[y][x - 1] == "*":
                if matrix[y][x - 2] == " ":
                    matrix[y][x - 2] = "$"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
                elif matrix[y][x - 2] == ".":
                    matrix[y][x - 2] = "*"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
            elif matrix[y][x - 1] == ".":
                matrix[y][x - 1] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True
            else:
                pass

        elif direction == "R":
            if matrix[y][x + 1] == " ":
                matrix[y][x + 1] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "
            elif matrix[y][x + 1] == "$":
                if matrix[y][x + 2] == " ":
                    matrix[y][x + 2] = "$"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y][x + 2] == ".":
                    matrix[y][x + 2] = "*"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
            elif matrix[y][x + 1] == "*":
                if matrix[y][x + 2] == " ":
                    matrix[y][x + 2] = "$"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
                elif matrix[y][x + 2] == ".":
                    matrix[y][x + 2] = "*"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
            elif matrix[y][x + 1] == ".":
                matrix[y][x + 1] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True
            else:
                pass

        elif direction == "D":
            if matrix[y + 1][x] == " ":
                matrix[y + 1][x] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "
            elif matrix[y + 1][x] == "$":
                if matrix[y + 2][x] == " ":
                    matrix[y + 2][x] = "$"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y + 2][x] == ".":
                    matrix[y + 2][x] = "*"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
            elif matrix[y + 1][x] == "*":
                if matrix[y + 2][x] == " ":
                    matrix[y + 2][x] = "$"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
                elif matrix[y + 2][x] == ".":
                    matrix[y + 2][x] = "*"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
            elif matrix[y + 1][x] == ".":
                matrix[y + 1][x] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True
            else:
                pass

        elif direction == "U":
            if matrix[y - 1][x] == " ":
                matrix[y - 1][x] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "
            elif matrix[y - 1][x] == "$":
                if matrix[y - 2][x] == " ":
                    matrix[y - 2][x] = "$"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y - 2][x] == ".":
                    matrix[y - 2][x] = "*"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
            elif matrix[y - 1][x] == "*":
                if matrix[y - 2][x] == " ":
                    matrix[y - 2][x] = "$"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
                elif matrix[y - 2][x] == ".":
                    matrix[y - 2][x] = "*"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True
            elif matrix[y - 1][x] == ".":
                matrix[y - 1][x] = "@"
                if matrix.target_found:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True
            else:
                pass


class API:
    def isValidValue(self, char) -> bool:
        return char in validValues

    def __init__(self, level):
        self.matrix = Matrix()
        self.matrixHistory = []
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
    
    def loadLevel(self):
        file = open('levels', 'r')
        level_found = False
        for line in file:
            row = []
            if not level_found:
                if line.strip() == 'Level ' + str(self.level):
                    level_found = True
            else:
                if line.strip() == '':
                    break
                row = []
                for char in line:
                    if char != '\n' and self.isValidValue(char):
                        row.append(char)
                    elif char == '\n':
                        continue
                    else:
                        print(f'Invalid character in level {self.level}')
                        # sys.exit(1)
                self.matrix.append(list(row))

    def getMatrix(self):
        return self.matrix

        max_row_length = 0
        # Iterate all Rows
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            row_length = len(self.matrix[i])
            if row_length > max_row_length:
                max_row_length = row_length
        self.matrix.size = [max_row_length, len(self.matrix)]
        self.matrix.width = max_row_length
        self.matrix.height = len(self.matrix)

    
    
    
    def start(self):
        pygame.init()
        # level = startGame()
        self.game = Game('levels', self.level)
        size = self.game.loadSize()
        self.screen = pygame.display.set_mode(size)
        printGame(self.game.getMatrix(), self.screen, self.assets)
        pygame.display.update()

        
    def move(self, direction):
        if self.game.isCompleted():
            displayEnd(self.screen)
        if direction == 'U':
            self.game.move(0, -1, True)
        elif direction == 'D':
            self.game.move(0, 1, True)
        elif direction == 'L':
            self.game.move(-1, 0, True)
        elif direction == 'R':
            self.game.move(1, 0, True)
        printGame(self.game.getMatrix(), self.screen, self.assets)
        pygame.display.update()

    def playSeq(self, sequence, delay=0.5):
        for direction in sequence:
            self.move(direction)
            time.sleep(delay)
            if self.game.isCompleted():
                displayEnd(self.screen)
                break


    def getMap(self):
        return self.game.getMatrix()

