from typing import List, Optional, Tuple
import database
from algorithm.algorithm import TicketGenerator
from data import Ticket, Participant
from process.errors import TicketProcessError

COLUMNS = 9
ROWS = 3
NUMBERS_IN_EACH_LINE = 5
SEPARATOR = '_'


class TicketProcess(object):
    """docstring for ticket"""

    def __init__(self, ticket: Ticket):
        self.ticket = ticket
        if ticket.ticket_string is None:
            raise TicketProcessError('TicketProcess with empty ticket string cannot be generated. Use get_new_ticket '
                                     'to create a new Ticket process')
        self._numbers: List[List[int]] = self._resolve_ticket_string(self.ticket.ticket_string)

    @staticmethod
    def get_new_ticket(participant_name, group_name):
        generator = TicketGenerator(
            rows=ROWS,
            columns=COLUMNS,
            numbers_in_each_line=NUMBERS_IN_EACH_LINE)
        numbers = generator.get_numbers()
        new_ticket = Ticket(
            group_name=group_name,
            participant_name=participant_name,
            ticket_string=TicketProcess._generate_ticket_string(numbers)
        )
        new_ticket.ticket_id = database.tickets_table.insert(new_ticket)
        return TicketProcess(new_ticket)

    @staticmethod
    def _generate_ticket_string(numbers: List[List[int]]) -> str:
        representation = ""
        for row in numbers:
            for number in row:
                representation += f"{number}{SEPARATOR}"
        return representation

    @staticmethod
    def _resolve_ticket_string(representation: str) -> List[List[int]]:
        representation_list = representation.split(SEPARATOR)
        filtered_list = filter(lambda i: i != '', representation_list)
        int_list = [int(i) for i in filtered_list]
        if len(int_list) != COLUMNS * ROWS:
            raise TicketProcessError("Wrong ticket representation received")
        numbers = list()
        for row in range(ROWS):
            numbers.append(int_list[row * COLUMNS: row * COLUMNS + COLUMNS])
        return numbers

    @property
    def numbers(self):
        return self._numbers

    def locate_number(self, number) -> Optional[Tuple[int, int]]:
        for row_index, row in enumerate(self._numbers):
            for col_index, present_number in enumerate(row):
                if number == present_number:
                    return row_index, col_index
        return None

    def get_participant(self):
        return Participant(participant_name=self.ticket.participant_name,
                           group_name=self.ticket.group_name)
