# Crooy's snake
# Julu 2022

import random
import time
import copy
import pygame
import numpy as np
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_z,
    K_x,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption('CrooySnake')

#set frames per second for the game loop
FPS = 10
fpsclock = pygame.time.Clock()
#set block drop rate (number of frames per drop)
moveRate = 2
pygame.key.set_repeat(10000, 10000)

screenWidth = 900
screenHeight = 800
gridWidth = 12
gridHeight = 12
gridSquareSize = 50
gridWidthOffset = 0
gridHeightOffset = 0
maxGridWidthPx = gridWidth * gridSquareSize
maxGridHeightPx = gridHeight * gridSquareSize

# Set up the drawing window
screen = pygame.display.set_mode([screenWidth, screenHeight])

# SEt background colour
background = pygame.Surface(screen.get_size())
background = background.convert()   
background.fill((255,228,181))

# set game surface
gameSurface = pygame.Surface((maxGridWidthPx + 1, maxGridHeightPx + 1))
gameSurface.fill((255,255,255))
gameRect = gameSurface.get_rect()

# fonts
font = pygame.font.Font('freesansbold.ttf', 26)
fontLarge = pygame.font.Font('freesansbold.ttf', 52)

# header
header = fontLarge.render('CROOY\'S SNAKE', True, (0, 0, 0), (255, 255, 255))

# scoreboard
scoreboardText = font.render('Score', True, (0, 0, 0), (255, 255, 255))
scoreboardScore = fontLarge.render('1', True, (0, 0, 0), (255, 255, 255))
scoreboard = pygame.Surface((100,100))
scoreboard.fill((0,0,0))
scoreboard.blit(scoreboardText, (15,10))
scoreboard.blit(scoreboardScore, (40,40))
            
# draw grid onto surface
currentXPos = gridWidthOffset
x = 0
while x < gridWidth + 1:
    pygame.draw.line(gameSurface, (0, 0, 0), [currentXPos, gridWidthOffset], [currentXPos, maxGridHeightPx])
    currentXPos = currentXPos + gridSquareSize
    x = x + 1

currentYPos = gridHeightOffset
y = 0
while y < gridHeight + 1:
    pygame.draw.line(gameSurface, (0, 0, 0), [gridHeightOffset, currentYPos], [maxGridWidthPx, currentYPos])
    currentYPos = currentYPos + gridSquareSize
    y = y + 1


