import pyengine.game
# import pyengine.camera

class GameObject:
    def __init__(self):
        self.game: pyengine.game.Game = pyengine.game.Game.main()
        self.window = self.game.window
        self.camera = self.game.camera

    def update(self):
        pass

    def render(self):
        pass
