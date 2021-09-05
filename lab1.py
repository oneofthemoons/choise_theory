from __future__ import annotations

import csv
from types import FunctionType
from typing import *

class Alternative:
    def __init__(self, id: int, variant: str, criteria: List[str], config: List[bool]):
        self.variant = variant
        self.criteria = criteria
        self.config = config
        self.id = id
    
    def __init__(self, id: int, csv_row: List[str], config: List[bool]):
        self.variant = csv_row[0]
        self.criteria = csv_row[1:]
        self.config = config
        self.id = id

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
    id = 1
    for row in data:
        for i in range(1, len(row)):
            row[i] = types[i](row[i].strip())
        alternatives.append(Alternative(id, row, config))
        id += 1
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

def make_criteria_filters(criteria: List[str]) -> List[Tuple[int, str, Any]]:
    print("Идентификаторы критериев:")
    n_zeros = len(str(len(criteria)))
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    id = 0
    for c in criteria:
        print(f"{alphabet[id]}: {c}")
        id += 1
    print()
    print("Введите границы критериев в следующем формате (без скобок):")
    print("[идентификатор критерия][знак сравнения < или >][значение]")
    print("Например, несколько критериев можно ввести через пробел: c>12000 d<9")
    ans = input().split()
    filters = list()
    for filter in ans:
        op_pos = max(filter.find('>'), filter.find('<'))
        id = alphabet.index(filter[:op_pos])
        op = filter[op_pos]
        val = filter[op_pos + 1:]
        try:
            val = int(val)
        except:
            val = float(val)
        filters.append((id, op, val))
    return filters

def make_filtered(alternatives: List[Alternative], filters :List[Tuple[int, str, Any]]):
    new_alternatives = list()
    for alternative in alternatives:
        filtered = False
        for filter in filters:
            if filter[1] == '>' and alternative.criteria[filter[0]] <= filter[2]:
                filtered = True
            if filter[1] == '<' and alternative.criteria[filter[0]] >= filter[2]:
                filtered = True
        if not filtered:
            new_alternatives.append(alternative)
    return new_alternatives

def print_alternative_ids(alternatives: List[Alternative]) -> None:
    print("Идентификаторы альтернатив:")
    n_zeros = len(str(len(alternatives)))
    for alternative in alternatives:
        print(f"{str(alternative.id).zfill(n_zeros)}: {alternative.variant}")

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

def print_set(alternatives: List[Alternative]):
    print("{ ", end='')
    print(', '.join(alternative.variant for alternative in alternatives), end='')
    print(' }')

def print_Paretho_set(alternatives: List[Alternative], idx_set: Set[int]) -> None:
    print("Парето-оптимальное множество решений:")
    print_set([alternatives[alt_idx] for alt_idx in make_Paretho_idx_set(eqt)])

if __name__ == '__main__':
    data_table = parse_data('lab1_data.csv')
    alternatives = make_alternatives(data_table)
    print_alternative_ids(alternatives)
    print()
    eqt = make_equaling_table(alternatives)
    print_equaling_table(eqt)
    print()
    print_Paretho_set(alternatives, make_Paretho_idx_set(eqt))
    print()
    ans = input('Хотите ли вы указать верхние/нижние границы критериев [Д/н]')
    if any(c in ans for c in 'YyДд'):
        filters = make_criteria_filters(data_table[0][1:])
        alternatives = make_filtered(alternatives, filters)
        print("Альтернативы отфильтрованы.")
        print_alternative_ids(alternatives)
        print()
        print("Текущее множество решений:")
        print_set(alternatives)
