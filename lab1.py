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
            lt_crit = self.criteria[i] < other.criteria[i] and self.config[i] \
                or self.criteria[i] > other.criteria[i] and not self.config[i]
            rv = rv and lt_crit
        return rv

    def __eq__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            rv = rv and self.criteria[i] == other.criteria[i]
        return rv
    
    def __gt__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            gt_crit = self.criteria[i] > other.criteria[i] and self.config[i] \
                or self.criteria[i] < other.criteria[i] and not self.config[i]
            rv = rv and gt_crit
        return rv

    def __le__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            gt_crit = self.criteria[i] <= other.criteria[i] and self.config[i] \
                or self.criteria[i] >= other.criteria[i] and not self.config[i]
            rv = rv and gt_crit
        return rv
        
    def __ge__(self, other: Alternative) -> bool:
        rv = True
        for i in range(len(self.criteria)):
            gt_crit = self.criteria[i] >= other.criteria[i] and self.config[i] \
                or self.criteria[i] <= other.criteria[i] and not self.config[i]
            rv = rv and gt_crit
        return rv

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
    config = list(map(lambda s: '+' in s, tabled_data[0][1:]))
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

def make_equaling_table(alts: List[Alternative]) -> List[List[str]]:
    table: List[List[str]] = [['' for _ in range(len(alts))] for __ in range(len(alts))]
    for i in range(len(alts)):
        for j in range(len(alts)):
            if j >= i:
                table[i][j] = 'X'
            elif alts[i] >= alts[j]:
                table[i][j] = f'A{i + 1}'
            elif alts[i] < alts[j]:
                table[i][j] = f'A{j + 1}'
            else:
                table[i][j] = 'H'
    return table

def make_Paretho_idx_set(eqt: List[List[str]]) -> Set[int]:
    rv = set()
    for row in eqt:
        for e in row:
            if e.startswith('A'):
                rv.add(int(e[1:]) - 1)
    return rv

def print_alternative_ids(alternatives: List[Alternative]) -> None:
    print("Идентификаторы альтернатив:")
    id = 1
    n_zeros = len(str(len(alternatives)))
    for alternative in alternatives:
        print(f"{str(id).zfill(n_zeros)}: {alternative.variant}")
        id += 1

def print_equaling_table(eqt: List[List[str]]) -> None:
    print("Таблица попарных сравнений:")
    sz_col = max(len(str(len(eqt))), max(map(lambda row: max(map(len, row)), eqt)))
    col_formatter = "{:_^" + str(sz_col) + "}"
    for _ in range(len(eqt) + 1):
        print('_' + col_formatter.format(''), end='')
    print('_')
    print('|' + col_formatter.format(''), end='')
    for id in range(1, len(eqt) + 1):
        print('|' + col_formatter.format(str(id)), end='')
    print('|')
    id = 1
    for row in eqt:
        print('|' + col_formatter.format(str(id)), end='')
        for e in row:
            print('|' + col_formatter.format(e), end='')
        print('|')
        id += 1

def print_Paretho_set(alternatives: List[Alternative], idx_set: Set[int]) -> None:
    print("Парето-оптимальное множество решений:")
    print("{ ", end='')
    print(', '.join([alternatives[alt_idx].variant for alt_idx in make_Paretho_idx_set(eqt)]), end='')
    print(' }')

if __name__ == '__main__':
    alternatives = make_alternatives(parse_data('lab1_data.csv'))
    
    print_alternative_ids(alternatives)
    print()
    eqt = make_equaling_table(alternatives)
    print_equaling_table(eqt)
    print()
    print_Paretho_set(alternatives, make_Paretho_idx_set(eqt))

