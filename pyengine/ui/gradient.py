import pygame
from enum import Enum


class Direction(Enum):
  HORIZONTAL = 0
  VERTICAL = 1


def gradient(size, from_color, to_color, direction=Direction.HORIZONTAL):
  surface = pygame.Surface(size, pygame.SRCALPHA)
  surface.fill(from_color)
  if direction == Direction.HORIZONTAL:
    for i in range(0, size[0]):
      surface.fill(_lerp(from_color, to_color, i / size[0]), (i, 0, 1, size[1]))
  elif direction == Direction.VERTICAL:
    for i in range(0, size[1]):
      surface.fill(_lerp(from_color, to_color, i / size[1]), (0, i, size[0], 1))

  return surface


def _lerp(color1, color2, amount):
  return (
    int(color1[0] + (color2[0] - color1[0]) * amount),
    int(color1[1] + (color2[1] - color1[1]) * amount),
    int(color1[2] + (color2[2] - color1[2]) * amount),
    int(color1[3] + (color2[3] - color1[3]) * amount) if len(color1) == 4 and len(color2) == 4 else 255
  )
