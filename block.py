import pygame

class Block:
  def __init__(self):
    self.__sprite = None
    self.__x_pos = 0
    self.__y_pos = 0
    self.__speed = 0
    self.__hits_left = 1
    self.__point = 1
    self.__special_block = False
    self.__touching_ground = False

  @property
  def sprite(self):
    return self.__sprite

  @property
  def x_pos(self):
    return self.__x_pos

  @property
  def y_pos(self):
    return self.__y_pos

  @property
  def speed(self):
    return self.__speed

  @property
  def hits_left(self):
    return self.__hits_left

  @property
  def point(self):
    return self.__point

  @property
  def special_block(self):
    return self.__special_block

  @property
  def touching_ground(self):
    return self.__touching_ground

  @sprite.setter
  def sprite(self, value: pygame.surface.Surface):
    self.__sprite = value

  @x_pos.setter
  def x_pos(self, value: int):
    self.__x_pos = value

  @y_pos.setter
  def y_pos(self, value: int):
    self.__y_pos = value

  @speed.setter
  def speed(self, value: int):
    self.__speed = value

  @hits_left.setter
  def hits_left(self, value: int):
    self.__hits_left = value

  @point.setter
  def point(self, value: int):
    self.__point = value

  @special_block.setter
  def special_block(self, value: bool):
    self.__special_block = value

  @touching_ground.setter
  def touching_ground(self, value: bool):
    self.__touching_ground = value

  # def __repr__(self):
  #     return f"{self.__class__.__name__} (\
  #         {self.sprite}, {self.x_pos}, {self.y_pos} \
  #         {self.speed}, {self.hits_left}, {self.point}\
  #         {self.touching_ground}, {self.special_block})"
