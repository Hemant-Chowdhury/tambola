from algorithm import ticket_generator

COLUMNS = 9
ROWS = 3
NUMBERS_IN_EACH_LINE = 5
SEPERATOR = '_'


class ticket(object):
    """docstring for ticket"""

    def __init__(self, ticket_string=None):
        if ticket_string:
            self._numbers = self._resolve_ticket_string(ticket_string)
        else:
            generator = ticket_generator(
                rows=ROWS,
                columns=COLUMNS,
                numbers_in_each_line=NUMBERS_IN_EACH_LINE)
            self._numbers = generator.get_numbers()

    def __repr__(self):
        representation = ""
        for row in self._numbers:
            for number in row:
                representation += f"{number}{SEPERATOR}"
        return representation

    def __str__(self):
        representation = ''
        for row in self._numbers:
            for num in row:
                representation += f'{num}\t'
            representation += '\n'
        return representation

    @property
    def numbers(self):
        return self._numbers

    def _resolve_ticket_string(self, representation: str):
        representation_list = representation.split(SEPERATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        int_list = [int(i) for i in filtered_list]
        assert len(int_list) == COLUMNS * ROWS, "Wrong ticket representation received"
        numbers = list()
        for row in range(ROWS):
            numbers.append(int_list[row * COLUMNS: row * COLUMNS + COLUMNS])
        return numbers


if __name__ == '__main__':
    t = ticket()
    print(t)
    nt = ticket(ticket_string=repr(t))
    print(nt)
