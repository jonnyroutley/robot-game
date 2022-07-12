# Import Modules
import pyxel
from random import shuffle

# Import Classes
from Ingredient import Ingredient
from IngredientList import IngredientList
from Objective import Objective    

# GLOBAL VARS
I_SIZE = 16      # ingredient block size
GAME_W = 192     # width for game playing space
OBJ_W = 64      # width for objective panel
HEIGHT = 128    # window height
I_LIMIT = 110    # height at which ingredients should disappear

#TODO:
# add speech bubbles for bad items
# enforce base collection first
# allow for an entirely bad pizza order to come in sometimes
# add variable difficulty as game progresses
# NOTE: pizza and objectives might not both be necessary - pizza is essentially our fulfilled objectives




# Ordered list of ingredient names for converting 'kind' integer to name
I_NAMES = ['Pizza Base', 'Rotten Egg', 'Mushroom', 'Wasabi', 'Aubergine', 'Hammer', 'Swiss Cheese', 
            'Stinky Socks', 'Pepperoni', 'Fish Carcass', 'Mozzarella', 'A... Nose?', 'Tomato Sauce', 'Paperclip', 'Basil']

# The ingredients are ordered such that all the even ones are good to eat and the odds are not
# we can therefore define two more lists that the store the indices of the good and bad ingredients respectively
I_NUMS_GOOD = [i for i, item in enumerate(I_NAMES) if i % 2 == 0]
I_NUMS_BAD = [i for i, item in enumerate(I_NAMES) if i % 2 != 0]


# objectives are the kinds of ingredients we want to collect
# ingredients are the falling objects that the player collects
# pizza is a list of the kind of ingredients that have been collected by the player


