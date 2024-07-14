from parse_csv import CsvParser

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

# https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
def nan_helper(y):
  """Helper to handle indices and logical indices of NaNs.

  Input:
      - y, 1d numpy array with possible NaNs
  Output:
      - nans, logical indices of NaNs
      - index, a function, with signature indices= index(logical_indices),
        to convert logical indices of NaNs to 'equivalent' indices
  Example:
      >>> # linear interpolation of NaNs
      >>> nans, x= nan_helper(y)
      >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
  """

  return np.isnan(y), lambda z: z.nonzero()[0]

DATES_KEY = 'date'

def create_numpy_mask(normal_data_list):
  mask = []
  for item in normal_data_list:
    #print(type(item))
    #print(item)
    if item < 0:
      mask.append(1)
    else:
      mask.append(0)
  print(mask)
  return mask

class DataGrapher:
  def __init__(self, data):
    self.data = data
  def graph(self):  
    dates = self.data[DATES_KEY]
    xpoints = np.array(dates)
    #xpoints = create_masked_array(xpoints)
    for label, list_of_points in self.data.items():
      if label != DATES_KEY:
        #ypoints = np.array(list_of_points)
        #mypoints = ma.masked_array(ypoints, mask=create_numpy_mask(list_of_points))
        ypoints = np.ma.array(list_of_points)
        ypointsmasked = np.ma.masked_where(ypoints < 0, ypoints)
        #print(ypoints)
        #ypoints = create_masked_array(ypoints)
        #plt.plot(xpoints, ypoints, label=label)
        #plt.plot(xpoints, mypoints, label=label)
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
