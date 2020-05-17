class Group(object):
    """docstring for Group"""

    def __init__(self, group_name: str):
        super(Group, self).__init__()
        self.group_name = group_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.group_name == self.group_name
        return False

