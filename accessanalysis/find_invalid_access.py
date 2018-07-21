from typing import Dict, Tuple, Optional, List

import itertools as it

from accessanalysis.graph import AccessGraph


def add_paths(a, b):
    if None in (a, b):
        return None
    return a + b[1:]


def gt_paths(old, new):
    if new is None:
        return False
    if old is None:
        return True
    return len(old).__gt__(len(new))


def compress_graph(graph: AccessGraph) -> Dict[Tuple[str, str], Optional[Tuple[str]]]:  # floyd-warshall
    nodes = graph.nodes()
    ret = {(f, t): None for f, t in it.product(nodes, repeat=2)}
    for f, t in ret:
        if f == t:
            ret[f, t] = (f,)
        elif graph[f, t]:
            ret[f, t] = (f, t)

    for step in nodes:
        for f in nodes:
            for t in nodes:
                new = add_paths(ret[f,step], ret[step,t])
                old = ret[f,t]
                if gt_paths(old,new):
                    ret[f,t] = new

    return ret

def find_invalid_access(graph: AccessGraph):
    compressed = compress_graph(graph)
    shortest_invalid = None
    for (f,t),v in compressed.items():
        if v is None:
            continue
        if (f in graph.users) == (t in graph.users):
            continue  # we are not interested in file-file or user-user connections
        if graph[f,t]:
            continue
        if gt_paths(shortest_invalid, v):
            shortest_invalid = v
    graph.invalid_access = shortest_invalid
    return shortest_invalid
