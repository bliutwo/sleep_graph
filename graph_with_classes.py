from parse_csv import CsvParser

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np

DATES_KEY = 'date'

class DataGrapher:
  def __init__(self, data):
    self.data = data
  def graph(self):  
    dates = self.data[DATES_KEY]
    xpoints = np.array(dates)
    for label, list_of_points in self.data.items():
      if label != DATES_KEY:
        ypoints = np.ma.array(list_of_points)
        ypointsmasked = np.ma.masked_where(ypoints < 0, ypoints)
        plt.plot(xpoints, ypointsmasked, label=label)
    plt.legend()
    plt.ylabel("Time in Hours")
    plt.title("Natalie's Sleep Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.show()

def main():
  parser = argparse.ArgumentParser(
    prog='graph with classes',
    description='parse the csv given and make a graph')
  parser.add_argument('filename')
  args = parser.parse_args()
  print(f"Filename: {args.filename}")
  csv_parser = CsvParser(args.filename)
  data = csv_parser.get_data()
  data_grapher = DataGrapher(data)
  data_grapher.graph()

if __name__ == "__main__":
  sys.exit(main())
