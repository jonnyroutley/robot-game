import pyxel

# GLOBAL VARS



class App:

    def __init__(self):
        pyxel.init(192, 128, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")
        self.score = 0
        self.player_x = 85
        self.player_y = 92
        self.player_dx = 0
        self.is_alive = True

        # ingredient = (x, y, kind, is_alive)
        # when the game starts, generate some ingredients that are spread horizontally and vertically
        num_ingredients = 4
        self.ingredients = [
            self.generate_ingredient() for i in range(num_ingredients)
        ] 


        # music playm
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        for i, v in enumerate(self.ingredients):
            self.ingredients[i] = self.update_ingredient(*v)


    def update_pizza():
        pass

    def generate_ingredient(self):
        num_types = 9
        return (pyxel.rndi(8, pyxel.width-8), pyxel.rndi(-70, -10), pyxel.rndi(0, num_types), True)


    def update_ingredient(self, x, y, kind, is_alive):
        # need some terminal condition
        # if is_alive and abs()

        y += 1

        if y > 100:
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
        pyxel.blt(0, 0, 0, 0, 16, 192, 128)

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
            160,
            32,
            32,
            1
        )

        # draw score

App()