import pyxel

# GLOBAL VARS
I_SIZE = 16      # ingredient block size
WIDTH = 192     # window width
HEIGHT = 128    # window height
I_LIMIT = 110    # height at which ingredients should disappear

#TODO: make real use of global vars - go through and try to remove magic nums
# update objectives
# draw pizzas


# Ordered list of ingredients for converting 'kind' integer to name
I_LIST = ['Pizza Base', 'Rotten Egg', 'Mushroom', 'Wasabi', 'Aubergine', 'Hammer', 'Swiss Cheese', 
            'Stinky Socks', 'Pepperoni', 'Fish Carcass', 'Mozzarella', 'A... Nose?', 'Tomato Sauce']

I_LIST_GOOD = [item for i, item in enumerate(I_LIST) if i % 2 == 0]

class Ingredient:

    def __init__(self, kind, x = 0, y = 0):
        self.x = x
        self.y = y
        self.kind = kind
        self.name = I_LIST[kind]
        self.is_alive = True
        self.is_good = True if kind % 2 == 0 else False


class App:

    def __init__(self):
        pyxel.init(WIDTH + 64, HEIGHT, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")
        # starting conditions
        self.score = 0
        self.player_x = 85
        self.player_y = 92
        self.player_dx = 0      #dx is used to indicate last used direction of travel
        self.is_alive = True
        # checks if there is a pizza base already
        self.is_base = False

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

        # check to see if there is a pizza base already - if so, do not generate more
        start_types = 1 if self.is_base else 0
        num_types = 12
        x = pyxel.rndi(I_SIZE, WIDTH-I_SIZE)
        y = pyxel.rndi(-5*I_SIZE, -I_SIZE)  
        kind = pyxel.rndi(start_types, num_types)

        return Ingredient(kind, x, y)


    def update_ingredient(self, ingredient):
        # need some terminal condition
        # if ingredient is 'alive' and is at right position relative to tray, ingredient should be added to pizza
        if ingredient.is_alive and abs(ingredient.x - (self.player_x + 16)) < 16 and abs(ingredient.y - self.player_y) < 8:
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
            self.player_x = min(self.player_x + 2, WIDTH - 24)
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
                pyxel.blt(ingredient.x, ingredient.y, 1, (ingredient.kind % 4) * 16, pyxel.floor(ingredient.kind / 4) * 16, 16, 16, 1)



        # draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0 if self.player_dx < 0 else 32, 
            16,
            32,
            32,
            1
        )

        # draw objectives
        pyxel.bltm(192, 0, 0, 192, 0, 64, 128)
        pyxel.text(204, 6, "Order's Up!", 0)

        for i, ingredient in enumerate(self.objectives):
            pyxel.text(204, (i+1)*24, ingredient.name, 0)
            if ingredient.kind in self.pizza:
                pyxel.blt(210, (i+1.2)*24, 1, (ingredient.kind % 4) * 16, pyxel.floor(ingredient.kind / 4) * 16, 16, 16, 1)
                pyxel.blt(210, (i+1.2)*24, 0, 0, 0, 16, 16, 1)

            else:
                pyxel.blt(210, (i+1.2)*24, 1, (ingredient.kind % 4) * 16, pyxel.floor(ingredient.kind / 4) * 16, 16, 16, 1)

        # draw score
        outstr = "Score: " + str(self.score)
        pyxel.text(8, 8, outstr, 9)

App()