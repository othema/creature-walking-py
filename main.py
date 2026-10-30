import pygame
import pyengine

from src.scenes.main_scene import MainScene


def main():
    pygame.init()

    pygame.display.set_caption("game")
    window = pygame.display.set_mode((1500, 900), flags=pygame.RESIZABLE | pygame.SCALED)

    game = pyengine.Game(window)
    game.set_scene(MainScene)
    game._debug_open = True
    
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
