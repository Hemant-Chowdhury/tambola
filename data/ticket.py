class Ticket(object):
    """docstring for ticket"""

    def __init__(self, participant_name, group_name, ticket_id=None, ticket_string=None):
        self.group_name = group_name
        self.participant_name = participant_name
        self.ticket_id = ticket_id
        self.ticket_string = ticket_string

    def __str__(self):
        return f'{self.ticket_string}\n{self.ticket_id}\n{self.participant_name}\n{self.group_name}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.group_name == self.group_name \
                   and other.participant_name == self.participant_name \
                   and other.ticket_id == self.ticket_id \
                   and other.ticket_string == self.ticket_string
