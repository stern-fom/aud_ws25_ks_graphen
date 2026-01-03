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

    top_sort_graph = graphviz.Digraph(engine="dot")
    top_sort_graph.attr(
        rankdir="TB",
        splines="curved",
        nodesep="1.0",
        ranksep="2.0",
        overlap="false")
    top_sort_graph.attr("node", shape="circle", width="0.8", height="0.8")

    # Force strict horizontal ordering by creating explicit rank constraints
    for i, node in enumerate(dag_sorted):
        top_sort_graph.node(node, label=node, pos=f"{i},0!")
        #top_sort_graph.node(node, label=node, rank="same")

    # Add edges AFTER nodes to ensure proper routing
    for node in dag_sorted:
        for successor in dag[node]:
            top_sort_graph.edge(node, successor,
                                constraint="false",
                                tailport="n",
                                headport="n")

    top_sort_graph.render(filename="top_sort_graph.dot", format="png", view=True)
