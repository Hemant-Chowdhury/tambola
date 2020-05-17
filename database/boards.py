import sqlite3

from database.base import DATABASE
from database.base import Table
from process.board import Board
from database.errors import DatabaseOperationError

connection = sqlite3.connect(DATABASE)
connection.execute("PRAGMA foreign_keys = ON")
cursor_obj = connection.cursor()


class Boards(Table):
    """docstring for boards"""

    def __init__(self):
        super(Boards, self).__init__('boards')

    @classmethod
    def _create_instance(cls):
        return Boards()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    sequence_str text,
                                    pointer int,
                                    group_name text PRIMARY KEY,
                                    CONSTRAINT fk_boards FOREIGN KEY (group_name)
                                    REFERENCES groups (name)
                                    ON DELETE CASCADE
                                    )""".format(self.table_name))
        except sqlite3.Error as e:
            print(e)

    def insert(self, board_obj):
        with connection:
            try:
                cursor_obj.execute("""INSERT INTO
                                {}(sequence_str, pointer, group_name)
                                VALUES
                                (:sequence_str, :pointer, :group_name)""".format(self.table_name),
                                   {
                                       'sequence_str': board_obj.sequence_str,
                                       'pointer': board_obj.pointer,
                                       'group_name': board_obj.group_name
                                   })

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
        return cursor_obj.fetchall()

    def fetch_board(self, group_name):
        cursor_obj.execute("SELECT sequence_str, pointer FROM {} WHERE group_name=:group_name".format(self.table_name),
                           {'group_name': group_name})
        result = cursor_obj.fetchone()
        if result is None:
            return None
        sequence_str, pointer = result
        return Board(
            sequence_str=sequence_str,
            pointer=pointer,
            group_name=group_name)

    def update_board(self, board_obj):
        with connection:
            try:
                cursor_obj.execute(
                    """UPDATE {} 
                    SET pointer=:pointer, sequence_str=:sequence_str 
                    WHERE group_name = :group_name """.format(self.table_name),
                    {'group_name': board_obj.group_name,
                     'pointer': board_obj.pointer,
                     'sequence_str': board_obj.sequence_str})
            except sqlite3.Error:
                connection.rollback()
                raise DatabaseOperationError()
