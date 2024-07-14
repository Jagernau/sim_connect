import json
from graphviz import Digraph

def create_graph(json_data, parent_node=None):
    graph = Digraph(format='pdf', engine='fdp')

    def traverse_json(data, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                node_name = f"{parent}.{key}" if parent else key
                graph.node(node_name)
                if parent:
                    graph.edge(parent, node_name)
                traverse_json(value, node_name)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                node_name = f"{parent}[{i}]" if parent else str(i)
                graph.node(node_name)
                if parent:
                    graph.edge(parent, node_name)
                traverse_json(item, node_name)

    traverse_json(json_data, parent_node)
    return graph

# Чтение файла JSON
with open('detail_tarif_id.json', 'r') as file:
    json_data = json.load(file)

# Создание графа
graph = create_graph(json_data)
graph.render('detail_tarif_graph')
