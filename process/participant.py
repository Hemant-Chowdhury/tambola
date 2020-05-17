from typing import List, Any
from process.ticket import Ticket
import database


class Participant(object):
    """docstring for Participant"""

    def __init__(self, participant_name, group_name):
        super(Participant, self).__init__()
        self.participant_name = participant_name
        self.group_name = group_name
        self.tickets: List[Ticket] = list()
        self._init_tickets()

    def _init_tickets(self):
        self.tickets = database.tickets_table.fetch_tickets_of_a_participant_in_a_group(
            group_name=self.group_name,
            participant_name=self.participant_name
        )

    def add_ticket(self):
        new_ticket = Ticket(
            participant_name=self.participant_name,
            group_name=self.group_name
        )
        ticket_id = database.tickets_table.insert(new_ticket)
        new_ticket.set_id(ticket_id)
        self.tickets.append(new_ticket)

    def delete_ticket(self, ticket_obj):
        database.tickets_table.delete(ticket_obj)
        self.tickets.remove(ticket_obj)

    def clear_ticket(self):
        self.tickets.clear()



