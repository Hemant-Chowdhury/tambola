class Board(object):
    """docstring for board"""

    def __init__(self, group_name, sequence_str=None, pointer=None):
        self.group_name = group_name
        self.sequence_str = sequence_str
        self.pointer = pointer

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.group_name == self.group_name \
                   and other.sequence_str == self.sequence_str \
                   and other.pointer == self.pointer
        return False
