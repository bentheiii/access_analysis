from typing import TextIO

from collections import namedtuple

from accessanalysis.graph import AccessGraph

def read(source: TextIO) -> AccessGraph:
    """
    each line is of the format:
    <file name>:(<user0>,<permissions0>)->(<user1>,<permissions1>)...
    """
    # todo option for multiple user in a single tuple?
