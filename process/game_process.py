from typing import List

from process.group_process import GroupProcess
from process.errors import ProcessError
from data import Group
import database


class GameProcess(object):
    """docstring for Game"""

    def __init__(self):
        super(GameProcess, self).__init__()
        self.groups: List[GroupProcess] = list()
        self._init_groups()

    def _init_groups(self):
        for group in database.groups_table.fetch_all():
            self.groups.append(GroupProcess(group))

    def create_new_group(self, group_name: str) -> GroupProcess:
        new_group = GroupProcess.get_new_group(group_name)
        self.groups.append(new_group)
        return new_group

    def delete_group(self, group_process: GroupProcess):
        database.groups_table.delete(group_process.group)
        self.groups.remove(group_process)
