from random import shuffle
from typing import List

import database
from database.errors import DatabaseOperationError
from process.errors import BoardProcessError
from data import Board


BOARD_SIZE = 90
SEPARATOR = '_'


class BoardProcess(object):
    """docstring for board"""

    def __init__(self, board: Board):
        if database.boards_table.exists(board) is False:
            raise BoardProcessError("Cannot create a Board process for non existent board")
        self.board = board
        self._sequence_numbers: List[int] = self._resolve_sequence_str(self.board.sequence_str)

    @staticmethod
    def get_new_board(group_name):
        new_board = Board(
            group_name=group_name,
            sequence_str=BoardProcess._get_new_sequence_str(),
            pointer=0)
        try:
            database.boards_table.insert(new_board)
        except DatabaseOperationError as e:
            raise BoardProcessError(e)
        return BoardProcess(new_board)

    @staticmethod
    def _get_new_sequence_str():
        sequence = list(range(1, BOARD_SIZE + 1))
        shuffle(sequence)
        sequence_str = BoardProcess._generate_sequence_str(sequence)
        return sequence_str

    @staticmethod
    def _resolve_sequence_str(representation: str) -> List[int]:
        representation_list = representation.split(SEPARATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        return [int(i) for i in filtered_list]

    @staticmethod
    def _generate_sequence_str(sequence) -> str:
        sequence_str = ''
        for number in sequence:
            sequence_str += f'{number}_'
        return sequence_str

    def get_checked_numbers(self) -> List[int]:
        return self._sequence_numbers[:self.board.pointer]

    def get_next_number(self) -> int:
        if self.board.pointer == BOARD_SIZE:
            raise BoardProcessError('All the numbers checked')
        next_number = self._sequence_numbers[self.board.pointer]
        self.board.pointer += 1
        try:
            database.boards_table.update_pointer(self.board)
        except DatabaseOperationError:
            self.board.pointer -= 1
            raise BoardProcessError('Unable to get next number, try again!')
        return next_number

    def is_checked(self, number) -> bool:
        if number in self.get_checked_numbers():
            return True
        return False

    def refresh_board(self):
        self.board.sequence_str = BoardProcess._get_new_sequence_str()
        self.board.pointer = 0
        database.boards_table.update_board(self.board)
