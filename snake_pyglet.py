import pyglet
from pyglet import shapes
from pyglet.window import key

import random

def moveSnake(movement): # moves whole snake one space along its path
    for i in range(len(snakeDict) - 1, 0, -1):
        snakeDict[i].position = snakeDict[i - 1].position

    match movement:
        case "up":
            snake.y += tSize
        case "left":
            snake.x -= tSize
        case "down":
            snake.y -= tSize
        case "right":
            snake.x += tSize

def randomCord(): # returns a random valid coordinate
    return random.randrange(0, (window.size[0]) - tSize + 1, tSize)

def spawnApple(): # spawns apple in an empty space
    validSpawn = False
    while not validSpawn:
        apple.x = randomCord()
        apple.y = randomCord()
        for i in range(0, len(snakeDict)):
            if apple.position == snakeDict[i].position:
                print("DEBUG: Apple tried to spawn on top of snake segment ", i)
                validSpawn = False
                break
            else:
                validSpawn = True


window = pyglet.window.Window(800, 800)
batch = pyglet.graphics.Batch()

label = pyglet.text.Label('Hello, world', # default example only
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

# todo - make game stats object with number of steps taken, time elapsed, etc.

tSize = 40 # tile size

snake = shapes.Rectangle(randomCord(), randomCord(), tSize, tSize, color=(255, 255, 155), batch=batch)
snakeDict = {}
snakeDict[0] = snake
apple = shapes.Rectangle(0 - tSize, 0 - tSize, tSize, tSize, color=(55, 55, 255), batch=batch)
spawnApple()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W: moveSnake("up")
    elif symbol == key.A: moveSnake("left")
    elif symbol == key.S: moveSnake("down")
    elif symbol == key.D: moveSnake("right")

    if snake.x < 0 or snake.y < 0 or snake.x >= 800 or snake.y >= 800:
        print("DEBUG: Snake went out-of-bounds, last position was ", snake.position)
        pyglet.app.exit()

    for i in range(1, len(snakeDict)):
        if snake.position == snakeDict[i].position:
            print("DEBUG: Snake self-collision, snake segment number ", i)
            pyglet.app.exit()

    if snake.position == apple.position:
        spawnApple()
        snakeDict[len(snakeDict)] = shapes.Rectangle(0 - tSize, 0 - tSize, tSize, tSize, color=(255, 200, 55), batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()