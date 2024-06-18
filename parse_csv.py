import argparse
import json
import re
import sys

class CsvParser:
  def __init__(self, filename):
    self.column_handler = None
    with open(filename, 'r') as f:
      for index, line in enumerate(f):
        line = line.replace('\n', '')
        line_list = line.split(',')
        if index == 0:
          index_to_column_label = {index: label for index, label in enumerate(line_list)}
          self.column_handler = ColumnHandler(index_to_column_label)
        else:
          assert self.column_handler
          for i, item in enumerate(line_list):
            self.column_handler.add(i, item)
    self.column_handler.do_conversions()
  def get_data(self):
    return self.column_handler.get_items()

class ColumnHandler:
  def __init__(self, index_to_column_label):
    self.index_to_column_label = index_to_column_label
    self.column_label_to_list_of_values = self._create_column_label_to_list_of_values()
  def _create_column_label_to_list_of_values(self):
    d = {}
    for index, label in self.index_to_column_label.items():
      d[label] = []
    return d
  def add(self, index, value):
    label = self.index_to_column_label[index]
    self.column_label_to_list_of_values[label].append(value)
  def _needs_conversion(self, list_of_values):
    for item in list_of_values:
      if 'm' in item:
        return True
    return False
  def _convert_list(self, list_of_values):
    final_list_of_values = []
    list_of_values = [item.replace('min', 'm') for item in list_of_values]
    for raw_time_string in list_of_values:
      x = re.search("(\d+)?h?(\d+)?m?", raw_time_string)
      final_value = 0
      if x.group(1) is None or x.group(2) is None:
        # If they are both none, do nothing
        if x.group(1) is None and x.group(2) is None:
          continue
        # One of h or m is missing
        if 'h' in raw_time_string:
          # We're only looking at hour times
          final_value = int(x.group(1)) * 60
        else:
          # We're only looking at minute times
          final_value = int(x.group(1))
      else:
        hours = int(x.group(1))
        minutes = int(x.group(2))
        final_value = (hours * 60) + minutes
      final_list_of_values.append(final_value)
    final_list_of_values = [minutes / 60.0 for minutes in final_list_of_values]
    return final_list_of_values
  def do_conversions(self):
    for label, list_of_values in self.column_label_to_list_of_values.items():
      if self._needs_conversion(list_of_values):
        new_list_of_values = self._convert_list(list_of_values)
        self.column_label_to_list_of_values[label] = new_list_of_values
  def print_items(self):
    print(json.dumps(self.column_label_to_list_of_values, indent=2))
  def get_items(self):
    return self.column_label_to_list_of_values

def main():
  parser = argparse.ArgumentParser(
    prog='csv_parser',
    description='parses the csv given')
  parser.add_argument('filename')
  args = parser.parse_args()
  print(f"Filename: {args.filename}")
  csv_parser = CsvParser(args.filename)
  csv_parser.get_data()

if __name__ == "__main__":
  sys.exit(main())