class App:

    def __init__(self):
        pyxel.init(GAME_W + OBJ_W, HEIGHT, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")

        # player starting conditions
        self.score = 0
        self.player_x = 85
        self.player_y = 92
        self.player_dx = 0      #dx is used to indicate last used direction of travel
        self.is_alive = True
        self.strikes = 0

        self.objectives = self.generate_objectives()

        # current pizza that is being built
        self.pizza = []
        self.is_base = False     #  used to see if pizza contains a base        

        # factor may become game difficulty - it determines how many more times 'good' ingredients are generated as compared to 'bad' ones. 
        # IL is a shuffled list of ingredients from which we pick the next ingredients to appear
        self.factor = 3
        self.IL = IngredientList(self.factor, I_NUMS_GOOD, I_NUMS_BAD)

        # the number of ingredients that should be in play at any one time - this could also act as a difficulty modifier
        num_ingredients = 4
        # create a list of the Ingredient objects that are initially falling
        self.ingredients = [
            self.generate_ingredient() for i in range(num_ingredients - 1)
        ] 


        # for music: pyxel.playm()

        # run the game by calling update and draw
        pyxel.run(self.update, self.draw)

    def update(self):
        # exit game by pressing Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # each time we update, update the robot
        self.update_player()

        # update ingredients
        for i, v in enumerate(self.ingredients):
            self.ingredients[i] = self.update_ingredient(v)


    def update_player(self):
        # player can move left and right within certain bounds
        # check for key presses and update the player position accordingly
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, -8)
            self.player_dx = -1

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, GAME_W - 24)
            self.player_dx = 1

    def update_ingredient(self, ingredient):
        # for a given falling ingredient, see if it needs updating in some way
        # it can be collected, hit the floor, or remain falling

        # the tray position changes dependent on left/right movement (because of how the robot is drawn)
        # so the centre of the tray at any point is:
        tray_pos = self.player_x + I_SIZE*1.5 if self.player_dx > 0 else self.player_x + I_SIZE/2

        # if ingredient has not been collected and is at right position relative to tray, ingredient should be added to pizza
        # offset the ingredient so we track the centre of it instead of the top left
        if not ingredient.collected and abs(ingredient.x + I_SIZE/2 - tray_pos) < 16 and abs(ingredient.y + I_SIZE/2 - self.player_y) < 8:
            # add the ingredient kind to the pizza 
            self.update_pizza(ingredient.kind)

            # set this ingredient to having been collected
            ingredient.collected = True

            # play sound?


        # if ingredient has hit the floor, generate a new one
        if ingredient.y > I_LIMIT:
            ingredient = self.generate_ingredient()

        # otherwise, let the ingredient keep falling
        fall_speed = 1.2      # this could also be utilised for changing difficulty 
        ingredient.y += fall_speed

        return ingredient



    def update_pizza(self, kind):
        # this function is called whenever an ingredient is collected by the player

        # if a good ingredient is collected:
        if kind % 2 == 0:
            saved_score = self.score
            for obj in self.objectives:
                # if ingredient is one of our unfulfilled objectives:
                if kind == obj.kind and not obj.achieved:
                     # add the ingredient kind to our pizza (so that it can be drawn)
                        self.pizza.append(kind)

                        # update our objectives
                        obj.achieved = True

                        # increase the score by 1
                        self.score += 1

                        # if we collect a base, mark .is_base as True so no more bases are generated
                        if kind == 0:
                            self.is_base = True
                        
                        break       # exit loop once ingredient has been found
            
            # if score hasn't changed, we either collected an item that isn't part of our objectives or has already been collected
            if saved_score == self.score:
                # therefore, don't add it to the pizza and incur a strike
                self.strikes += 1

        # if bad ingredient is collected, empty pizza and add a strike. Also set is_base to False.
        else:
            self.pizza = []
            self.strikes += 1
            self.is_base = False


        # given our new pizza, check to see if objectives need updating
        self.update_objectives()


    def generate_ingredient(self):
        # improvement - good ingredients appear at a different frequency to bad ingredients using IngredientList class

        # x and y position for new ingredient
        x = pyxel.rndi(I_SIZE, GAME_W-I_SIZE)
        y = pyxel.rndi(-5*I_SIZE, -I_SIZE)  

        # if IL is empty then regenerate
        if not self.IL.items:
            self.IL = IngredientList(self.factor, I_NUMS_GOOD, I_NUMS_BAD)
        
        # if pizza has no base, we want to generate it and more frequently than normal
        if not self.is_base and pyxel.rndi(0,2) == 1:
            kind = 0        # randomly generate number between 0 and 3 and if it equals 1 then generate base

        # otherwise stick to regular order of ingredients
        else:
            kind = self.IL.items.pop()

        return Ingredient(kind, I_NAMES, x, y)


    def generate_objectives(self):
        # return a new list of Objective items which form a new pizza order
        # each pizza must include a base
        objectives = [Objective(0)] + [Objective(2*pyxel.rndi(1, len(I_NUMS_GOOD)-1)) for i in range(3)]

        #TODO: if sauce is included, this should come after base. Also need to enforce base/sauce collection before other toppings

        return objectives

    def update_objectives(self):
        # check to see whether our current objectives need changing

        # if order is complete then we want to create a new order:
        if all(obj.achieved for obj in self.objectives):
            # increase score by 5
            self.score += 5
            self.objectives = self.generate_objectives()
            # reset pizza
            self.pizza = []
            self.is_base = False

        # if we have 3 strikes, then we lose and need to start again
        if self.strikes == 3:
            self.strikes = 0
            self.score = 0
            self.objectives = self.generate_objectives()
            self.pizza = []
            self.is_base = False


    def draw(self):
        pyxel.cls(1)


        # draw background
        pyxel.bltm(0, 0, 0, 0, 0, 192, 128)
        
        # add animations:
        # fire:
        if pyxel.frame_count % 30 < 15:
            pyxel.blt(24, 80, 0, 24, 80, I_SIZE/2, I_SIZE/2)
            pyxel.blt(32, 80, 0, 24, 80, I_SIZE/2, I_SIZE/2)

        # smoke:
        if pyxel.frame_count % 50 < 10:
            pyxel.blt(24, 64, 0, 8, 96, I_SIZE/2, I_SIZE/2)
            pyxel.blt(32, 64, 0, 8, 96, I_SIZE/2, I_SIZE/2)

        # stars:
        if pyxel.frame_count % 100 < 10:
            pyxel.blt(48, 8, 0, 16, 64, I_SIZE/2, I_SIZE/2)
        if pyxel.frame_count % 100 > 40 and pyxel.frame_count % 100 < 50:
            pyxel.blt(96, 8, 0, 16, 72, I_SIZE/2, I_SIZE/2)
        if pyxel.frame_count % 100 > 80 and pyxel.frame_count % 100 < 90:
            pyxel.blt(168, 16, 0, 16, 72, I_SIZE/2, I_SIZE/2)


        # trains:
        self.animate_train(pyxel.frame_count, 500, 15)        

        # draw ingredients
        for ingredient in self.ingredients:
            if not ingredient.collected:
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

        for i, obj in enumerate(self.objectives):
            # draw text for objective
            pyxel.text(204, (i+1)*24, I_NAMES[obj.kind], 0)
            # draw icon for objective
            pyxel.blt(210, (i+1.2)*24, 1, (obj.kind % 4) * I_SIZE, pyxel.floor(obj.kind / 4) * I_SIZE, I_SIZE, I_SIZE, 1)
            
            # draw tick for correct ingredients in pizza
            if obj.achieved:
                pyxel.blt(210, (i+1.2)*24, 0, 0, 0, I_SIZE, I_SIZE, 1)



        # draw score
        outstr = "Score: " + str(self.score)
        pyxel.text(8, 8, outstr, 9)

        # draw number of strikes
        # rectangle in top right corner of game canvas
        pyxel.rect(GAME_W - I_SIZE*2 - 3, 1, I_SIZE*2+2, I_SIZE/2+2, 1)

        for i in range(self.strikes):
            pyxel.blt(GAME_W - I_SIZE*2 - 2 + 3*I_SIZE/4*i, 2, 0, I_SIZE, 0, I_SIZE/2, I_SIZE/2, 1)


    def animate_train(self, frame_count, freq = 1000, speed = 20):
        # draw the train going from left to right at a specified frequency and speed
        # speed here refers to how many frames in each position the train stays at, so the smaller the number the 'faster' the train
        # travels across the screen
            
            t = pyxel.floor(frame_count % freq / speed)
            match t:
                case 0:
                    pyxel.blt(136, 80, 0, 24, 48, I_SIZE/2, I_SIZE)

                case 1:
                    pyxel.blt(136, 80, 0, 24, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(144, 80, 0, 40, 48, I_SIZE/2, I_SIZE)

                case 2:
                    pyxel.blt(136, 80, 0, 24, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(144, 80, 0, 32, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(152, 80, 0, 40, 48, I_SIZE/2, I_SIZE)

                case 3:
                    pyxel.blt(136, 80, 0, 24, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(144, 80, 0, 32, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(152, 80, 0, 32, 48, I_SIZE/2, I_SIZE)

                case 4:
                    pyxel.blt(144, 80, 0, 32, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(152, 80, 0, 32, 48, I_SIZE/2, I_SIZE)

                case 5:
                    pyxel.blt(176, 80, 0, 40, 48, I_SIZE/2, I_SIZE)
                    pyxel.blt(152, 80, 0, 32, 48, I_SIZE/2, I_SIZE)

                case 6:
                    pyxel.blt(176, 80, 0, 32, 48, I_SIZE/2, I_SIZE)
                
                case 7:
                    pyxel.blt(176, 80, 0, 32, 48, I_SIZE/2, I_SIZE)
                
                case 8:
                    pyxel.blt(176, 80, 0, 40, 64, I_SIZE/2, I_SIZE)

                case _:
                    pass

App()    