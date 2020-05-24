from typing import List, Optional
import database
from database.errors import DatabaseOperationError
from process.errors import GroupProcessError
from process.participant_process import ParticipantProcess
from process.board_process import BoardProcess
from data import Group


class GroupProcess(object):
    """docstring for Group"""

    def __init__(self, group: Group):
        super(GroupProcess, self).__init__()
        if database.groups_table.exists(group) is False:
            raise GroupProcessError("Cannot create group process for non existent group")
        self.group = group
        self.participant_process_list: List[ParticipantProcess] = list()
        self._init_participants()
        self.board_process: Optional[BoardProcess] = None
        self._init_board()

    def _init_participants(self):
        for participant in database.participants_table.fetch_participants_in_a_group(self.group):
            self.participant_process_list.append(ParticipantProcess(participant))

    def _init_board(self):
        board = database.boards_table.fetch_board(self.group)
        if board is None:
            self.board_process = BoardProcess.get_new_board(self.group.group_name)
            return
        self.board_process = BoardProcess(board=board)

    @staticmethod
    def get_new_group(group_name):
        GroupProcess._validate_group(group_name)
        new_group = Group(group_name=group_name)
        try:
            database.groups_table.insert(new_group)
        except DatabaseOperationError as e:
            raise GroupProcessError(e)
        return GroupProcess(new_group)

    @staticmethod
    def _validate_group(group_name: str):
        if group_name == '' or group_name[0] == ' ':
            raise GroupProcessError('Invalid group name')

    def add_participant(self, participant_name: str) -> ParticipantProcess:
        participant_process = ParticipantProcess.get_new_participant(
            participant_name=participant_name,
            group_name=self.group.group_name)
        self.participant_process_list.append(participant_process)
        return participant_process

    def remove_participant(self, participant_process_obj: ParticipantProcess):
        try:
            database.participants_table.delete(participant_process_obj.participant)
            self.participant_process_list.remove(participant_process_obj)
        except DatabaseOperationError:
            raise GroupProcessError(f'Unable to remove {participant_process_obj.participant.participant_name},'
                                    f' please try again')

    def refresh_group_variables(self):
        try:
            self.board_process.refresh_board()
            database.tickets_table.delete_all_tickets_in_a_group(self.group)
            for participant in self.participant_process_list:
                participant.clear_tickets()
        except DatabaseOperationError:
            raise GroupProcessError('Unable to start a new game, please try again!')
