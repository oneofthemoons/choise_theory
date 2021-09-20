import csv
import copy

from numpy import mat

import networkx as nx
import matplotlib.pyplot as plt

def get_criteria(path):
    criteria = dict()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = True
        for row in reader:
            if header:
                header = False
                continue
            criteria[row[0]] = { "weight": int(row[1]), "to": row[-1] }
    return criteria

def get_data(path, criteria):
    data = list()
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = True
        col_names = []
        for row in reader:
            if header:
                header = False
                col_names = row
                continue
            data.append(dict({ 'name': row[0], 'criteria': copy.deepcopy(criteria) }))
            for i in range(1, len(row)):
                data[-1]['criteria'][col_names[i]]["value"] = float(row[i])
    return data

def get_preference_matrix(data):
    matrix = [['-' for _ in range(len(data))] for _ in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                matrix[i][j] = 'x'
                continue
            p = 0
            n = 0
            for key in data[i]['criteria'].keys():
                l = data[i]['criteria'][key]
                r = data[j]['criteria'][key]
                w = l['weight']
                if l['value'] > r['value']:
                    if l['to'] == 'max':
                        p += w
                    else:
                        n += w
                elif l['value'] < r['value']:
                    if l['to'] == 'min':
                        p += w
                    else:
                        n += w
            if n == 0:
                matrix[i][j] = 'inf'
            elif p / n > 1:
                matrix[i][j] = round(p / n, 1)
    return matrix

def print_preference_matrix(matrix):
    print("Таблица предпочтений:")
    idx = 0
    print('\t'.join(map(str, list(range(len(matrix) + 1)))))
    for row in matrix:
        idx += 1
        pretty = [str(idx)]
        pretty.extend(row)
        print('\t'.join(map(str,pretty)))
    return matrix

def get_layer(id, matrix, was = set()):
    layer = 0
    if id in was:
        return layer
    was.add(id)
    for i in range(len(matrix)):
        if type(matrix[i][id]) == float:
            layer = max(layer, layer + get_layer(i, matrix, copy.deepcopy(was)) + 1)
    return layer
    


def draw_preference_graph(matrix):
    graph = nx.DiGraph(directed=True)
    for i in range(len(matrix)):
        showed = False
        for col in matrix[i]:
            if type(col) == float:
                showed = True
                break
        if showed:
            graph.add_node(str(i + 1))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if type(matrix[i][j]) == float:
                graph.add_edge(str(i + 1), str(j + 1), weight=matrix[i][j])
    options = {
        'node_color': 'red',
        'node_size': 300,
        'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    pos = nx.spring_layout(graph)
    pos_x_on_layer = [(150 if i % 2 == 0 else 0) for i in range(len(pos))]
    for node in pos:
        layer = get_layer(int(node) - 1, matrix)
        shift_y_on_layer = 0
        if pos_x_on_layer[layer] % 2000 == 0:
            shift_y_on_layer = 150
        pos[node] = (pos_x_on_layer[layer], layer * 1000 + shift_y_on_layer)
        pos_x_on_layer[layer] += 1000
    nx.draw_networkx(graph, pos, arrows=True, **options)
    plt.draw()
    plt.show()
    

if __name__ == '__main__':
    draw_preference_graph(
        print_preference_matrix(
            get_preference_matrix(
                get_data(
                    'lab2_data.csv',
                    get_criteria(
                        'lab2_criteria.csv'
                    )
                )
            )
        )
    )
