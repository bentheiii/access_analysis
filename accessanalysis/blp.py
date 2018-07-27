from accessanalysis.compress import compress_graph, gt_paths
from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *
import itertools as it


@cache_attr('blp')
def blp(graph: AccessGraph):
    equal_groups = create_equal_groups(graph)
    pass

def create_equal_groups(graph):
    compressed = compress_graph(graph)

    equal_groups = []

    for n in graph.nodes():
        temp_group = [n]
        equal_groups.append(temp_group)
        for group in equal_groups:
            if n in group:
                if group == temp_group:
                    continue
                equal_groups.remove(temp_group)
                temp_group = group

        for m in graph.nodes():
            if n == m:
                continue
            elif (n in graph.users) == (m in graph.users):
                continue  # we are not interested in file-file or user-user connections
            elif compressed[n, m] and compressed[m, n]:
                if m not in temp_group:
                    temp_group.append(m)

    return equal_groups
