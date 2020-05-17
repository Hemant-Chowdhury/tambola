class Participant(object):
    """docstring for Participant"""

    def __init__(self, participant_name, group_name):
        super(Participant, self).__init__()
        self.participant_name = participant_name
        self.group_name = group_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.participant_name == other.participant_name \
                   and self.group_name == other.group_name
        return False

