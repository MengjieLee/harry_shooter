import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.y = 0
        pyxel.run(self.update, self.draw)

    def __del__(self):
        pass

    def update(self):
        self.y = (self.y + 1) % pyxel.width
        print(self.y)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, self.y, 8, 8, 9)

App()
