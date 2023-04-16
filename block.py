import pygame


class Block:
  def __init__(self):
    self.sprite = None
    self.x_pos = 0
    self.y_pos = 0
    self.speed = 0
    self.hits_left = 1
    self.point = 1
    self.special_block = False
    self.touching_ground = False

  @property
  def sprite(self):
    return self.sprite

  @property
  def x_pos(self):
    return self.x_pos

  @property
  def y_pos(self):
    return self.y_pos

  @property
  def speed(self):
    return self.speed

  @property
  def hits_left(self):
    return self.hits_left

  @property
  def point(self):
    return self.point

  @property
  def special_block(self):
    return self.special_block

  @property
  def touching_ground(self):
    return self.touching_ground

  @sprite.setter
  def sprite(self, value: pygame.surface.Surface):
    self.sprite = value

  @x_pos.setter
  def x_pos(self, value: int):
    self.x_pos = value
    
  @y_pos.setter
  def y_pos(self, value: int):
    self.y_pos = value
    
  @speed.setter
  def speed(self, value: int):
    self.speed = value
    
  @hits_left.setter
  def hits_left(self, value: int):
    self.hits_left = value
    
  @point.setter
  def point(self, value: int):
    self.point = value
    
  @special_block.setter
  def special_block(self, value: bool):
    self.special_block = value
    
  @touching_ground.setter
  def touching_ground(self, value: bool):
    self.touching_ground = value 
