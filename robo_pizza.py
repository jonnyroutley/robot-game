import pyxel

class App:

    def __init__(self):
        pyxel.init(192, 128, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")
        self.score = 0
        self.player_x = 80
        self.player_y = 92
        self.player_dx = 0
        self.is_alive = True

        # music playm
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()


    def update_pizza():
        pass

    def update_ingredient():
        pass

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

        # draw ingredient

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