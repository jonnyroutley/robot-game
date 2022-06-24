import pyxel

class App:

    def __init__(self):
        pyxel.init(160, 120, title="Robo Pizza")
        pyxel.load("robo_pizza.py.pyxres")
        self.score = 0
        self.player_x = 80
        self.player_y = 0

        pyxel.run(self.update, self.draw)

    def update():
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def update_pizza():
        pass

    def update_ingredient():
        pass

    def update_player():
        pass

    def draw():
        pyxel.cls(0)
        pyxel.rect(10, 10, 20, 20, 11)


        # draw background

        # draw ingredient

        # draw player

        # draw score

App()