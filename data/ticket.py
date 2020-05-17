class Ticket(object):
    """docstring for ticket"""

    def __init__(self, participant_name, group_name, ticket_id=None, ticket_string=None):
        self.group_name = group_name
        self.participant_name = participant_name
        self.ticket_id = ticket_id
        self.ticket_string = ticket_string

    def __str__(self):
        return f'{self.ticket_string}\n{self.ticket_id}\n{self.participant_name}'
