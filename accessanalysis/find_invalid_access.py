from accessanalysis.compress import compress_graph, gt_paths
from accessanalysis.graph import AccessGraph


def find_invalid_access(graph: AccessGraph):
    compressed = compress_graph(graph)
    shortest_invalid = None
    for (f, t), v in compressed.items():
        if v is None:
            continue
        if (f in graph.users) == (t in graph.users):
            continue  # we are not interested in file-file or user-user connections
        if graph[f, t]:
            continue
        if gt_paths(shortest_invalid, v):
            shortest_invalid = v
    graph.invalid_access = shortest_invalid
    return shortest_invalid
