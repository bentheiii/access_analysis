from typing import Iterable

import re

from accessanalysis.graph import AccessGraph

_part_pattern = re.compile('\(\s*(?P<user>[a-zA-Z_0-9]+)\s*,\s*(?P<permissions>r|rw|w|wr)\s*\)')


def read(source: Iterable[str]) -> AccessGraph:
    """
    each line is of the format:
    <file name>:(<user0>,<permissions0>)->(<user1>,<permissions1>)...
    """
    ret = AccessGraph()
    for line in source:
        line = line.strip()
        col_index = line.find(':')
        if col_index == -1:
            continue
        file = line[:col_index]
        ret.files.add(file)
        line = line[col_index + 1:]
        parts = _part_pattern.finditer(line)
        for p in parts:
            user = p['user']
            ret.users.add(user)
            perm = p['permissions']
            ret[user, file] = perm
    return ret
    # todo option for multiple user in a single tuple?
