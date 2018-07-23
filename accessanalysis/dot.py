try:
    import graphviz as gv
except ImportError:
    gv = None

from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *


@cache_attr('dot')
def dot(graph: AccessGraph):
    if not gv:
        raise ImportError('graphviz was not imported, please re-run with graphviz imported to use dot functionality')

    d = gv.Digraph()
    for f in graph.files:
        d.node(f, fillcolor='ivory', style='filled')
    for u in graph.users:
        d.node(u, fillcolor='lightblue', style='filled')
    d.edges(graph.edges())
    return d
