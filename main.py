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
    print(top_sort(dag))