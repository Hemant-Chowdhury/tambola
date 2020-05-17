from typing import List

from process.group import Group
from process.errors import DataObjectError
import database


class Game(object):
    """docstring for Game"""

    def __init__(self):
        super(Game, self).__init__()
        self.groups: List[Group] = list()
        self.__init_groups()

    def __init_groups(self):
        self.groups = database.groups_table.fetch_all()

    def create_new_group(self, group_name: str):
        self._validate_group(group_name)
        new_group = Group(group_name)
        database.groups_table.insert(new_group)
        new_group.set_new_board_if_not_present()
        self.groups.append(new_group)

    def _validate_group(self, group_name: str):
        if group_name == '' or group_name[0] == ' ':
            raise DataObjectError('Invalid group name')
        for group_obj in self.groups:
            if group_obj.group_name == group_name :
                raise DataObjectError('Group already exists')

    def delete_group(self, group: Group):
        database.groups_table.delete(group)
        self.groups.remove(group)


if __name__ == '__main__':

    game = Game()
    game.create_new_group("Test")
    test_group = game.groups[0]
    test_group.add_participant("Hemant")
    participant_0 = test_group.participants[0]
    participant_0.add_ticket()
    participant_0.add_ticket()
    for ticket_obj in participant_0.tickets:
        print(ticket_obj)
    game.delete_group(test_group)