from typing import List, Optional
import database
from database.errors import DatabaseOperationError
from process.errors import DataObjectError
from process.participant import Participant
from process.board import Board


class Group(object):
    """docstring for Group"""

    def __init__(self, group_name: str):
        super(Group, self).__init__()
        self.group_name = group_name
        self.participants: List[Participant] = list()
        self.__init_participants()
        self.board: Optional[Board] = None
        self.__init_board()

    def __init_participants(self):
        self.participants = database.participants_table.fetch_participants_in_a_group(self.group_name)

    def __init_board(self):
        self.board = database.boards_table.fetch_board(self.group_name)

    def add_participant(self, participant_name: str):
        self._validate_participant(participant_name)
        new_participant = Participant(
            participant_name=participant_name,
            group_name=self.group_name)
        database.participants_table.insert(new_participant)
        self.participants.append(new_participant)

    def _validate_participant(self, participant_name: str):
        if participant_name=='' or participant_name[0] == ' ':
            raise DataObjectError('Invalid participant name')
        for participant_obj in self.participants:
            if participant_name == participant_obj.participant_name:
                raise DataObjectError('Participant already exists')

    def remove_participant(self, participant_obj):
        database.participants_table.delete(participant_obj)
        self.participants.remove(participant_obj)

    def set_new_board_if_not_present(self):
        if self.board:
            return
        new_board = Board(group_name=self.group_name)
        database.boards_table.insert(new_board)
        self.board = new_board

    def refresh_group_variables(self):
        new_board = Board(group_name=self.group_name)
        try:
            database.tickets_table.delete_all_tickets_in_a_group(self.group_name)
            for participant in self.participants:
                participant.clear_tickets()
            database.boards_table.update_board(new_board)
            self.board = new_board

        except DatabaseOperationError:
            raise DataObjectError('Unable to start a new game')







