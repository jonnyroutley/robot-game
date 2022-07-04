import pyxel
import random

# GLOBAL VARS
I_SIZE = 16      # ingredient block size
GAME_W = 192     # width for game playing space
OBJ_W = 64      # width for objective panel
HEIGHT = 128    # window height
I_LIMIT = 110    # height at which ingredients should disappear

#TODO: make real use of global vars - go through and try to remove magic nums
# update objectives/score
# game behaviour:
# pizza order should always be base first then sauce if included
# repeats are allowed 
# ingredients should be collected in order: base, sauce, any order for toppings
# once all ingredients are collected, new order is made - points added and potentially difficulty changed
# if ingredient is added in wrong order, pizza will not change but a strike will be incurred - 3 strikes and game is over
# strike also added for bad ingredient added and pizza will be tossed 




# Ordered list of ingredients for converting 'kind' integer to name
I_LIST = ['Pizza Base', 'Rotten Egg', 'Mushroom', 'Wasabi', 'Aubergine', 'Hammer', 'Swiss Cheese', 
            'Stinky Socks', 'Pepperoni', 'Fish Carcass', 'Mozzarella', 'A... Nose?', 'Tomato Sauce', 'Paperclip', 'Basil']

I_LIST_GOOD = [i for i, item in enumerate(I_LIST) if i % 2 == 0]
I_LIST_BAD = [i for i, item in enumerate(I_LIST) if i % 2 != 0]

class Ingredient:

    def __init__(self, kind, x = 0, y = 0):
        self.x = x
        self.y = y
        self.kind = kind
        self.name = I_LIST[kind]
        self.is_alive = True
        self.is_good = True if kind % 2 == 0 else False

class IngredientList:
    # intention here is to help improve how new ingredients are generated
    # this class uses a factor to create an array with *factor* times more good ingredients than bad
    # the array is then shuffled, and items can be taken from this shuffled array

    def __init__(self, factor = 1):
        self.factor = factor
        self.items = I_LIST_GOOD * factor + I_LIST_BAD
        random.shuffle(self.items)

