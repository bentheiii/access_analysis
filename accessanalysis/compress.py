import itertools as it
from typing import Dict, Tuple, Optional

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
    if graph.compressed:
        return graph.compressed
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
                new = add_paths(ret[f, step], ret[step, t])
                old = ret[f, t]
                if gt_paths(old, new):
                    ret[f, t] = new

    graph.compressed = ret
    return ret
