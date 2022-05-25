'''
FlabbyPird.py
@Klaus
26.04.2022
'''

import pygame
from pygame.locals import *

from sys import *
import random
import time

# Variables ====================

go = "j"
fps = 24
Width = 450
Height = 600

partikel = 10
brickspeed = 8
downspeed = 4
borderheight = Height - partikel*2.5

counter = 0

BLACK  = (0,0,0)
YELLOW = (255,255,0)
RED = (205,51,51)
GREEN = (0,128,0)

bricks = []



# Walking Bricks ================
# =============================================

class Bricks():
    def __init__(self, where, colour, left, top, width, height, speed):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top 
        self.bottomtop = 0
        self.width = width
        self.height = height
        self.bottomheight = 0
        self.speed = speed
        self.gapHeight = Height/4
        self.gaplocker = random.randint(Height*0.3, Height*0.6)

    #====TWO DIFFERENT BRICKS WITHOUT GAP
    #===============================================

    def drawBrick (self):
        self.top = 0
        self.bodytop=pygame.draw.rect(self.where, self.colour, [self.left, self.top, self.width, self.height])
        self.bottomtop = self.height + self.gapHeight
        self.bottomheight = borderheight - self.bottomtop
        self.bodybottom=pygame.draw.rect(self.where, self.colour, [self.left, self.bottomtop, self.width, self.bottomheight])  

    def walk(self):        
        self.left -= self.speed

    def lvlUp(self):
        self.speed *= 1.2


# jumpinPird =======================
# =====================================================

class Pird():
    def __init__(self, where, colour, left, top, width, height, speed):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.speed = speed
        self.jumpVar = -16


    def drawPird(self):
        self.body=pygame.draw.ellipse(self.where, self.colour, [self.left, self.top, self.width, self.height])

    def fallDown(self):
        if self.top < Height:
            self.top += self.speed
            self.speed += 1.1


    def jumpUp(self):
        # stupid Jump
        # ======================
        #self.top -= self.speed*10

        # dynamic Jump
        # ========================
        if self.jumpVar == -16:
            self.jumpVar = 15

        if self.jumpVar >= -15:
            n = 1
            if self.jumpVar < 0:
                n = -1
            self.top -= (self.jumpVar**2.1)*0.17*n

        self.speed = downspeed

class Bottom():
    def __init__(self, where, colour, left, top, width, height):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top 
        self.width = width
        self.height = height

    def draw(self):
        self.body=pygame.draw.rect(self.where, self.colour, [self.left, self.top, self.width, self.height])


# ======================================
# M A I N ==============================
# ======================================

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([Width, Height])      
pygame.display.set_caption("FlabbyPird")


border = Bottom(screen, GREEN, 0, borderheight, Width, partikel*2.5)
pird = Pird(screen,RED, Width*0.3, Height/2-partikel*2, partikel*4, partikel*3, downspeed)
topBrickHeight = random.randint(Height*0.3, Height*0.6)
startBrick = Bricks(screen, YELLOW , Width + partikel , 0, partikel*2, Height*0.4, brickspeed)
startBrick.height = topBrickHeight

bricks.append(startBrick)




while go == "j":
    screen.fill(BLACK)

    # ====== suicide pird
    border.draw()
    pird.drawPird()
    pird.fallDown()
    
    # ============================
    # ====== the walking bricks
    for i in bricks:
        i.drawBrick()
        i.walk()
        if i.left <= Width*0.4 and i.left >= Width*0.39:       
            counter += 1     
            topBrickHeight = random.randint(Height*0.2, Height*0.8)
            bricks.append(Bricks(screen, YELLOW, Width + partikel , 0, partikel*2, startBrick.height, brickspeed))
            bricks[counter].height = topBrickHeight
            

        # Prepare To Die 
        #================================
        if i.bodytop.colliderect(pird.body) or i.bodybottom.colliderect(pird.body) or border.body.colliderect(pird.body):
            time.sleep(3)
            go = "n"
        # ==============================

    # ===========================

    for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
            go = "n"

        # jumpin`OutOfDeath ==============
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pird.jumpUp()

    my_font = pygame.font.Font(None, 50)
    surface = my_font.render(str(counter), True, (255,255,255))
    text_rect = surface.get_rect()
    text_rect.center = (Width*0.75, Height * 0.15)
    screen.blit(surface, text_rect)

    pygame.display.flip()
    clock.tick(fps)



pygame.quit()