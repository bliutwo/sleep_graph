from parse_csv import CsvParser

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

DATES_KEY = 'Date'

def create_masked_array(numpyarray):
  mask = []
  for value in numpyarray:
    if value == np.nan:
      mask.append(0)
    else:
      mask.append(1)
  return ma.masked_array(numpyarray, mask=mask)

class DataGrapher:
  def __init__(self, data):
    self.data = data
  def graph(self):  
    dates = self.data[DATES_KEY]
    xpoints = np.array(dates)
    #xpoints = create_masked_array(xpoints)
    for label, list_of_points in self.data.items():
      if label != DATES_KEY:
        ypoints = np.array(list_of_points)
        #ypoints = create_masked_array(ypoints)
        plt.plot(xpoints, ypoints, label=label)
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
