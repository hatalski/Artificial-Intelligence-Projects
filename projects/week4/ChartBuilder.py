import pandas as pd
import matplotlib.pyplot as plt
import time

class ChartBuilder():
  def __init__(self):
    self.df = None
  
  def setup(self, dict):
    self.df = pd.DataFrame(dict)

  def draw(self):
    self.df.plot()
    plt.show()
    
  def save_to_csv(self):
    self.df.to_csv("_moves_" + str(time.time()) + ".csv")
