from typing import List, Any
from database.errors import DatabaseOperationError
from process.errors import ParticipantProcessError
from process.ticket_process import TicketProcess
from data import Participant
import database


class ParticipantProcess(object):
    """docstring for Participant"""

    def __init__(self, participant: Participant):
        super(ParticipantProcess, self).__init__()
        if database.participants_table.exists(participant) is False:
            raise ParticipantProcessError("Participant process cannot be created non existent participant")
        self.participant = participant
        self.tickets: List[TicketProcess] = list()
        self._init_tickets()

    def _init_tickets(self):
        self.tickets = database.tickets_table.fetch_tickets_of_a_participant_in_a_group(self.participant)

    @staticmethod
    def get_new_participant(participant_name, group_name):
        ParticipantProcess._validate_participant(participant_name)
        new_participant = Participant(
            participant_name=participant_name,
            group_name=group_name
        )
        try:
            database.participants_table.insert(new_participant)
        except DatabaseOperationError as e:
            raise ParticipantProcessError(e)
        return ParticipantProcess(new_participant)

    @staticmethod
    def _validate_participant(participant_name: str):
        if participant_name == '' or participant_name[0] == ' ':
            raise ParticipantProcessError('Invalid participant name')

    def add_ticket(self) -> TicketProcess:
        new_ticket_process = TicketProcess.get_new_ticket(
            participant_name=self.participant.participant_name,
            group_name=self.participant.group_name
        )
        self.tickets.append(new_ticket_process)
        return new_ticket_process

    def delete_ticket(self, ticket_process: TicketProcess):
        database.tickets_table.delete(ticket_process.ticket)
        self.tickets.remove(ticket_process)

    def clear_tickets(self):
        self.tickets.clear()



