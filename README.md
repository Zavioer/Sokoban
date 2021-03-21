# Sokoban

Application which is a project for the Motorola Science Cup competition.

This is a game whose goal is to move and place crates in the warehouse to the designated positions playing as a warehouse worker.
-  A warehouse is a board that consists of a layout of fields.
-  Warehouse keeper controlled by a player can move vertically or horizontally (never diagonally).
-  He can only push one box, and cannot pull or pass through it.
-  The warehouseman's task is to move the boxes to all designated positions - the boxes can only be moved individually.

### Technology stack

- Python

# Navigation

1. [Getting Started](#getting-started)

- [Prerequisites](#prerequisites)
- [How to ...?](#how-to)
  - [How to install dependencies](#how-to-install-dependencies)
  - [How to run game](#how-to-run-game)
  - [How to run tests](#how-to-run-tests)
  - [How to create documentation](#how-to-create-documentation)

2. [FAQ](#faq)

1. [DEFINITIONS](#definitions)

- [What is this app?](#what-is-this-app)
- [What was the content of the task this application responds to?](#what-was-the-content-of-the-task-this-application-responds-to)
- [Contributors](#contributors)

2. [FEATURES](#features)

- [What stages does the game consist of?](#what-does-the-application-show-on-the-map)
- [First stage](#first-stage)
- [Second stage](#second-stage)
- [Third stage](#third-stage)

3. [SCREENSHOTS](#screenshots)

## Getting started

### Prerequisites

- Pygame 2.0.0
- Python 3.8.6

### How to

1. #### How to install dependencies

To install dependencies open a command prompt in the game folder and type in:

```bash
pip install -r requirements.txt
```

2. #### How to run game

To run game open a command prompt in the game folder and type in:

```bash
py app.py
```

3. #### How to run tests

To run all tests go to the **tests** subfolder and run:

```bash
python -m unittest tests.logic_test
```

4. #### How to create documentation

To create the documentation, go to the **docs** subfolder, open a command prompt, and type in

```bash
make html
```

It will create documentation itself, that will be placed in **_build** folder. 

## FAQ

If you have some more questions, you may find an answer in the following topics.

1. [DEFINITIONS](#definitions)

- [What is this app?](#what-is-this-app)
- [What was the content of the task this application responds to?](#what-was-the-content-of-the-task-this-application-responds-to)
- [Contributors](#contributors)

2. [FEATURES](#features)

- [What stages does the game consist of?](#what-stages-does-the-game-consist-of)
- [First stage](#first-stage)
- [Second stage](#second-stage)
- [Third stage](#third-stage)

### Definitions

#### What is this app?

This is a logical game where you can turn into a warehouse keeper and expand the mind by putting the chests in the right places.

#### What was the content of the task this application responds to?

"This is a game whose goal is to move and place crates in the warehouse to the designated positions.
-  A warehouse is a board that consists of a layout of fields.
-  Warehouse keeper controlled by a player can move vertically or horizontally (never diagonally).
-  He can only push one box, and cannot pull or pass through it.
-  The warehouseman's task is to move the boxes to all designated positions - the boxes can only be moved individually."

#### Contributors

- [Piotr Bator](https://github.com/Zavioer)
- [Gabriel Brzoskwinia](https://github.com/brzoskwi)

### Features

#### What stages does the game consist of?

This game has three stages.

1. ##### First stage

- The player can play on one of the 20 prepared boards (the maximum size of the board is 30x20 fields).
- Each of the boards is assigned one of three difficulty levels.
- The player chooses one of the three difficulty levels and starts the game.

2. ##### Second stage

- After starting the application, the player selects one of the three game modules.
- In the second stage, he starts the game on 20 boards with increasing difficulty levels.
- Points are added up, the number of points is made up of the map passage time.
- The player has the option to interrupt and save the game and return to it after restarting the application.
- The player may end the game. The result will be included in the final ranking.
- The player can check the ranking.

3. ##### Third stage

- After starting the application, the player selects one of the three game modules.
- Choosing the third module of the game gives the player the opportunity to play on a previously created and saved board.
- The player has the option to stop the game and save the game.
- The player can not only create and save his boards, but also delete them.
- The player on the board with a maximum size of 30 x 20 fields places walls, a warehouse keeper, boxes and target positions for boxes.
- In the third module, he can only play on one of the boards previously created by himself.

### Screenshots

![gameplayScreenshot](https://user-images.githubusercontent.com/40405579/111919260-61bf1f00-8a89-11eb-9c77-be9a161c110f.png)
![mapCreating](https://user-images.githubusercontent.com/40405579/111919261-6257b580-8a89-11eb-9bea-7308c7fb373c.png)
