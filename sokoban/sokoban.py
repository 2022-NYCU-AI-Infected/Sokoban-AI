import sys
import pygame
import string
import queue

validVlaue = [' ', '#', '@', '.', '*', '$', '+']

class Game:
    def isValidValue(self, char) -> bool:
        if char in validVlaue:
            return True
        else:
            return False
    def __init__(self, filename, level) -> None:
        self.queue = queue.LifoQueue()
        self.matrix = []

        if level < 1:
            print('Level must be greater than 0')
            sys.exit(1)
        else:
            file = open(filename, 'r')
            level_found = False
            for line in file:
                row = []
                if not level_found:
                    if line.strip() == 'Level ' + str(level):
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
                            print(f'Invalid character in level {level}')
                            sys.exit(1)
                    self.matrix.append(row)

    def loadSize(self) -> tuple:
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)
    
    def getMatrix(self) -> list:
        return self.matrix
    
    def printMatrix(self) -> None:
        for row in self.matrix:
            print(row)

    def getContent(self, x, y) -> str:
        return self.matrix[y][x]

    def setContent(self, x, y, value) -> None:
        if self.isValidValue(value):
            self.matrix[y][x] = value
        else:
            print(f'Invalid value {value} to be set')
    
    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x += 1
            x = 0
            y += 1

    def canMove(self, x, y) -> bool:
        wx, wy, wpos = self.worker()
        return self.getContent(wx + x, wy + y) not in ['#', '*', '$']

    def next(self, x, y) -> str:
        wx, wy, wpos = self.worker()
        return self.getContent(wx + x, wy + y)

    def canPush(self, x, y) -> bool:
        return (self.next(x, y) in ['*', '$'] and self.next(x + x, y + y) in [' ', '.'])

    def isCompleted(self) -> bool:
        for row in self.matrix:
            for pos in row:
                if pos == '$':
                    return False
        return True

    def moveBox(self, x, y, a, b):
        correntBox = self.getContent(x, y)
        futureBox = self.getContent(x + a, y + b)
        if correntBox == '$' and futureBox == ' ':
            self.setContent(x + a, y + b, '$')
            self.setContent(x, y, ' ')
        elif correntBox == '$' and futureBox == '.':
            self.setContent(x + a, y + b, '*')
            self.setContent(x, y, ' ')
        elif correntBox == '*' and futureBox == ' ':
            self.setContent(x + a, y + b, '$')
            self.setContent(x, y, '.')
        elif correntBox == '*' and futureBox == '.':
            self.setContent(x + a, y + b, '*')
            self.setContent(x, y, '.')
    
    def unmove(self):
        if not self.queue.empty():
            movement = self.queue.get()
            if movement[2]:
                corrent = self.worker()
                self.move(movement[0] * -1, movement[1] * -1, False)
                self.moveBox(corrent[0] + movement[0], corrent[1] + movement[1], movement[0] * -1, movement[1] * -1)
            else:
                self.move(movement[0] * -1, movement[1] * -1, False)
    
    def move(self, x, y, save):
        if self.canMove(x, y):
            current = self.worker()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.setContent(current[0] + x, current[1] + y, '@')
                self.setContent(current[0], current[1], ' ')
                if save:
                    self.queue.put((x, y, False))
            elif current[2] == '@' and future == '.':
                self.setContent(current[0] + x, current[1] + y, '+')
                self.setContent(current[0], current[1], ' ')
                if save:
                    self.queue.put((x, y, False))
            elif current[2] == '+' and future == ' ':
                self.setContent(current[0] + x, current[1] + y, '@')
                self.setContent(current[0], current[1], '.')
                if save:
                    self.queue.put((x, y, False))
            elif current[2] == '+' and future == '.':
                self.setContent(current[0] + x, current[1] + y, '+')
                self.setContent(current[0], current[1], '.')
                if save:
                    self.queue.put((x, y, False))
        elif self.canPush(x, y):
            current = self.worker()
            future = self.next(x, y)
            futureBox = self.next(x + x, y + y)
            if current[2] == '@' and future == '$' and futureBox == ' ':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], ' ')
                self.setContent(current[0] + x, current[1] + y, '@')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '@' and future == '$' and futureBox == '.':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], ' ')
                self.setContent(current[0] + x, current[1] + y, '@')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and futureBox == ' ':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], ' ')
                self.setContent(current[0] + x, current[1] + y, '+')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '@' and future == '*' and futureBox == '.':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], ' ')
                self.setContent(current[0] + x, current[1] + y, '+')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '+' and future == '$' and futureBox == ' ':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], '.')
                self.setContent(current[0] + x, current[1] + y, '@')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '+' and future == '$' and futureBox == '.':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], '.')
                self.setContent(current[0] + x, current[1] + y, '+')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and futureBox == ' ':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], '.')
                self.setContent(current[0] + x, current[1] + y, '+')
                if save:
                    self.queue.put((x, y, True))
            elif current[2] == '+' and future == '*' and futureBox == '.':
                self.moveBox(current[0] + x, current[1] + y, x, y)
                self.setContent(current[0], current[1], '.')
                self.setContent(current[0] + x, current[1] + y, '+')
                if save:
                    self.queue.put((x, y, True))

def printGame(matrix, screen, assets):
    screen.fill(assets["background"])
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == ' ':
                screen.blit(assets["floor"], (x, y))
            elif char == '#':
                screen.blit(assets["wall"], (x, y))
            elif char == '@':
                screen.blit(assets["worker"], (x, y))
            elif char == '.':
                screen.blit(assets["docker"], (x, y))
            elif char == '*':
                screen.blit(assets["box_docked"], (x, y))
            elif char == '$':
                screen.blit(assets["box"], (x, y))
            elif char == '+':
                screen.blit(assets["worker_docked"], (x, y))
            x += 32
        x = 0
        y += 32

def getKey():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

def displayBox(screen, message):
    fontObject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() / 2 - 100, screen.get_height() / 2 - 10, 200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() / 2 - 102, screen.get_height() / 2 - 12, 204, 24), 1)
    if len(message) != 0:
        screen.blit(fontObject.render(message, 1, (255, 255, 255)), (screen.get_width() / 2 - 100, screen.get_height() / 2 - 10))
    pygame.display.flip()

def displayEnd(screen):
    message = "You Win!"
    fontObject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() / 2 - 100, screen.get_height() / 2 - 10, 200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() / 2 - 102, screen.get_height() / 2 - 12, 204, 24), 1)
    screen.blit(fontObject.render(message, 1, (255, 255, 255)), (screen.get_width() / 2 - 100, screen.get_height() / 2 - 10))
    pygame.display.flip()

def ask(screen, question):
    pygame.font.init()
    current_string = []
    displayBox(screen, question + ": " + ''.join(current_string))
    while True:
        inkey = getKey()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        displayBox(screen, question + ": " + ''.join(current_string))
    return ''.join(current_string)

def startGame():
    start = pygame.display.set_mode((320, 240))
    level = int(ask(start, "Select Level"))
    if level > 0:
        return level
    else:
        print("Invalid Level")
        sys.exit(2)

