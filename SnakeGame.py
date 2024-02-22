
import pygame
import sys
import random
import time
import os
import msvcrt

# Set directory where code started
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

pygame.init()
clock = pygame.time.Clock()
random.seed()

# Set up the drawing window
screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption('Snake')
gameWidth = 640
gameHeight = 480
backGroundColor = (0,0,0)

class Point:
    x = 0
    y = 0

class foodPoint:
    x = 0
    y = 0
    exist = False

#=======================================================
# SNAKE
class Snake:
    headColor = (0,200,10)
    tailColor = (0,200,0)
    x = 270 # Snakes head start coordinates
    y = 330
    movingStep = 3 # snake speed pixels/step (or game cycle)
    xDir = 0 # Snakes moving directions 
    yDir = -movingStep # starts upward by amount of movingStep
    snakeGrow = 0 # When snake eats food, this is set higher value. eg. 3*movingStep increases lenght by 3
    snakeParts = [] # List for snakes tail
    currentHead = 0
    head = [] # List for head images. One for each direction
    headOffsetX = 0
    headOffsetY = 0  
    
    def __init__(self,snakeInitLen = 20): # Snakes initial lenght
        del self.snakeParts[:]
        del self.head[:]
        for i in range(0,snakeInitLen): # make snakes tail
            self.snakeParts.append(Point())
            self.snakeParts[i].y = self.y + (i*self.movingStep)
            self.snakeParts[i].x = self.x
        self.head.append(pygame.image.load("SnakeHead1.bmp").convert_alpha())
        self.headOffsetX = self.head[0].get_width()/2
        self.headOffsetY = self.head[0].get_height()/2
        self.head.append(pygame.image.load("SnakeHead2.bmp").convert_alpha())
        self.head.append(pygame.image.load("SnakeHead3.bmp").convert_alpha())
        self.head.append(pygame.image.load("SnakeHead4.bmp").convert_alpha())
        self.snakeMask = pygame.mask.from_surface(self.head[0]) # Collision mask. Heads are identical in shapes - only one needed
   
    def moveSnake(self):
        #global snakeGrow
        if snake.snakeGrow > 0: # Snake is set to grow up lenght
            self.snakeParts.append(Point()) # make new part to the end of snake
            self.snakeGrow -= self.movingStep # Decrease growing variable by one step
        for i in range(len(self.snakeParts)-1,0,-1):
            self.snakeParts[i].x = self.snakeParts[i-1].x # Move snakes coordinates backwards...
            self.snakeParts[i].y = self.snakeParts[i-1].y # ...that moves snake forward
        self.snakeParts[0].x = self.x # Second part os snake get snakes former position 
        self.snakeParts[0].y = self.y
        self.x += self.xDir # Finally snakes head gets new position
        self.y += self.yDir         
            
    def drawSnake(self):
        snakeLenght = len(self.snakeParts)-1
        #pygame.draw.circle(screen, self.headColor, (self.x, self.y), 7) # snakes head as circle
        
        # self.x and self.y are pointing to the middle of the image. So they are changed to top left of image with offsetsS
        screen.blit(self.head[self.currentHead], (self.x - self.headOffsetX, self.y - self.headOffsetY)) 
        for i in range(0,snakeLenght-1): # Rest of snake
            pygame.draw.circle(screen, self.tailColor, (self.snakeParts[i].x, self.snakeParts[i].y), 5)
        pygame.draw.circle(screen, self.tailColor, (self.snakeParts[snakeLenght-1].x, self.snakeParts[snakeLenght-1].y), 4) # Tail before tip
        pygame.draw.circle(screen, self.tailColor, (self.snakeParts[snakeLenght].x, self.snakeParts[snakeLenght].y), 3) # Tail tip

    # check collision to food and borders
    def checkCollision(self):
        # Check if hit food
        global gameScore, gameSpeed
        X_offset = food.x - self.x+self.headOffsetX
        Y_offset = food.y - self.y+self.headOffsetY
        if self.snakeMask.overlap(foodMask,(X_offset, Y_offset)):
            self.snakeGrow = self.movingStep * 3
            food.exist = False
            gameScore += 20
            if foodIndex == 4:
                gameSpeed = 120
            else:
                gameSpeed = 60
           
        # Check collision to borders
        if self.x < 40 or self.x > 510 or self.y < 30 or self.y > 450:
            global gameRuns    
            gameRuns = False

    # Check collision to own tail
    def checkSelfCollision(self):
        global gameRuns
        color = pygame.Surface.get_at(screen,((self.x + self.xDir * 3),(self.y + self.yDir * 3)))
        if color == self.tailColor:
            gameRuns = False

