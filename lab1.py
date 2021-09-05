from __future__ import annotations

import csv
from types import FunctionType
from typing import *

class Alternative:
    def __init__(self, variant: str, criteria: List[str], config: List[bool]):
        self.variant = variant
        self.criteria = criteria
        self.config = config
    
    def __init__(self, csv_row: List[str], config: List[bool]):
        self.variant = csv_row[0]
        self.criteria = csv_row[1:]
        self.config = config

    def __lt__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            rv = rv and self.criteria[i] < other.criteria[i]
        return rv

    def __eq__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            rv = rv and self.criteria[i] == other.criteria[i]
        return rv
    
    def __gt__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            rv = rv and self.criteria[i] > other.criteria[i]
        return rv

    def __le__(self, other: Alternative) -> bool:
        return self < other or self == other
        
    def __ge__(self, other: Alternative) -> bool:
        return self > other or self == other

    def __ne__(self, other: Alternative) -> bool:
        return not self == other

def parse_data(path: str) -> List[List[str]]:
    data : List[List[str]] = list()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def column_type(col: list) -> Type:
    try:
        for tried in col:
            _ = int(tried)
        return int
    except: pass
    try:
        for tried in col:
            _ = float(tried)
        return float
    except: pass
    return str

def make_alternatives(tabled_data: List[List[str]]) -> List[Alternative]:
    config = tabled_data[0]
    data = tabled_data[1:]
    types : List[Type] = list()
    for i in range(len(data[0])):
        col = [row[i] for row in data]
        types.append(column_type(col))
    alternatives: List[Alternative] = list()
    for row in data:
        for i in range(1, len(row)):
            row[i] = types[i](row[i])
        alternatives.append(Alternative(row, config))
    return alternatives

if __name__ == '__main__':
    make_alternatives(parse_data('lab1_data.csv'))
