from algorithm.algorithm import TicketGenerator

COLUMNS = 9
ROWS = 3
NUMBERS_IN_EACH_LINE = 5
SEPARATOR = '_'


class Ticket(object):
    """docstring for ticket"""

    def __init__(self, participant_name, group_name, ticket_id=None, ticket_string=None):
        self.group_name = group_name
        self.participant_name = participant_name
        self._ticket_id = None
        if ticket_id:
            self._ticket_id = ticket_id
        if ticket_string:
            self._numbers = self._resolve_ticket_string(ticket_string)
        else:
            generator = TicketGenerator(
                rows=ROWS,
                columns=COLUMNS,
                numbers_in_each_line=NUMBERS_IN_EACH_LINE)
            self._numbers = generator.get_numbers()

    def __str__(self):
        representation: str = ''
        for row in self._numbers:
            for num in row:
                representation += f'{num}\t'
            representation += '\n'
        return f'{representation}\n{self._ticket_id}\n{self.participant_name}'

    @property
    def ticket_string(self):
        representation = ""
        for row in self._numbers:
            for number in row:
                representation += f"{number}{SEPARATOR}"
        return representation

    @property
    def numbers(self):
        return self._numbers

    @property
    def ticket_id(self):
        return self._ticket_id

    @staticmethod
    def _resolve_ticket_string(representation: str):
        representation_list = representation.split(SEPARATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        int_list = [int(i) for i in filtered_list]
        assert len(int_list) == COLUMNS * ROWS, "Wrong ticket representation received"
        numbers = list()
        for row in range(ROWS):
            numbers.append(int_list[row * COLUMNS: row * COLUMNS + COLUMNS])
        return numbers

    def set_id(self, ticket_id):
        self._ticket_id = ticket_id


if __name__ == '__main__':
    t = Ticket(group_name='', participant_name='')
    print(t)
    nt = Ticket(ticket_string=t.ticket_string)
    print(nt)
