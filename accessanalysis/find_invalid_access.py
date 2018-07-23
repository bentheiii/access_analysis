from accessanalysis.compress import compress_graph, gt_paths
from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *


@cache_attr('invalid_access')
def invalid_access(graph: AccessGraph):
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
    return shortest_invalid
