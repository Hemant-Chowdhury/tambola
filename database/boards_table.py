import sqlite3
from typing import List

from data import Board, Group
from database.base import Table, DATABASE
from database.errors import DatabaseOperationError


class Boards(Table):
    """docstring for boards"""

    def __init__(self):
        super(Boards, self).__init__('boards')

    @classmethod
    def _create_instance(cls):
        return Boards()

    def create_table(self):
        try:
            with self.connection:
                self.cursor_obj.execute(
                    """
                    CREATE TABLE {} (
                    sequence_str text,
                    pointer int,
                    group_name text PRIMARY KEY,
                    CONSTRAINT fk_boards FOREIGN KEY (group_name)
                    REFERENCES groups (name)
                    ON DELETE CASCADE
                    )""".format(self.table_name))
        except sqlite3.OperationalError:
            pass

    def insert(self, board_obj: Board):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    INSERT INTO 
                    {}(sequence_str, pointer, group_name)
                    VALUES
                    (:sequence_str, :pointer, :group_name)
                    """.format(self.table_name),
                    {
                        'sequence_str': board_obj.sequence_str,
                        'pointer': board_obj.pointer,
                        'group_name': board_obj.group_name
                    })

            except sqlite3.IntegrityError:
                raise DatabaseOperationError('Board already exists')

    def delete(self, board_obj: Board):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    DELETE from {} 
                    WHERE group_name = :group_name
                    """.format(self.table_name),
                    {
                        'group_name': board_obj.group_name
                    })
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        self.cursor_obj.execute(
            """
            SELECT sequence_str, pointer, group_name 
            FROM {}
            """.format(self.table_name))
        result: List[Board] = list()
        for sequence_str, pointer, group_name in self.cursor_obj.fetchall():
            result.append(Board(
                sequence_str=sequence_str,
                pointer=pointer,
                group_name=group_name
            ))
        return result

    def fetch_board(self, group_obj: Group):
        self.cursor_obj.execute(
            """
            SELECT 
            sequence_str, pointer 
            FROM {} 
            WHERE group_name=:group_name
            """.format(self.table_name),
            {'group_name': group_obj.group_name})
        result = self.cursor_obj.fetchone()
        if result is None:
            return None
        sequence_str, pointer = result
        return Board(
            sequence_str=sequence_str,
            pointer=pointer,
            group_name=group_obj.group_name)

    def update_pointer(self, board_obj: Board):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    UPDATE {} 
                    SET pointer=:pointer
                    WHERE group_name = :group_name 
                    """.format(self.table_name),
                    {
                        'group_name': board_obj.group_name,
                        'pointer': board_obj.pointer
                    })
            except sqlite3.Error as e:
                print(e)
                self.connection.rollback()
                raise DatabaseOperationError(e)

    def update_board(self, board_obj: Board):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    UPDATE {} 
                    SET pointer=:pointer, sequence_str=:sequence_str 
                    WHERE group_name = :group_name 
                    """.format(self.table_name),
                    {
                        'group_name': board_obj.group_name,
                        'pointer': board_obj.pointer,
                        'sequence_str': board_obj.sequence_str
                    })
            except sqlite3.Error as e:
                self.connection.rollback()
                raise DatabaseOperationError(e)

    def exists(self, board_obj: Board):
        return self.fetch_board(Group(board_obj.group_name)) is not None
