import pyengine.game
import pygame


class Positions:
  @classmethod
  def _window(cls):
    return pyengine.game.Game.main().window

  @staticmethod
  def _padding(position, pl, pr, pt, pb):
    return (position[0] + pl - pr, position[1] + pt - pb)

  @staticmethod
  def _get_side_padding(p: int | tuple | pygame.Vector2):
    return p if type(p) in (tuple, pygame.Vector2) else (p, p)
  
  @staticmethod
  def topleft(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((0, 0), px, 0, py, 0)

  @staticmethod
  def top(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((Positions._window().get_width() // 2, 0), 0, 0, py, 0)

  @staticmethod
  def topright(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((Positions._window().get_width(), 0), 0, px, py, 0)
  
  @staticmethod
  def left(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((0, Positions._window().get_height() // 2), px, 0, 0, 0)
  
  @staticmethod
  def center(p: int | tuple | pygame.Vector2 = 0):
    return Positions._padding((Positions._window().get_width() // 2, Positions._window().get_height() // 2), 0, 0, 0, 0)
  
  @staticmethod
  def right(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((Positions._window().get_width(), Positions._window().get_height() // 2), 0, px, 0, 0)

  @staticmethod
  def bottomleft(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((0, Positions._window().get_height()), px, 0, 0, py)
  
  @staticmethod
  def bottom(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((Positions._window().get_width() // 2, Positions._window().get_height()), 0, 0, 0, py)
  
  @staticmethod
  def bottomright(p: int | tuple | pygame.Vector2 = 0):
    px, py = Positions._get_side_padding(p)
    return Positions._padding((Positions._window().get_width(), Positions._window().get_height()), 0, px, 0, py)
