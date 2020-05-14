import sqlite3
from abc import ABCMeta, abstractmethod
DATABASE = 'tumbola.db'

connection = sqlite3.connect(DATABASE)
connection.execute("PRAGMA foreign_keys = ON")
cursor_obj = connection.cursor()


class DatabaseOperationError(Exception):
    """docstring for DatabaseOperationError"""

    def __init__(self):
        super(DatabaseOperationError, self).__init__()


class table(metaclass=ABCMeta):
    """docstring for table"""
    __INSTANCE = None

    def __init__(self, table_name):
        self.table_name = table_name
        self.create_table()

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls.create_instance()
        return cls.__INSTANCE

    @classmethod
    @abstractmethod
    def create_instance(cls):
        ...

    @abstractmethod
    def create_table(self):
        ...

    @abstractmethod
    def insert(self):
        ...

    @abstractmethod
    def delete(self):
        ...

    @abstractmethod
    def fetch_all(self):
        ...


class groups(table):
    """docstring for groups"""

    def __init__(self):
        super(groups, self).__init__('groups')

    @classmethod
    def create_instance(cls):
        return groups()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    name text PRIMARY KEY
                                    )""".format(self.table_name))
        except sqlite3.Error:
            pass

    def insert(self, group_name):
        with connection:
            try:
                cursor_obj.execute("INSERT INTO {} VALUES (:name)".format(self.table_name),
                                   {'name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, group_name):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} where name = :name".format(self.table_name),
                                   {'name': group_name})
            except sqlite3.Error:
                pass

    def fetch_all(self):
        cursor_obj.execute("SELECT * FROM {}".format(self.table_name))
        groups_list = list()
        for name in cursor_obj.fetchall():
            groups_list.append(*name)
        return groups_list


class participants(table):
    """docstring for participants"""

    def __init__(self):
        super(participants, self).__init__('participants')

    @classmethod
    def create_instance(cls):
        return participants()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    name text NOT NULL,
                                    group_name text,
                                    PRIMARY KEY (name, group_name),
                                    CONSTRAINT fk_participants FOREIGN KEY (group_name)
                                    REFERENCES groups(name)
                                    ON DELETE CASCADE
                                    )""".format(self.table_name))
        except sqlite3.Error:
            pass

    def insert(self, group_name, participant_name):
        with connection:
            try:
                cursor_obj.execute("INSERT INTO {} VALUES (:name, :group_name)".format(self.table_name),
                                   {'name': participant_name, 'group_name': group_name})

            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, group_name, participant_name):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} WHERE name = :participant_name AND group_name = :group_name".format(self.table_name),
                                   {'participant_name': participant_name, 'group_name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        cursor_obj.execute("SELECT * FROM {}".format(self.table_name))
        print(cursor_obj.fetchall())


class tickets(table):
    """docstring for tickets"""

    def __init__(self):
        super(tickets, self).__init__('tickets')

    @classmethod
    def create_instance(cls):
        return tickets()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    ticket_string text,
                                    participant_name text,
                                    group_name text,
                                    CONSTRAINT fk_tickets FOREIGN KEY (participant_name, group_name)
                                    REFERENCES participants(name, group_name)
                                    ON DELETE CASCADE
                                    )""".format(self.table_name))
        except sqlite3.Error:
            pass

    def insert(self, ticket_string, participant_name, group_name):
        with connection:
            try:
                cursor_obj.execute("""INSERT INTO
                                {}(id, ticket_string, participant_name, group_name )
                                VALUES
                                (null, :ticket_string, :participant_name, :group_name)""".format(self.table_name),
                                   {'ticket_string': ticket_string, 'participant_name': participant_name, 'group_name': group_name})

            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, participant_name, group_name):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} WHERE participant_name = :participant_name AND group_name = :group_name".format(self.table_name),
                                   {'participant_name': participant_name, 'group_name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        cursor_obj.execute("SELECT * FROM {}".format(self.table_name))
        print(cursor_obj.fetchall())


class boards(table):
    """docstring for boards"""

    def __init__(self):
        super(boards, self).__init__('boards')

    @classmethod
    def create_instance(cls):
        return boards()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    board_string text,
                                    pointer int,
                                    group_name text PRIMARY KEY,
                                    CONSTRAINT fk_boards FOREIGN KEY (group_name)
                                    REFERENCES groups (name)
                                    ON DELETE CASCADE
                                    )""".format(self.table_name))
        except sqlite3.Error:
            pass

    def insert(self, board_string, pointer, group_name):
        with connection:
            try:
                cursor_obj.execute("""INSERT INTO
                                {}(board_string, pointer, group_name)
                                VALUES
                                (:board_string, :pointer, :group_name)""".format(self.table_name),
                                   {'board_string': board_string, 'pointer': pointer, 'group_name': group_name})

            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, group_name):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} WHERE group_name = :group_name".format(self.table_name),
                                   {'group_name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        cursor_obj.execute("SELECT * FROM {}".format(self.table_name))
        print(cursor_obj.fetchall())


groups_table = groups.get_instance()
participants_table = participants.get_instance()
tickets_table = tickets.get_instance()
boards_table = boards.get_instance()


if __name__ == '__main__':
    pass
    # groups_obj = groups.get_instance()
    # participants_obj = participants.get_instance()
    # tickets_obj = tickets.get_instance()
    # boards_obj = boards.get_instance()

    # groups_obj.insert('xy')
    # groups_obj.insert('test')
    # groups_obj.fetch_all()
    # participants_obj.insert(participant_name='Hemant', group_name='xy')
    # participants_obj.insert(participant_name='Hemant', group_name='test')
    # participants_obj.fetch_all()
    # tickets_obj.insert("2_2_2_", participant_name='Hemant', group_name='xy')
    # tickets_obj.insert("2_2_2_", participant_name='Hemant', group_name='xy')
    # tickets_obj.insert("2_2_2_", participant_name='Hemant', group_name='xy')
    # tickets_obj.fetch_all()
    # groups_obj.delete('xy')
    # groups_obj.fetch_all()
    # tickets_obj.fetch_all()
    # tickets_obj.insert("2_2_2_", participant_name='Hemant', group_name='test')
    # tickets_obj.insert("2_2_2_", participant_name='Hemant', group_name='test')
    # boards_obj.insert(board_string='2_3_4_', pointer=3, group_name='test')
    # groups_obj.fetch_all()
    # participants_obj.fetch_all()
    # tickets_obj.fetch_all()
    # boards_obj.fetch_all()
    # groups_obj.delete('test')
    # groups_obj.fetch_all()
    # participants_obj.fetch_all()
    # tickets_obj.fetch_all()
    # boards_obj.fetch_all()
