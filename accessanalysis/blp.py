from typing import Dict, Set, List, Tuple, Optional

import itertools as it

from accessanalysis.find_invalid_access import invalid_access
from accessanalysis.compress import compress_graph
from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *


def get_level_id(i):
    """
    >>> get_level_id(0)
    'a'
    >>> get_level_id(26)
    'ba'
    """
    vocab = ord('z') - ord('a') + 1
    if i < vocab:
        return chr(i + ord('a'))
    return get_level_id(i // vocab) + get_level_id(i % vocab)


@cache_attr('BLP_mapping')
def blp(graph: AccessGraph):
    if invalid_access(graph) is not None:
        return False, 'there is invalid access in the graph', None  # if there is an invalid access there is no BLP

    try:
        eq = create_equal_groups(graph)
        mg = merge_groups(eq, graph)
        sg = sort_groups(mg, compress_graph(graph))
        as_ = assign(mg)
        return True, as_, sg
    except ValueError as e:
        return False, e.args[0], None


def create_equal_groups(graph: AccessGraph[str]) -> Dict[str, Set[str]]:
    equal_groups = {f:
                        frozenset(u for u in graph.users if graph.get(u, f) == 'rw-')
                    for f in graph.files}

    return equal_groups


def merge_groups(equal_groups: Dict[str, Set[str]], graph: AccessGraph) -> List[Tuple[str, Set[str]]]:
    for (f0, g0), (f1, g1) in it.combinations(equal_groups.items(), 2):
        if g0.intersection(g1) and g0 != g1:
            raise ValueError(f'two groups have non, trivial intersects for files {f0}, {f1}')
    # now we know that all same equality groups are equal
    ret = []
    for f, g in equal_groups.items():
        m_group = None
        if g:  # if g is empty it needs to be in a separate group
            for mg in ret:
                if g < mg:
                    m_group = mg
                    break
        if m_group is None:
            m_group = set(g)
            ret.append(m_group)

        m_group.add(f)
    for u in graph.users:
        if not any((u in g) for g in ret):
            ret.append({u})
    ret = [('lv-' + get_level_id(i), frozenset(s)) for (i, s) in enumerate(ret)]
    return ret


def sort_groups(merged_groups: List[Tuple[str, Set[str]]], compressed: Dict[Tuple[str, str], Optional[Tuple[str]]]):
    lt: Dict[str, List[str]] = {}  # y in lt[x] ==> x < y
    for (n0, g0), (n1, g1) in it.combinations(merged_groups, 2):
        (arb0, *_), (arb1, *_) = g0, g1
        order = False
        if compressed[arb0, arb1]:
            order = True
        elif compressed[arb1, arb0]:
            order = True
            (n0, g0), (n1, g1) = (n1, g1), (n0, g0)
        del arb0, arb1  # these might be flipped, so delete them for safety
        # we can be certain that if arb0 -> arb1 then all g0 -> g1 because:
        # * all g0 and all g1 are in rw states with each other
        # * there are no invalid accesses in the graph
        #
        # so if there were a x0 in g0 and x1 in g1 where x0 -/-> x1 then that would be an invalid access since
        # x0->arb0->arb1->x1
        if order:
            lt.setdefault(n0, [])
            lt[n0].append(n1)

    # now we need to check for transitivity
    for a, uppers in lt.items():
        for b in uppers:  # a < b
            for c in lt.get(b, ()):  # b < c
                if c not in uppers:  # a < c?
                    raise ValueError(f'non-transitive order between groups {a}, {b}, {c}')
    return lt


def assign(mg):
    ret = {}
    for n, g in mg:
        for i in g:
            ret[i] = n
    return ret
