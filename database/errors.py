class DatabaseOperationError(Exception):
    """docstring for DatabaseOperationError"""

    def __init__(self, message='Internal error'):
        super(DatabaseOperationError, self).__init__(message)
