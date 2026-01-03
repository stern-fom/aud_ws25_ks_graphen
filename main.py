import graphviz
from typing import Dict, List


def top_sort(dag: Dict[str, List[str]]):
    result = []
    in_degree = {node: 0 for node in dag}
    for node in dag:
        for successor in dag[node]:
            in_degree[successor] += 1

    to_process = [node for node in dag if in_degree[node] == 0]

    while to_process:
        node = to_process.pop(0)
        result.append(node)
        for successor in dag[node]:
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                to_process.append(successor)

    if len(result) != len(dag):
        raise ValueError("Graph is not acyclic!")

    return result


if __name__ == '__main__':
    dag = {
        "A": ["B", "C", "G", "F"],
        "B": [],
        "C": [],
        "D": [],
        "E": ["D"],
        "F": ["D", "E"],
        "G": ["C", "H"],
        "H": ["I"],
        "I": [],
        "J": ["G", "K", "L", "M"],
        "K": [],
        "L": ["G", "M"],
        "M": [],
    }
    dag_sorted = top_sort(dag)
    print(dag_sorted)
    graph = graphviz.Digraph(engine="dot")
    graph.attr("node", shape="circle")
    for node in dag:
        graph.node(node, label=node)
        for successor in dag[node]:
            graph.edge(node, successor)

    #graph.render(filename="graph.dot", format="png", view=True)

    top_sort_graph = graphviz.Digraph(engine="neato")
    top_sort_graph.attr(
        splines="curved",
        overlap="false",
        sep="+10")
    top_sort_graph.attr("node", shape="circle")

    # Force horizontal ordering with explicit positions
    spacing = 1.5
    for i, node in enumerate(dag_sorted):
        top_sort_graph.node(node, label=node, pos=f"{i*spacing},0!")

    # Add edges with port directions to route around nodes
    node_positions = {node: i for i, node in enumerate(dag_sorted)}
    edge_count = {}  # Count edges to alternate between top and bottom

    for node in dag_sorted:
        for successor in dag[node]:
            distance = abs(node_positions[successor] - node_positions[node])

            # For edges spanning multiple nodes, route via top or bottom
            if distance > 1:
                # Alternate between north (top) and south (bottom) routing
                key = (node, successor)
                count = edge_count.get(node, 0)
                edge_count[node] = count + 1

                if count % 2 == 0:
                    # Route via top
                    top_sort_graph.edge(node, successor, tailport="n", headport="n")
                else:
                    # Route via bottom
                    top_sort_graph.edge(node, successor, tailport="s", headport="s")
            else:
                # Direct connection for adjacent nodes
                top_sort_graph.edge(node, successor)

    top_sort_graph.render(filename="top_sort_graph.dot", format="png", view=True)
