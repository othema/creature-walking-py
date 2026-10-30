import pygame
import pyengine.ui

cached = {}


def align_surf(alignment, surface, position):
  return pyengine.ui.align_rect((*position, *surface.get_size()), alignment).topleft


def get_font(name, size):
  cache_key = str(name) + ":" + str(size)
  if cache_key in cached:
    return cached[cache_key]
  else:
    font = pygame.font.Font(name, size)
    cached[cache_key] = font
    return font
