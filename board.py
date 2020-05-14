from random import shuffle
BOARD_SIZE = 90
SEPERATOR = '_'


class board(object):
    """docstring for board"""

    def __init__(self, sequence_str=None, pointer=None):
        if sequence_str is not None and pointer is not None:
            self._sequence = self._resolve_sequence_string(sequence_str)
            self._pointer = pointer
        else:
            self._sequence = list(range(1, BOARD_SIZE + 1))
            shuffle(self._sequence)
            self._pointer = 0

    @property
    def pointer(self):
        return self._pointer

    @property
    def checked_numbers(self):
        return self._sequence[:self._pointer]

    @property
    def sequence_string(self):
        representation = ""
        for element in self._sequence:
            representation += f"{element}{SEPERATOR}"
        return representation

    def _resolve_sequence_string(self, representation: str):
        representation_list = representation.split(SEPERATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        return [int(i) for i in filtered_list]

    def get_next_number(self):
        if self._pointer == BOARD_SIZE:
            return 0
        next_number = self._sequence[self._pointer]
        self._pointer += 1
        return next_number

    def is_checked(self, number) -> bool:
        if number in self.checked_numbers:
            return True
        return False


if __name__ == '__main__':
    b = board()
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    b.get_next_number()
    print(b.checked_numbers)
    x = b.sequence_string
    print(x)
    c = Board(sequence_str=b.sequence_string, pointer=b.pointer)
    print(c.checked_numbers)
