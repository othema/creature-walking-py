import pygame
from typing import Callable

import pyengine.game
import pyengine.ui.text_utils


def bar(value, max, rect: pygame.Rect, background_color, bar_color, text: Callable[[int | float, int | float], str] = None, font=None, font_size=16, align=0, space=0):
    surface = pygame.Surface(rect.size)
    new_rect = rect.copy()
    new_rect.topleft = pyengine.ui.text_utils.align_surf(align, surface, rect.topleft)

    if space == pyengine.Space.WORLD:
        new_rect.topleft = pyengine.game.Game.main().camera.adjust(new_rect.topleft)
    
    surface.fill(background_color)
    bar_width = int((value / max) * rect.width)
    surface.fill(bar_color, (0, 0, bar_width, rect.height))

    if text is not None:
        font = pyengine.ui.text_utils.get_font(font, font_size)
        text_surface = font.render(text(value, max), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(new_rect.width // 2, new_rect.height // 2))
        surface.blit(text_surface, text_rect)

    pyengine.game.Game.main().window.blit(surface, new_rect.topleft)


def bar_text(attribute_name):
    def _text(value, max):
        return f"{attribute_name}: {round(value)}/{round(max)}"
    return _text