# END OF SNAKE   
#==================================================================================================
            
#==============================================================
# Read high scores from file
#==============================================================
highScores = []
def createNewFile(): # if not found make new file
    for i in range(0,5): 
            highScores.append(f"{'AAA'};{0}\n") 
            with open("snakescores.txt","w") as scoreFile:
                for i in highScores:
                    scoreFile.write(i)
    readHighScores()

def readHighScores():
    highScores.clear()
    try:
        myfile = open("snakescores.txt", "r") # Try open high scores file
        for i in myfile:
            list = i.strip()
            list = list.split(";")
            highScores.append(list)
        myfile.close                       
    except IOError:
        createNewFile()
        
def saveHighScores():
    with open("snakescores.txt","w") as scoreFile:
        for i in highScores:
             scoreFile.write(f"{i[0]};{i[1]}\n") 
                    
def printHighScores():
    yPos = 185
    for i in highScores:
        text = (f"{i[0]}")
        score1 = font3.render(text, True, (200,200,200))
        screen.blit(score1, (535, yPos))
        text = (f"{i[1]}")
        score1 = font3.render(text, True, (200,200,200))
        screen.blit(score1, (585, yPos))
        yPos += 25
# END OF HIGH SCORES
#==============================================================

#---------------------------------------------------------------------------------
# Set food on screen
def setFood(): 
    foodSet = False
    while foodSet == False:
        foodX = random.randint(45, gameWidth-145)
        foodY = random.randint(40, gameHeight-45)
        foodSet = True
    food.x = foodX
    food.y = foodY
    food.exist = True
#================================================================================
# Keyboard and mouse input events
#================================================================================   
def readKeyboard():
    keys = pygame.key.get_pressed()  #Checking pressed keys
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if snake.yDir != snake.movingStep: # Prevent snake to start backwards
            snake.xDir = 0
            snake.yDir = -snake.movingStep
            snake.currentHead = 0
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if snake.yDir != -snake.movingStep:
            snake.xDir = 0
            snake.yDir = snake.movingStep
            snake.currentHead = 2
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if snake.xDir != snake.movingStep:
            snake.xDir = -snake.movingStep
            snake.yDir = 0
            snake.currentHead = 3
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if snake.xDir != -snake.movingStep:    
            snake.xDir = snake.movingStep
            snake.yDir = 0
            snake.currentHead = 1
    
#--------------------------------------------------------------------
# Return values for eHandler:
# 0 nothing happened
# 1 Any key pressed
# 2 p key was pressed
# 3 mouse was clicked

def eventHandler():
    global snake, xx, yy
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            del snake
            pygame.quit()
            sys.exit()
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return 2 
            return 1 

        # Check if mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            xx,yy=pygame.mouse.get_pos() # Used to see coordinates
            return 3
    return 0
# END OF INPUTS
#========================================================================

# Game paused. Wair for a key to continue
def gamePaused(message):
    while True:
        global gameIsPaused
        txtOffset = 50 
        gamePausedText = font.render(message, True, (0,0,0))
        screen.blit(gamePausedText, (txtOffset, 50))
        gamePausedText = font.render(message, True, (200,200,200))
        screen.blit(gamePausedText, (txtOffset+2, 52))
        pygame.display.update()
        if eventHandler() != 0:
            gameIsPaused = False
            break
#------------------------------------------------------
# Input for high score initials
def writeEvent():
    global user_initials 
    global initialsCount  
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key > 47 and event.key < 123: # Letter or number including some other character
                    user_initials += event.unicode
                    initialsCount += 1
                if event.key == pygame.K_BACKSPACE and initialsCount > 0:
                    user_initials = user_initials[:-1]
                    initialsCount -= 1
                               