class App:

    def __init__(self):
        pyxel.init(GAME_W + OBJ_W, HEIGHT, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")
        # starting conditions
        self.score = 0
        self.player_x = 85
        self.player_y = 92
        self.player_dx = 0      #dx is used to indicate last used direction of travel
        self.is_alive = True
        self.strikes = 1
        # checks if there is a pizza base already
        self.is_base = False

        self.factor = 3
        self.IL = IngredientList(self.factor)


        # current pizza that is being built
        self.pizza = []

        # current objectives - which ingredients to collect
        # start by picking 3 ingredients from good list

        

        self.objectives = [Ingredient(0)] + [Ingredient(2*pyxel.rndi(1, len(I_LIST_GOOD)-1)) for i in range(3)]    
        # self.objectives = [0] + [pyxel.rndi(1, len(I_LIST_GOOD)) for i in range(3)]

        # ingredient = (x, y, kind, is_alive)
        # when the game starts, generate some ingredients that are spread horizontally and vertically
        num_ingredients = 3
        # list of Ingredient objects
        self.ingredients = [
            self.generate_ingredient() for i in range(num_ingredients)
        ] 


        # for music: pyxel.playm()
        pyxel.run(self.update, self.draw)

    def update(self):
        # exit game by pressing Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # update robot
        self.update_player()

        # update ingredients
        for i, v in enumerate(self.ingredients):
            self.ingredients[i] = self.update_ingredient(v)


    def update_pizza(self, kind):
            # code - all odd ingredients are bad 
            if kind % 2 == 0:
                self.pizza.append(kind)
                self.score += 1

            else:
                self.pizza = []
                self.score = 0

    def generate_ingredient(self):
        # improvement - good ingredients appear at a different frequency to bad ingredients using IngredientList class

        if not self.IL.items:
            self.IL = IngredientList(self.factor)
        
        kind = self.IL.items.pop()


        # remove this feature for now
            # check to see if there is a pizza base already - if so, do not generate more
            # start_types = 1 if self.is_base else 0
            # num_types = len(I_LIST) - 1


        x = pyxel.rndi(I_SIZE, GAME_W-I_SIZE)
        y = pyxel.rndi(-5*I_SIZE, -I_SIZE)  
        # kind = pyxel.rndi(start_types, num_types)

        return Ingredient(kind, x, y)


    def update_ingredient(self, ingredient):
        # need some terminal condition
        # tray position changes dependent on left/right movement so the centre of the tray at any point is:
        tray_pos = self.player_x + I_SIZE*1.5 if self.player_dx > 0 else self.player_x + I_SIZE/2

        # if ingredient is 'alive' and is at right position relative to tray, ingredient should be added to pizza
        # offset the ingredient so we track the centre of it instead of the top left
        if ingredient.is_alive and abs(ingredient.x + I_SIZE/2 - tray_pos) < 16 and abs(ingredient.y + I_SIZE/2 - self.player_y) < 8:
            ingredient.is_alive = False
            # play sound?

            # add ingredient kind to pizza and update score
            self.update_pizza(ingredient.kind)

        fall_speed = 1
        ingredient.y += fall_speed

        # if ingredient hits the floor, generate a new one
        if ingredient.y > I_LIMIT:
            ingredient = self.generate_ingredient()

        return ingredient

    def update_player(self):

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, -8)
            self.player_dx = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, GAME_W - 24)
            self.player_dx = 1

    def update_objectives(self):
        # when we collect an ingredient we want to:
        # draw an updated pizza on top of the robot
        # change the objectives list to acknowledge the change
        
        # if set(self.pizza).issubset(set(self.objectives))
        pass


    def draw(self):
        pyxel.cls(1)

        # draw background
        pyxel.bltm(0, 0, 0, 0, 0, 192, 128)

        

        # draw ingredients
        for ingredient in self.ingredients:
            if ingredient.is_alive:
                pyxel.blt(ingredient.x, ingredient.y, 1, (ingredient.kind % 4) * I_SIZE, pyxel.floor(ingredient.kind / 4) * I_SIZE, I_SIZE, I_SIZE, 1)



        # draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0 if self.player_dx > 0 else 32, 
            16,
            32,
            32,
            1
        )

        pyxel.pset(self.player_x, self.player_y, 11)

        # draw pizza
        for i, kind in enumerate(self.pizza):    
            pyxel.blt(
                self.player_x + I_SIZE if self.player_dx > 0 else self.player_x,
                self.player_y - I_SIZE - pyxel.floor(i/2), 
                2,
                (kind % 4) * I_SIZE, 
                pyxel.floor(kind / 4) * I_SIZE, 
                I_SIZE, 
                I_SIZE, 
                1
            )

        # draw objectives
        pyxel.bltm(GAME_W, 0, 0, GAME_W, 0, OBJ_W, HEIGHT)
        pyxel.text(GAME_W + OBJ_W/6, 6, "Order's Up!", 0)

        for i, ingredient in enumerate(self.objectives):
            # draw text for ingredient
            pyxel.text(204, (i+1)*24, ingredient.name, 0)
            # draw icon for ingredient
            pyxel.blt(210, (i+1.2)*24, 1, (ingredient.kind % 4) * I_SIZE, pyxel.floor(ingredient.kind / 4) * I_SIZE, I_SIZE, I_SIZE, 1)
            
            # draw tick for correct ingredients in pizza
            if ingredient.kind in self.pizza:
                pyxel.blt(210, (i+1.2)*24, 0, 0, 0, I_SIZE, I_SIZE, 1)



        # draw score
        outstr = "Score: " + str(self.score)
        pyxel.text(8, 8, outstr, 9)

        # draw number of strikes
        # rectangle in top right corner of game canvas
        pyxel.rect(GAME_W - I_SIZE*2 - 3, 1, I_SIZE*2+2, I_SIZE/2+2, 1)

        for i in range(self.strikes):
            pyxel.blt(GAME_W - I_SIZE*2 - 2 + 3*I_SIZE/4*i, 2, 0, I_SIZE, 0, I_SIZE/2, I_SIZE/2, 1)


App()