from leaderboard import Score

class ScoreCalculator:
  def __init__(self):
    self.__score = 0
    
  @property
  def score(self):
    return self.__score
  
  @score.setter
  def score(self, value: int):
    self.__score = value