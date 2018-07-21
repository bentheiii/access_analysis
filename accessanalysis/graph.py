from typing import MutableMapping, MutableSet, Generic, TypeVar, Union, Tuple, Iterable, List

N = TypeVar('N')


class AccessGraph(Generic[N]):
    def __init__(self):
        self.connections: MutableMapping[N, MutableSet[N]] = {}
        self.users = set()
        self.files = set()
        self.invalid_access = ...  # ... means unknown
        self.BLP_mapping = ...
        self.UNIX_mapping_modern = ...
        self.UNIX_mapping_classic = ...

    def links(self, valid_nodes: Iterable[N] = ...):
        if valid_nodes is ...:
            valid_nodes = self.files

        ret: MutableMapping[N, List[Tuple[str, N]]] = {n: [] for n in valid_nodes}
        for f, t in self.connections.items():
            if f in ret:
                ret[f].extend(('to', d) for d in t)
            for d in t:
                if d in ret:
                    ret[d].append(('from', f))
        return ret

    def __iter__(self):
        ret = set(self.connections)
        for tos in self.connections.values():
            for d in tos:
                if d not in ret:
                    ret.add(d)
        return ret

    def __getitem__(self, item: Tuple[N, N]) -> bool:
        f, t = item
        return t in self.connections.get(f, ())

    def __setitem__(self, key: Tuple[N, N], value: bool):
        f, t = key
        if value:
            self.connections[f].add(t)
        else:
            self.connections[f].remove(t)