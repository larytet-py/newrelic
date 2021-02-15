"""
Please use Python3.

In this exercise you will implement the CSVFile class.
CSVFile receives a file stream as an input, the file is formatted as CSV.
The class should support the following:
- get_line: Returns the requested line as a dict
- get_iter: Returns an iterator starting at the input line
            (for more about iterators in python see:
             https://docs.python.org/3.7/glossary.html#term-iterator - or just use google)

*** Important note: The main usage for this class is to support large CSV files, it will be tested on a 20GB file.
    Take this into consideration when implementing the class and design the solution assuming you cannot simply keep
    all the file contents in memory. ***

To save time you should assume:
- The input file is always in CSV format with the ',' delimiter
- The first line contains the title name for each field
"""

import sys
from io import StringIO, IOBase
from typing import Dict, Iterator


class CSVFile(object):
    def __init__(self, file: IOBase):
        '''
        Read the whole file line by line
        Collect offsets of all lines in an array of lines
        '''
        self.file = file
        self.lines_offsets = []
        header = file.readline().strip()
        self.col_names = header.split(",")

        self.lines_offsets.append(0)
        while True:
            offset = file.tell()
            line = file.readline()
            if line == "":
                break
            self.lines_offsets.append(offset)

    def verify(self, line_number: int):
        if line_number >= len(self.lines_offsets):
            print(f"The {line_number} is too large")
            return False
        if line_number == 0:
            print(f"The {line_number} is a file header")
            return False
        return True

    def get_line(self, line_number: int) -> Dict:
        """Get a specific line in the CSV file
        Args:
            line_number: The line number (starting at 1, notice that 0 is the header row)
        Returns:
            A dictionary in which the keys are the column header (from the first row)
            and the values are the fields in the specific line.
        """
        if not self.verify(line_number):
            return {}
        offset = self.lines_offsets[line_number]
        self.file.seek(offset)
        line = self.file.readline().strip()
        values = line.split(",")

        d = dict(zip(self.col_names, values)) 
        return d

    def get_iter(self, line_number: int) -> Iterator[Dict]:
        """
        Returns an iterator starting at line_number in which every iteration returns the next line
        Args:
            line_number: The line number (strating at 1, notice that 0 is the titles row)
        Returns:
            A python iterator
        """
        pass


def main():
    with open(sys.argv[1], 'r') as f:
        csvFile = CSVFile(f)
        d = csvFile.get_line(3)
        print(d)

def example():
    """
    Simple example of what the implemented class should do
    """
    example_csv = """age,name,color
                     23, Dan, blue
                     33, Danny, purple
                     50, Danna, red
                     22, Barbra, grey
                     55, Moshik, white"""

    csv = StringIO(example_csv)

    csv_file = CSVFile(csv)
    assert csv_file.get_line(3) == {'age': '50', 'name': 'Danna', 'color': 'red'}

    for line in csv_file.get_iter(1):
        print(line)
        # Should print every line from the first one to the last as a dictionary.


if __name__ == "__main__":
    main()
