from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

import sys

def main():
  fall_asleep_times = [
    35,
    50,
    42,
    37,
    40,
    76,
    42,
    33,
    35,
    25,
    32,
    39,
    24,
    25,
    58,
    39,
    26,
  ]

  total_night_bedtimes = [
    240,
    420,
    240,
    554,
    617,
    584,
    560,
    571,
    608,
    540,
    447,
    613,
    595,
    641,
    559,
    543,
    543,
  ]

  wake_windows = [
    231,
    237,
    232,
    227,
    222,
    251,
    238,
    244,
    244,
    265,
    240,
    245,
    240,
    230,
    274,
    219,
    236,
  ]

  assert len(fall_asleep_times) == len(total_night_bedtimes) == len(wake_windows), f"\nlen(fall_asleep_times): {len(fall_asleep_times)}\nlen(total_night_bedtimes): {len(total_night_bedtimes)}\nlen(wake_windows): {len(wake_windows)}"

  print("lengths of lists of times are equal")

  n = len(fall_asleep_times)

  labels = [
    "Time to fall asleep",
    "Total Night Bedtime",
    "Wake Window Length",
  ]

  points_in_time = [i for i in range(n)]

  today = datetime.today()

  dates = []
  for i in range(n):
    dates.append((today - timedelta(days=i+1)).strftime('%m-%d'))

  dates = dates[::-1]
  print(dates)

  xpoints = np.array(dates)

  fall_asleep_times = [time / 60.0 for time in fall_asleep_times]
  total_night_bedtimes = [time / 60.0 for time in total_night_bedtimes]
  wake_windows = [time / 60.0 for time in wake_windows]

  for index, y_list_of_points in enumerate([fall_asleep_times, total_night_bedtimes, wake_windows]):
    ypoints = np.array(y_list_of_points)
    plt.plot(xpoints, ypoints, label=labels[index])
  plt.legend()
  plt.ylabel("Time in Hours")
  plt.title("Natalie's Sleep Over Time")
  plt.xticks(rotation=45, ha="right")
  plt.show()

if __name__ == "__main__":
  sys.exit(main())