#GridSquare class
class GridSquare(pygame.sprite.Sprite):
    def __init__(self, gameSurface, xPos, yPos, size, status):
        super(GridSquare, self).__init__()
        self.surf = pygame.Surface((size - 5, size - 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = ((xPos*size)+(size/2), (yPos*size)+(size/2)))
        
        self.gameSurface = gameSurface
        self.xPos = xPos
        self.yPos = yPos
        self.size = size
        self.status = status
        self.colour = 'white'

    def setColour(self,colour):
        if colour == 'random':
            self.surf.fill((random.randint(30,225),random.randint(30,225),random.randint(30,225)))
        if colour == 'red':
            self.surf.fill((106,5,7))
        if colour == 'green':
            self.surf.fill((0, 63, 17))
        if colour == 'orange':
            self.surf.fill((233, 68, 0))
        if colour == 'blue':
            self.surf.fill((0,0,108))
        if colour == 'purple':
            self.surf.fill((60,5,74))
        if colour == 'slate':
            self.surf.fill((93,106,122))
        if colour == 'white':
            self.surf.fill((255,255,255))              

    def setStatus(self,status):
        self.status = status
        if status == 'snakeHead':
            self.setColour('blue')

        if status == 'snakeBody':
            self.setColour('purple')

        if status == 'mouse':
            self.surf.fill((250, 253, 15))
            
        if status == '-':
            self.surf.fill((255, 255, 255))
            
        if status == 'crash':
            self.setColour('red')
        
        if status == 'baddy':
            self.setColour('slate')

#declare a 2d array of GridSquare, size [gridWidth, gridHeight] 
gridSquareList = [[GridSquare(gameSurface, x, y, gridSquareSize, '-') for y in range(int(gridHeight))] for x in range(int(gridWidth))]
    
# Main loop
running = True
loopCount = 0
currentXPos = int(gridWidth/2)
currentYPos = int(gridHeight/2)
gridSquareList[currentXPos][currentYPos].setStatus('snakeHead')
gridSquareList[random.randint(0,gridWidth-1)][random.randint(0,gridHeight-1)].setStatus('mouse')
mouseFrequency = 10
baddyFrequency = 20
currentDirection = 'right'
snakeLength = 1
snakeList = [[currentXPos,currentYPos]]
foundMouseFlag = 0
    
def increaseSnakeSize(snakeList, xPos, yPos):
    snakeList.append([xPos, yPos])
    return snakeList

isCrash = 0
while running and isCrash == 0:
    loopCount = loopCount + 1                                 
        
    # loop through the list and blit onto the gameSurface 
    for i in range(gridWidth):
        for j in range(gridHeight):
            gameSurface.blit(gridSquareList[i][j].surf, gridSquareList[i][j].rect)

    screen.blit(background, ( 0, 0 ))
    screen.blit(header, ((screenWidth - gameSurface.get_width()) / 2, 10))
    screen.blit(scoreboard, (25, (screenHeight - gameSurface.get_height()) / 2))
    screen.blit(gameSurface, ( (screenWidth - gameSurface.get_width()) / 2, (screenHeight - gameSurface.get_height()) / 2) )
     
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user close the window?
        if event.type == QUIT:
            pygame.quit()
            running = False

    pressedKeys = pygame.key.get_pressed()
                
    #keydown left/right/down/up - change direction - do not allow diagonals
    if pressedKeys[K_UP] and not(pressedKeys[K_DOWN]) and not(pressedKeys[K_LEFT]) and not(pressedKeys[K_RIGHT]) and currentDirection != 'down':
        currentDirection = 'up'
        
    if pressedKeys[K_DOWN] and not(pressedKeys[K_UP]) and not(pressedKeys[K_LEFT]) and not(pressedKeys[K_RIGHT]) and currentDirection != 'up':
        currentDirection = 'down'
        
    if pressedKeys[K_LEFT] and not(pressedKeys[K_DOWN]) and not(pressedKeys[K_UP]) and not(pressedKeys[K_RIGHT]) and currentDirection != 'right':
        currentDirection = 'left'

    if pressedKeys[K_RIGHT] and not(pressedKeys[K_DOWN]) and not(pressedKeys[K_UP]) and not(pressedKeys[K_LEFT]) and currentDirection != 'left':
        currentDirection = 'right'


    if loopCount % moveRate == 0:       
        #deselect current pos
        #gridSquareList[currentXPos][currentYPos].setStatus('-')
        #gridSquareList[snakeList[0][0]][snakeList[0][1]].setStatus('-')

        i = 0
        newSnakeList = copy.deepcopy(snakeList)
        newSnakeList.clear()
        
        currentXPos = snakeList[0][0]
        currentYPos = snakeList[0][1]
        newCurrentXPos = currentXPos
        newCurrentYPos = currentYPos 

        #set new head pos
        if currentDirection == 'up':
            if currentYPos > 0:
                newCurrentYPos = currentYPos - 1
            else:
                newCurrentYPos = gridHeight-1
            
        if currentDirection == 'down' :
            if currentYPos < gridHeight-1:
                newCurrentYPos = currentYPos + 1
            else:
                newCurrentYPos = 0
            
        if currentDirection == 'left':
            if currentXPos > 0:
                newCurrentXPos = currentXPos - 1
            else:
                newCurrentXPos = gridWidth-1

        if currentDirection == 'right':
            if currentXPos < gridWidth-1:
                newCurrentXPos = currentXPos + 1
            else:
                newCurrentXPos = 0

        #deselect the final snake part
        gridSquareList[snakeList[snakeLength - 1][0]][snakeList[snakeLength - 1][1]].setStatus('-')

        #add the head to the new snake
        newSnakeList.append([newCurrentXPos, newCurrentYPos])

        #construct the rest of the snake's body
        i = 0
        while i < snakeLength - 1:
            newSnakeList.append([snakeList[i][0], snakeList[i][1]])
            i = i + 1                
        
        snakeList = copy.deepcopy(newSnakeList)
        print(str(snakeList))

    #draw new mouse if needed
    if loopCount % mouseFrequency == 0:
        gridSquareList[random.randint(0,gridWidth-1)][random.randint(0,gridHeight-1)].setStatus('mouse')

    #draw new baddy if needed
    if loopCount % baddyFrequency == 0:
        gridSquareList[random.randint(0,gridWidth-1)][random.randint(0,gridHeight-1)].setStatus('baddy')
        
    #crash! game over
    if gridSquareList[snakeList[0][0]][snakeList[0][1]].status == 'snakeBody' or gridSquareList[snakeList[0][0]][snakeList[0][1]].status == 'baddy':
        print('crash!!!')
        i = 0
        while i < snakeLength-1:
            gridSquareList[snakeList[i][0]][snakeList[i][1]].setStatus('crash')
            print(gridSquareList[snakeList[i][0]][snakeList[i][1]].status)
            isCrash = 1
            header = fontLarge.render('CROOY\'S SNAKE CRASHED!', True, (0, 0, 0), (255, 255, 255))
            screen.blit(header, ((screenWidth - gameSurface.get_width()) / 2, 10))
            i = i + 1

    #we have found a mouse! Increase snake length by 1
    if gridSquareList[snakeList[0][0]][snakeList[0][1]].status == 'mouse':
        snakeList = increaseSnakeSize(snakeList, currentXPos, currentYPos)
        snakeLength = snakeLength + 1
        
        scoreboardScore = fontLarge.render(str(snakeLength), True, (255, 255, 255), (0, 0, 0))
        scoreboard.blit(scoreboardScore, (40,40))

    if isCrash == 0:
        i = 0
        while i <= snakeLength-1:
            gridSquareList[snakeList[i][0]][snakeList[i][1]].setStatus('snakeBody')
            i = i + 1
        gridSquareList[snakeList[0][0]][snakeList[0][1]].setStatus('snakeHead')
    
    #update display
    pygame.display.flip()
    fpsclock.tick(FPS)


    


    
