# Pie, Robot
### A game made with [Pyxel](https://github.com/kitao/pyxel) inspired by [Pazzi](https://www.youtube.com/watch?v=fNpBDwYLi-Q) and [625 Sandwich Stacker](https://archive.org/details/flash_625-sandwich-stacker).

*Order's Up! Help your robot friend make pizzas by collecting the right ingredients and avoiding the bad stuff.*

<img src="https://github.com/jonnyroutley/robot-game/blob/main/imgs/Game.gif">

Score points by collecting the ingredients (`left/right arrow keys`) shown in order. When a pizza is complete take it to the oven and hit `space` to clear the order and get a points bonus. 

Collecting a wrong ingredient will incur a strike, and if it's one of the nasty ones (*is that a... human nose?*) will mean you have to start the order over. Three strikes and it's game over !


### How to Run
Install Pyxel following these [instructions](https://github.com/kitao/pyxel#how-to-install).

Then run:

```
git clone https://github.com/jonnyroutley/robot-game
cd robot-game/robo_pizza
pyxel play robo_pizza.py.pyxapp
```

Alternatively, you can play in-browser here:
https://kitao.github.io/pyxel/wasm/launcher/?play=jonnyroutley.robot-game.robo_pizza.robo_pizza