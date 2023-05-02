from singleton import Singleton

# The ScoreCalculator class has the responsibility to 
# maintain the current score for the player playing the game.
class ScoreCalculator(metaclass=Singleton):
  def __init__(self):
    self.__score = 0

  @property
  def score(self):
    return self.__score

  @score.setter
  def score(self, value: int):
    self.__score = value
