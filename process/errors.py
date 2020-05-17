class ProcessError(Exception):

    def __init__(self, message):
        super(ProcessError, self).__init__(message)


class TicketProcessError(ProcessError):

    def __init__(self, message):
        super(TicketProcessError, self).__init__(message)


class BoardProcessError(ProcessError):
    def __init__(self, message):
        super(BoardProcessError, self).__init__(message)


class GroupProcessError(ProcessError):
    def __init__(self, message):
        super(GroupProcessError, self).__init__(message)


class ParticipantProcessError(ProcessError):
    def __init__(self, message):
        super(ParticipantProcessError, self).__init__(message)
