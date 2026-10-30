from enum import Enum
import pygame


class Align(Enum):
  TOPLEFT = 0
  TOP = 1
  TOPRIGHT = 2
  LEFT = 3
  CENTER = 4
  RIGHT = 5
  BOTTOMLEFT = 6
  BOTTOM = 7
  BOTTOMRIGHT = 8


def align_rect(rect, alignment):
  new_rect = pygame.Rect(rect)

  if alignment == Align.TOPLEFT:
    pass
  elif alignment == Align.TOP:
    new_rect.centerx = new_rect.left
  elif alignment == Align.TOPRIGHT:
    new_rect.right = new_rect.left
  elif alignment == Align.LEFT:
    new_rect.centery = new_rect.top
  elif alignment == Align.CENTER:
    new_rect.center = new_rect.topleft
  elif alignment == Align.RIGHT:
    new_rect.centery = new_rect.top
    new_rect.right = new_rect.left
  elif alignment == Align.BOTTOMLEFT:
    new_rect.bottom = new_rect.top
  elif alignment == Align.BOTTOM:
    new_rect.bottom = new_rect.top
    new_rect.centerx = new_rect.left
  elif alignment == Align.BOTTOMRIGHT:
    new_rect.bottom = new_rect.top
    new_rect.right = new_rect.left

  return new_rect
