import pygame
import pyengine.game
import pyengine.ui.text_utils

cached = {}


def text(text, position, color=(255, 255, 255), size=24, font=None, align=0, background=None, space=0):
  font = pyengine.ui.text_utils.get_font(font, size)
  surface = font.render(str(text), True, color, background)

  new_pos = pyengine.ui.text_utils.align_surf(align, surface, position)
  if space == pyengine.Space.WORLD:
    new_pos = pyengine.game.Game.main().camera.adjust(new_pos)

  pyengine.game.Game.main().window.blit(surface, new_pos)
  return pygame.Rect(new_pos[0], new_pos[1], *surface.get_size())


def button(text, position, size=24, font=None, align=0, text_color=(0, 0, 0), bg_color=(255, 255, 255),
           hover_text_color=(0, 0, 0), hover_bg_color=(230, 230, 230), padding=4, space=0, width=None):
  
  font = pyengine.ui.text_utils.get_font(font, size)
  text_dimensions = list(font.size(str(text)))
  
  rect = pygame.Rect(0, 0, text_dimensions[0] + padding*2, text_dimensions[1] + padding*2)
  if width is not None:
    rect.w = width
  surface = pygame.Surface(rect.size)
  rect.topleft = pyengine.ui.text_utils.align_surf(align, surface, position)

  if space == pyengine.Space.WORLD:
    rect.topleft = pyengine.game.Game.main().camera.adjust(rect.topleft)
  hover = rect.collidepoint(pygame.mouse.get_pos())

  surface.fill(hover_bg_color if hover else bg_color)
  if width is not None:
    surface.blit(font.render(text, True, hover_text_color if hover else text_color), (rect.w/2 - text_dimensions[0]/2, padding))
  else:
    surface.blit(font.render(text, True, hover_text_color if hover else text_color), (padding, padding))

  pyengine.game.Game.main().window.blit(surface, rect.topleft)
  return hover and pyengine.game.Game.main().just_mouse_up
