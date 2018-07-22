from typing import MutableMapping, MutableSet, Generic, TypeVar, Union, Tuple, Iterable, List

N = TypeVar('N')


class AccessGraph(Generic[N]):
    def __init__(self):
        self.connections: MutableMapping[N, MutableSet[N]] = {}
        self.users = set()
        self.files = set()
        self.compressed = None
        self.invalid_access = ...  # ... means unknown
        self.BLP_mapping = ...
        self.UNIX_mapping = ...

    def nodes(self):
        ret = set(self.connections)
        for tos in self.connections.values():
            for d in tos:
                if d not in ret:
                    ret.add(d)
        return ret

    def __getitem__(self, item: Tuple[N, N]) -> bool:
        f, t = item
        return t in self.connections.get(f, ())

    def __setitem__(self, key: Tuple[N, N], value: Union[bool, str]):
        f, t = key
        # if value is a string, we assume f is the user and t is the file
        if value in ('', '---'):
            pass
        elif value in ('r', 'r--'):
            self[t, f] = True
        elif value in ('w', '-w-'):
            self[f, t] = True
        elif value in ('rw', 'wr', 'rw-'):
            self[t, f] = self[f, t] = True

        elif value:
            self.connections.setdefault(f, set())
            self.connections[f].add(t)
        else:
            raise Exception('removing is not supported')

    def get(self, user, file):
        w = self[user, file]
        r = self[file, user]
        if w and r:
            return 'rw-'
        if w:
            return '-w-'
        if r:
            return 'r--'
        return '---'
