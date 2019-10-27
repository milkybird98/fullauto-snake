# FULLAUTO Snake
 a Snake game with a simple ai inside

## Getting Started

```
git clone https://github.com/milkybird98/FULLAUTO-Snake
cd FULLAUTO-Snake
python snake_ai.py
```
Once in the menu, press UP or DOWN to choose ai mode or manuly mode ( just like a normal snake game )
+ Use UP, DOWN, LEFT and RIGHT four arrow keys to contorl your snake in manuly mode.
+ Just watch the twisting snake in your screen in ai mode.
+ Press ESC to exit.

## Prerequisites
In the game, curses is used to generate the game CUI in you shell.
### Windows
```
pip install windows-curses
```
### Linux
```
pip install curses
```

## Installing
You dont need to installing process to play this game.

# Usage
Change the WIDTH and HEIGTH in line 377 to change the game map size ( default 15*30).
```
WIDTH = 15
HEIGTH = 30
```
Change the AI_STEP_DELAY and MAN_STEP_DELAY in line 380 to change the delay time between snake movements, and when it's larger, the slower the game would be. ( The unit is millisecond )
```
AI_STEP_DELAY = 0
MAN_STEP_DELAY = 500
```

# FULLAUTO
## Algorithm
In this implementation, snake would do following "thinkings" by order
1. is there a way between the food and snake head, if not, goto step 4
2. can snake's head follow its tail after eated food, if not goto step 4
3. choose shorest way to eat food, go back to 1
4. can snake follow its tail, if not goto step 6
5. choose longest way to follow tail, go back to 1
6. make any possible movement, go back to 1

## Drawbacks
In the algorithm.step2, the only way to check whether snake's head can follow its tail is to generate the future game map that snake eating the food. 

This process will be done in a virtual map, simulate every steps before virtual snake eat food, and each step require a full map DFS to find the shorest way to the food.

And worse, now this game can only consume one CPU core, so when map size become larger than 40*40, the game speed would crazily slow.

# Versioning
Beta 0.99
