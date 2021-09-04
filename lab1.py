import csv
from typing import *

class Alternative:
    def __init__(self, variant: str, criteria: List[str], config: List[bool]):
        self.variant = variant
        self.criteria = criteria
        self.config = config
    
    def __init__(self, csv_row: List[List[str]], config: List[bool]):
        self.variant = csv_row[0]
        self.criteria = csv_row[1:]
        self.config = config

def parse_data(path: str) -> List[List[str]]:
    data : List[List[str]] = list()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def make_alternatives(tabled_data: List[List[str]]) -> List[Alternative]:
    config = tabled_data[0]
    data = tabled_data[1:]
    alternatives: List[Alternative] = list()
    for row in data:
        alternatives.append(Alternative(row, config))
    return alternatives
