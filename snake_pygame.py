import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((620, 620))
clock = pygame.time.Clock()
running = True # overall software state
playing = True # gameplay is actively happening


## Functions ##

def playerSettings(boardSize=20, scaleColour="orange", eyeColour="black", gameSpeed=10):
    snakeColour = (scaleColour, eyeColour)

    return boardSize, snakeColour, gameSpeed

def gameSettings(boardSize):
    length = 2 # starting length
    snakeSegments = {} # dictionary to record snake segment coordinates
    snakeSegments[0] = int((boardSize ** 2 - boardSize) / 2)  # starting location at centre of board
    snakeSegments.setdefault(length - 1, 0) # dynamically adds segments as length increases

    tileSize = 30 # set tile length/width TO-DO !set dynamically!!!

    return length, snakeSegments, tileSize

def setInitialGameState():
    gameOver = False
    pause = False
    appleExists = False
    direction = None
    lastDirectionMoved = None

    return gameOver, pause, appleExists, direction, lastDirectionMoved

# Renders the game board as a square with grid lines and returns a dict of the tile cords (coordinates)
def renderGameBoard(boardSize, tileSize):
    maxBoardSize = boardSize * tileSize # maximum for the range
    tileIncrements = tileSize + 1 # increments for the range
    gameBoard = {} # create empty dictionary to store the tile cords
    tileKey = 0

    for y in range (0, maxBoardSize, tileIncrements):
        for x in range(0, maxBoardSize, tileIncrements):
            gridTiles = pygame.Rect(x, y, tileSize, tileSize)
            pygame.draw.rect(screen, "white", gridTiles)

            tileKey += 1
            gameBoard[tileKey] = (x, y) # stores each pair of coordinates as a tuple

    return gameBoard

# Renders the snake including a distinct head with eyes
def renderSnake(length, gameBoard, snakeSegments, tileSize, lastDirectionMoved, snakeColour):
    cords = gameBoard[snakeSegments[0]] # get snake head coordinates

    match lastDirectionMoved: # set eye position and size
        case "up":
            leftEye = (cords[0] + 10, cords[1] + 5)
            rightEye = (cords[0] + 17, cords[1] + 5)
            eyeSize = (0.1 * tileSize, 0.3 * tileSize) # (3, 9) for tileSize=30
        case "left":
            leftEye = (cords[0] + 5, cords[1] + 17)
            rightEye = (cords[0] + 5, cords[1] + 10)
            eyeSize = (0.3 * tileSize, 0.1 * tileSize)
        case "right":
            leftEye = (cords[0] + 16, cords[1] + 10)
            rightEye = (cords[0] + 16, cords[1] + 17)
            eyeSize = (0.3 * tileSize, 0.1 * tileSize)
        case _: # None, down, and catch-all
            leftEye = (cords[0] + 17, cords[1] + 16)
            rightEye = (cords[0] + 10, cords[1] + 16)
            eyeSize = (0.1 * tileSize, 0.3 * tileSize)

    snakeHead = (  
        (pygame.Rect(cords[0], cords[1], tileSize, tileSize), snakeColour[0]), 
        (pygame.Rect(leftEye[0], leftEye[1], eyeSize[0], eyeSize[1]), snakeColour[1]), 
        (pygame.Rect(rightEye[0], rightEye[1], eyeSize[0], eyeSize[1]), snakeColour[1])
        )

    for i in range(0, len(snakeHead)): # render head and eyes
        pygame.draw.rect(screen, snakeHead[i][1], snakeHead[i][0])

    for n in range(1, length): # render body
        position = snakeSegments[n]
        if position != 0:
            cords = gameBoard[position]
            snakeTile = pygame.Rect(cords[0], cords[1], tileSize, tileSize)
            pygame.draw.rect(screen, snakeColour[0], snakeTile)

def renderApple(gameBoard, appleLocation, tileSize):
    cords = gameBoard[appleLocation]
    appleTile = pygame.Rect(cords[0], cords[1], tileSize, tileSize)
    pygame.draw.rect(screen, "blue", appleTile)

# Provides a random spawn location to try
def spawnApple(boardSize):
    appleLocation = random.randrange(1, (boardSize ** 2) + 1)

    return appleLocation

# Update the snake's location and move in the currently-set direction
def moveSnake(direction, snakeSegments, length, boardSize): # slither
    for s in range(length, 0, -1):
        snakeSegments[s] = snakeSegments[s - 1] # each snake tile follows the same route the head moved
    
    match direction: # moves the head
        case "up":
            snakeSegments[0] -= boardSize
        case "down":
            snakeSegments[0] += boardSize
        case "left":
            snakeSegments[0] -= 1
        case "right":
            snakeSegments[0] += 1

    return snakeSegments

# Renders text evenly across the screen (must use '\n' to manually format text) TO-DO add font size variable in player settings
def renderText(text, fontName="Calibri", fontSize=40, isBold=True, resolution=620):
    lines = text.split('\n') # pygame cannot handle newlines
    gameFont = pygame.font.Font(pygame.font.match_font(fontName, isBold), fontSize)

    # Check if there is enough space on screen to render the text
    if (gameFont.size(text)[0] * gameFont.size(text)[1]) > (resolution ** 2):
        lines = ["ERROR while trying to display text"]
        print("ERROR: Not enough screen space to render text")

    yStart = resolution / (len(lines) + 1)

    for n in range(0, len(lines)):
        spaceNeeded = gameFont.size(lines[n])
        xOffset = (resolution - spaceNeeded[0]) / 2
        yOffset = (yStart * (n + 1)) - (spaceNeeded[1] / 2)

        targetSurface = pygame.Rect(xOffset, yOffset, spaceNeeded[0], spaceNeeded[1])
        textSurface = gameFont.render(lines[n], True, "black")
        screen.blit(textSurface, targetSurface)
        