def askInitials():
    global user_initials 
    global initialsCount
    user_initials = ""
    text_box = pygame.Rect(225,200,120,40)
    
    # Empty keyboard buffer 
    for event in pygame.event.get(): 
        if event.type != pygame.KEYDOWN:
            break
    
    while True:
        writeEvent()
        pygame.draw.rect(screen,(0,0,0),text_box)
        teksti = font.render("HIGH SCORE", True, (0,0,0))
        screen.blit(teksti, (175, 125))
        teksti = font.render("HIGH SCORE", True, (200,200,200))
        screen.blit(teksti, (177, 127))
        teksti2 = font2.render("Enter your initials", True, (0,0,0))
        screen.blit(teksti2, (175, 160))
        teksti2 = font2.render("Enter your initials", True, (200,200,200))
        screen.blit(teksti2, (177, 162))
        surf = font.render(user_initials,True,(200,200,200))
        screen.blit(surf, (text_box.x + 10 , text_box.y - 5))
        pygame.display.update()

        if initialsCount == 3:
            if user_initials == "":
                user_initials = "---"
            time.sleep(1)
            initialsCount = 0
            return user_initials.upper()
              
def endOfGame():
    global gameScore
    global snake
    # Show GAME OVER -text
    teksti = font.render("GAME OVER", True, (0,0,0))
    screen.blit(teksti, (180, 240))
    teksti = font.render("GAME OVER", True, (200,200,200))
    screen.blit(teksti, (182, 242))
    pygame.display.update()
    time.sleep(2)
    # Check if score is higher than any of existing scores
    i = 0
    while i < 5:
        if gameScore > int(highScores[i][1]):
            for j in range(4,i,-1):
                highScores[j] = highScores[j-1]
            inits = askInitials()
            highScores[i] = (inits,gameScore)
            break
        i += 1
    gameScore = 0
    saveHighScores()
    
def newGame():
    global snake
    global gameMessage
    global gameIsPaused
    global gameSpeed
    snake = Snake() # Make new snake
    readHighScores()
    gameSpeed = 60
    gameIsPaused = True
    gameMessage = '   Press any key to start'
    return True

#------------------------------------------------------------------- 
xx = 0
yy = 0
user_initials = ''
initialsCount = 0
gameIsPaused = True
gameRuns = True
gameScore = 0
gameSpeed = 60

food = foodPoint()
food.exist = False
foodImg = []
foodIndex = 0
foodImg.append(pygame.image.load("fruit1.bmp").convert_alpha())
foodImg.append(pygame.image.load("fruit2.bmp").convert_alpha())
foodImg.append(pygame.image.load("fruit3.bmp").convert_alpha())
foodImg.append(pygame.image.load("fruit4.bmp").convert_alpha())
foodImg.append(pygame.image.load("turbo.bmp").convert_alpha())
foodMask = pygame.mask.from_surface(foodImg[0])

backgroudImage  = pygame.image.load("backg1.png").convert()

font = pygame.font.SysFont('comicsansms', 32,True)
font2 = pygame.font.SysFont('comicsansms', 24,True)
font3 = pygame.font.SysFont('agencyfb', 20,True)
newGame()

#====================================================================
# MAIN LOOP
#====================================================================   
while True:
    # Read inputs = keyboard and mouse
    keys = eventHandler()
    if keys == 2:
        gameIsPaused = True
        gameMessage = 'Game paused. Press any key'
    elif keys == 66:
        gameRuns = False
    readKeyboard()

    # Set the background image
    screen.blit(backgroudImage, (0, 0))
    
    # Texts
    score = font.render(str(gameScore), True, (200,200,200))
    scoreX = 618 - score.get_width()
    screen.blit(score, (scoreX, 70))
    printHighScores()

    # Draw food on screen is exists. If not make new
    if food.exist == True: 
        screen.blit(foodImg[foodIndex], (food.x,food.y))
    else:
        foodIndex = random.randint(0, 4)
        setFood()
    
    snake.moveSnake()
    snake.checkCollision()
    
    snake.drawSnake() # Snake must be drawn before checking collision to self
    snake.checkSelfCollision()

    pygame.display.flip()
    if gameIsPaused == True:
        gamePaused(gameMessage)

    clock.tick(gameSpeed)  # 60 frames per second
    if gameRuns == False:
        initialsCount = 0
        endOfGame()
        if newGame() == True:
            gameRuns = True
