from random import shuffle
import database
from database.errors import DatabaseOperationError
from process.errors import DataObjectError


BOARD_SIZE = 90
SEPARATOR = '_'


class Board(object):
    """docstring for board"""

    def __init__(self, group_name, sequence_str=None, pointer=None):
        self.group_name = group_name
        if sequence_str is not None and pointer is not None:
            self._sequence = self._resolve_sequence_str(sequence_str)
            self._pointer = pointer
        else:
            self._sequence = list(range(1, BOARD_SIZE + 1))
            shuffle(self._sequence)
            self._pointer = 0

    def __str__(self):
        return f"{self._sequence}\npointer: {self._pointer}"

    @property
    def pointer(self):
        return self._pointer

    @property
    def checked_numbers(self):
        return self._sequence[:self._pointer]

    @property
    def sequence_str(self):
        representation = ""
        for element in self._sequence:
            representation += f"{element}{SEPARATOR}"
        return representation

    @staticmethod
    def _resolve_sequence_str(representation: str):
        representation_list = representation.split(SEPARATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        return [int(i) for i in filtered_list]

    def get_next_number(self):
        if self._pointer == BOARD_SIZE:
            raise DataObjectError('Unable to get next number')
        next_number = self._sequence[self._pointer]
        self._pointer += 1
        try:
            database.boards_table.update_board(self)
        except DatabaseOperationError:
            self._pointer -= 1
            raise DataObjectError('Unable to get next number, try again!')
        return next_number

    def is_checked(self, number) -> bool:
        if number in self.checked_numbers:
            return True
        return False


if __name__ == '__main__':
    b = Board(group_name='')
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    print(b.checked_numbers)
    x = b.sequence_str
    print(x)
    c = Board(group_name='', sequence_str=b.sequence_str, pointer=b.pointer)
    print(c.checked_numbers)
