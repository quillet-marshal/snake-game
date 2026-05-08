# Snake

If you are unfamiliar with Snake you can learn about it here: https://en.wikipedia.org/wiki/Snake_(video_game_genre)

## Pygame version
My first attempt at reproducing Snake using Python. This version of the game was intended for human players and offers a more complete gaming experience. This includes the ability to pause mid-game, to restart after a game over, and a more detailed snake sprite. Additionally, the snake automatically continues moving in the last direction chosen. This significantly increases the difficulty of the game when compared with the Pyglet version.

You can learn more about Pygame here: https://www.pygame.org/docs/

## Pyglet version
This version offers a more simplified version of snake with basic graphics, no menus, no ability to pause, and single-step movement control. I created this version to experiment with Pyglet and I intended to use it with my machine learning code (https://github.com/quillet-marshal/machine-learning-snake) to train a Deep Q Learning (DQN) model. It became inefficient to train using Pyglet due to the unnecessary graphical overhead but this version became the template for the training loop used by the DQN code.

You can learn more about Pyglet here: https://pyglet.org/

## Playing the game
To play either version, you will need to install the Pygame or Pyglet module respectively. Once you have the requisite module installed, you can run the Python code and the game will start.

If you are unfamiliar with the installation of Python modules, you can learn more here: https://docs.python.org/3/installing/index.html
