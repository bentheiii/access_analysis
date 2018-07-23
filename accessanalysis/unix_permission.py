from typing import Dict

from collections import namedtuple

from accessanalysis.graph import AccessGraph
from accessanalysis.__util import *

UNIXPermission = namedtuple('UNIXPermission', 'owner_perm group_perm other_perm group owner')


def _get_unix_perm(file, graph) -> UNIXPermission:
    permission_groups = {}
    for u in graph.users:
        perms = graph.get(u, file)
        if perms in permission_groups:
            permission_groups[perms].add(u)
        else:
            permission_groups[perms] = {u}
    if len(permission_groups) > 3:
        raise ValueError(f'file {file} has more than three distinct access rights')
    if len(permission_groups) == 0:
        return UNIXPermission('---', '---', '---', set(), '<root>')
    if len(permission_groups) == 1:
        (perm, users), = permission_groups.items()
        arb_user = next(iter(users))
        return UNIXPermission(perm, perm, perm, {arb_user}, arb_user)
    permission_groups = sorted(permission_groups.items(), key=lambda x: len(x[1]))
    if len(permission_groups) == 2:
        (perm0, users0), (perm1, users1) = permission_groups
        return UNIXPermission(perm0, perm0, perm1, users0, next(iter(users0)))
    (o_perm, owner), (g_perm, group), (r_perm, rest) = permission_groups
    if len(owner) > 1:
        raise ValueError(f'no access right with only one user for owner in file {file}')
    owner = next(iter(owner))
    return UNIXPermission(o_perm, g_perm, r_perm, group, owner)


@cache_attr('UNIX_mapping')
def unix_permissions(graph: AccessGraph):
    ret: Dict[str, UNIXPermission] = {}
    for f in graph.files:
        try:
            ret[f] = _get_unix_perm(f, graph)
        except ValueError as e:
            return e.args[0]
    return ret

# todo classic UNIX?
