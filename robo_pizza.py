import pyxel

# GLOBAL VARS
I_SIZE = 16      # ingredient block size
WIDTH = 192     # window width
HEIGHT = 128    # window height
I_LIMIT = 100    # height at which ingredients should disappear

# Ordered list of ingredients for converting 'kind' integer to name
I_LIST = ['Pizza Base', 'Rotten Egg', 'Mushroom', 'Wasabi', 'Tomato', 'Aubergine', 'Hammer', 
            'Swiss Cheese', 'Stinky Socks', 'Pepperoni', 'Fish Carcass', 'Mozzarella', 'A... Nose?', 'Tomato Sauce']


class App:

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Robo Pizza")
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

        # ingredient = (x, y, kind, is_alive)
        # when the game starts, generate some ingredients that are spread horizontally and vertically
        num_ingredients = 3
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
            self.ingredients[i] = self.update_ingredient(*v)


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
        return (pyxel.rndi(I_SIZE, pyxel.width-I_SIZE), pyxel.rndi(-5*I_SIZE, -I_SIZE), pyxel.rndi(start_types, num_types), True)


    def update_ingredient(self, x, y, kind, is_alive):
        # need some terminal condition
        # if ingredient is 'alive' and is at right position relative to tray, ingredient should be added to pizza
        if is_alive and abs(x - (self.player_x + 16)) < 16 and abs(y - self.player_y) < 12:
            is_alive = False
            # play sound?

            # add ingredient to pizza and update score
            self.update_pizza(kind)

        fall_speed = 1
        y += fall_speed

        # if ingredient hits the floor, generate a new one
        if y > I_LIMIT:
            x, y, kind, is_alive = self.generate_ingredient()

        return (x, y, kind, is_alive)

    def update_player(self):

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, -8)
            self.player_dx = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 24)
            self.player_dx = 1



    def draw(self):
        pyxel.cls(1)

        # draw background
        pyxel.bltm(0, 0, 0, 0, 0, 192, 128)

        # draw ingredients
        for x, y, kind, is_alive in self.ingredients:
            if is_alive:
                pyxel.blt(x, y, 1, (kind % 4) * 16, pyxel.floor(kind / 4) * 16, 16, 16, 1)



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

        # draw score
        outstr = "Score: " + str(self.score)
        pyxel.text(8, 8, outstr, 9)

App()