## Initial Variables ##

boardSize, snakeColour, gameSpeed = playerSettings() # get player settings
length, snakeSegments, tileSize = gameSettings(boardSize) # set game settings
gameOver, pause, appleExists, direction, lastDirectionMoved = setInitialGameState() # set game state variables


## Start of Gameplay ##

while running:

    while playing:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                running = False
                gameOver = True

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # RENDER YOUR GAME HERE
        gameBoard = renderGameBoard(boardSize, tileSize)
        renderSnake(length, gameBoard, snakeSegments, tileSize, lastDirectionMoved, snakeColour)

        # check for self-collision
        snakeLocations= {}
        try:
            for segment in snakeSegments:
                snakeLocations[snakeSegments[segment]] = snakeLocations.get(snakeSegments[segment], 0) + 1
                if playing and snakeLocations[snakeSegments[segment]] > 1:
                    print("DEBUG: Self-collision; Segment collided with:", segment)
                    gameOver = True
        except:
            print("ERROR: Self-collision check failed")
            gameOver = True

        # spawn the apple if it has been eaten
        if not gameOver and appleExists:
            renderApple(gameBoard, appleLocation, tileSize)

        elif not gameOver:
            appleLocation = spawnApple(boardSize)
            appleExists = True

            for i in range(0, length):
                if appleLocation == snakeSegments[i]:
                    appleExists = False
                    print("DEBUG: Apple spawn collision avoided")

        # eat the apple if it intersects with the snake's head, and lengthen the snake
        if not gameOver and appleExists and snakeSegments[0] == appleLocation:
            length += 1
            appleExists = False

        # detect input and prevent snake turning 180 degrees
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not gameOver and lastDirectionMoved != "down":
            direction = "up"
        if keys[pygame.K_s] and not gameOver and lastDirectionMoved != "up":
            direction = "down"
        if keys[pygame.K_a] and not gameOver and lastDirectionMoved != "right":
            direction = "left"
        if keys[pygame.K_d] and not gameOver and lastDirectionMoved != "left":
            direction = "right"

        if keys[pygame.K_SPACE] and not gameOver:
            print("DEBUG: Game paused")
            pause = True
            playing = False

        # move the snake in the direction it is pointing, and check if it hit anything
        if not gameOver and not pause and direction != None:
            previousLocation = snakeSegments[0]
            snakeSegments = moveSnake(direction, snakeSegments, length, boardSize)
            lastDirectionMoved = direction

            if snakeSegments[0] < 1:
                print("DEBUG: Snake hit the top of the gameboard")
                gameOver = True
            elif snakeSegments[0] > boardSize ** 2:
                print("DEBUG: Snake hit the bottom of the gameboard")
                gameOver = True
            elif (snakeSegments[0] - 1) % boardSize == 0 and previousLocation % boardSize == 0:
                print("DEBUG: Snake hit the right side of the gameboard")
                gameOver = True
            elif snakeSegments[0] % boardSize == 0 and (previousLocation - 1) % boardSize == 0:
                print("DEBUG: Snake hit the left side of the gameboard")
                gameOver = True

        if gameOver and running:
            print("DEBUG: Final snake length was", length)
            playing = False

        pygame.display.flip() # flip() the display to put your work on screen
        clock.tick(gameSpeed) # limits FPS to 10


    ## Pause Menu ##

    while pause and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pause = False

        # screen.fill("grey") # wipe previous screen; comment out to leave the current game on screen
        renderText("Game Paused\nPress R to resume\n Press Escape to exit") # TO-DO ?hold space to resume?

        keys = pygame.key.get_pressed()
        if pause and keys[pygame.K_r]:
            print("DEBUG: Resuming game from pause")
            playing = True
            pause = False

        if pause and keys[pygame.K_ESCAPE]:
            print("DEBUG: Exiting from pause")
            running = False
            pause = False

        pygame.display.flip()
        clock.tick(gameSpeed)


    ## Game Over Menu ##

    while gameOver and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = False
                running = False

        screen.fill("grey") # wipe previous screen
        renderText("GAME OVER\nFinal length was " + str(length) + "\nTry Again?\nPress R to retry\nPress Escape to exit")

        keys = pygame.key.get_pressed()
        if gameOver and keys[pygame.K_ESCAPE]:
            print("DEBUG: Exiting from game over menu")
            gameOver = False
            running = False

        if gameOver and keys[pygame.K_r]:
            print("DEBUG: Starting new game now")

            # reset to initial game parameters
            boardSize, snakeColour, gameSpeed = playerSettings()
            length, snakeSegments, tileSize = gameSettings(boardSize)
            gameOver, pause, appleExists, direction, lastDirectionMoved = setInitialGameState()
            
            playing = True

        pygame.display.flip()
        clock.tick(gameSpeed)


pygame.quit()

'''

#### TO-DO ####

-add boilerplate and version

-add adaptive resolution and board size options

-figure out speed/FPS control
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

-add cause of death to game over menu

-make more things functions?

-add menu with settings (board size, speed, resolution, controls?, colour scheme?)

-look up python global variables, reduce number of passed args to functions
    i.e. gameBoard, tileSize, etc.

-replace self-collision code with a pygame function such as:
    https://www.pygame.org/docs/ref/rect.html

    # pygame.Rect.collidedict
    # test if one rectangle in a dictionary intersects

    # pygame.Rect.collidelist
    # test if one rectangle in a list intersects

    # pygame.Rect.contains
    # test if one rectangle is inside another


'''