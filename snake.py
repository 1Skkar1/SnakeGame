import math
import time
import datetime
import random
import pygame

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
GOLD = (255,223,0)

# window
width = 500
height = 535

# surface
cols = 25
rows = 25

# globals
win = 0
food = 0
s = 0
endTime = 0


class square:
    rows = 25
    w = 500

    def __init__(self, start, dirX=1, dirY=0, color=GREEN):
        self.pos = start
        self.dirX = dirX
        self.dirY = dirY
        self.color = color
    
    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)
    
    def spawn(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + dis - radius * 2, j * dis + 14)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 6)
            pygame.draw.circle(surface, BLACK, circleMiddle, radius)
            pygame.draw.circle(surface, BLACK, circleMiddle2, radius)


class snake:
    body = []
    turns = {}
    score = 0

    def __init__(self, color, pos):
        self.color = color
        self.head = square(pos)
        self.body.append(self.head)
        self.dirX = 0
        self.dirY = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]
                elif keys[pygame.K_ESCAPE]:
                    pygame.quit()
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirX, c.dirY)

    def reset(self, pos):
        self.head = square(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.score = 0
        self.dirX = 0
        self.dirY = 1

    def increaseBody(self):
        tail = self.body[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.body.append(square((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(square((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(square((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(square((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirX = dx
        self.body[-1].dirY = dy

    def spawn(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.spawn(surface, True)
            else:
                c.spawn(surface)


def redrawWindow():
    global win, endTime

    win.fill(BLACK)
    drawGrid(width, rows, win)
    s.spawn(win)
    food.spawn(win)
    textScore = "SCORE: " + str(s.score)
    label = game_font.render(textScore, 1, WHITE)
    win.blit(label, (width - label.get_width() - 10, 510))
    currentTime = pygame.time.get_ticks() - endTime
    passed_time = "TIME: " + str(datetime.timedelta(seconds=currentTime / 1000))
    label = game_font.render(passed_time, 1, WHITE)
    win.blit(label, (10, 510))
    pygame.display.update()
    pass


def drawGrid(w, rows, surface):
    sizeGap = w // rows
    x = 0
    y = 0

    for i in range(rows):
        x = x + sizeGap
        y = y + sizeGap
        pygame.draw.line(surface, WHITE, (x,0), (x,w))
        pygame.draw.line(surface, WHITE, (0,y), (w,y))


def randomFood(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)

        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    
    return x, y


def end():
    global s, food, win, endTime

    win.fill((0, 0, 0))
    textScore = "SCORE:"
    numScore = str(s.score)
    goNext = replaytitle_font.render('Press any button to play again', 1, WHITE)
    dontgoNext = replaytitle_font.render('Press Esc to quit', 1, WHITE)
    label = title_font.render(textScore, 1, WHITE)
    label2 = score_font.render(numScore, 1, WHITE)
    win.blit(label, (width / 2 - label.get_width() / 2, 100))
    win.blit(label2, (width / 2 - label2.get_width() / 2, 140))
    win.blit(goNext, (width / 2 - goNext.get_width() / 2, 475))
    win.blit(dontgoNext, (width / 2 - dontgoNext.get_width() / 2, 500))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                again = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                again = False
    s.reset((10, 10))
    s.increaseBody()
    endTime = pygame.time.get_ticks()


def main():
    global s, food, win

    bonus = False
    win = pygame.display.set_mode((width, height))
    s = snake(GREEN, (10,10))
    s.increaseBody()
    food = square(randomFood(rows, s), color=RED)
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos

        if headPos[0] >= rows or headPos[0] < 0 or headPos[1] >= rows or headPos[1] < 0:
            end()

        if s.body[0].pos == food.pos:
            if food.color == RED:
                s.score += 1
            elif food.color == GOLD:
                s.score += 5
                bonus = False
            s.increaseBody()
            food = square(randomFood(rows, s), color=RED)

        if len(s.body) % 10 == 0 and bonus is False:
            food = square(randomFood(rows, s), color=GOLD)
            bonus = True

        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z:z.pos, s.body[i + 1:])):
                end()
                break

        redrawWindow()


pygame.init()
title_font = pygame.font.SysFont('yanmartext', 50)
score_font = pygame.font.SysFont('consolas', 35)
game_font = pygame.font.SysFont('consolas', 20)
replaytitle_font = pygame.font.SysFont('consolas', 15)
icon = pygame.image.load('assets/logo.png')
pygame.display.set_caption('Snake Game')
pygame.display.set_icon(icon)
main()
