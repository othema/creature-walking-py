import pygame
from time import time
from random import randint
from pyengine.game_object import GameObject
import pyengine.ui.space

from typing import Tuple


class Camera(GameObject):
  position = pygame.Vector2(0, 0)
  _shake_intensity = 0
  _shake_interval = 0
  _last_shaked = 0
  _end_shake = 0
  _offset = pygame.Vector2(0, 0)

  def rect(self, color, rect, width=0, radius=-1):
    position = self.adjust(rect)
    pygame.draw.rect(self.window, color, (position[0], position[1], rect[2], rect[3]), width, radius)

  def circle(self, color, center, radius, width=2):
    position = self.adjust(center)
    pygame.draw.circle(self.window, color, (int(position[0]), int(position[1])), radius, width)
  
  def line(self, color, start_pos, end_pos, width=1):
    start_pos = self.adjust(start_pos)
    end_pos = self.adjust(end_pos)
    pygame.draw.line(self.window, color, start_pos, end_pos, width)
  
  def blit(self, surface, position, space=pyengine.ui.space.Space.WORLD):
    if space == pyengine.ui.space.Space.WORLD:
      self.window.blit(surface, self.adjust(position))
    else:
      self.window.blit(surface, position)
  
  def adjust(self, position):
    return pygame.Vector2(
      position[0] - self.position.x + self._offset.x,
      position[1] - self.position.y + self._offset.y
    )

  def center_on(self, rect: Tuple[int, int, int, int] | pygame.Rect, lerp=1):
    pos = (rect[0] + rect[2]/2, rect[1] + rect[3]/2)
    self.position.x += ((pos[0] - self.window.get_width()/2) - self.position.x) / lerp
    self.position.y += ((pos[1] - self.window.get_height()/2) - self.position.y) / lerp

  def center_on(self, position: pygame.Vector2 | Tuple[int, int], lerp=1):
    self.position.x += ((position[0] - self.window.get_width()/2) - self.position.x) / lerp
    self.position.y += ((position[1] - self.window.get_height()/2) - self.position.y) / lerp
  
  def shake(self, intensity, interval, duration):
    self._shake_intensity = int(intensity)
    self._shake_interval = interval
    self._end_shake = time() + duration

  def get_mouse_pos(self, space=pyengine.ui.space.Space.SCREEN):
    mouse_pos = pygame.mouse.get_pos()
    if space == pyengine.ui.space.Space.WORLD:
      return pygame.Vector2(mouse_pos[0] + self.position.x, mouse_pos[1] + self.position.y)
    return pygame.Vector2(mouse_pos)
  
  def update(self):
    if self._shake_intensity > 0:
      if time() > self._last_shaked + self._shake_interval:
        self._last_shaked = time()
        self._offset.update(randint(-self._shake_intensity, self._shake_intensity),
                            randint(-self._shake_intensity, self._shake_intensity))
      
      if time() > self._end_shake:
        self._shake_intensity -= 1
    else:
      self._end_shake = 0
      self._offset.update(0, 0)
  
  def is_visible(self, rect):
    return pygame.Rect(*self.position, rect[2], rect[3]).colliderect(rect)
