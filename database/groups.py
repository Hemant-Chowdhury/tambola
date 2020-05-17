import sqlite3
from typing import List
from data import Group
from database.base import Table, DATABASE
from database.errors import DatabaseOperationError


class Groups(Table):
    """docstring for groups"""

    def __init__(self):
        super(Groups, self).__init__('groups')

    @classmethod
    def _create_instance(cls):
        return Groups()

    def create_table(self):
        try:
            with self.connection:
                self.cursor_obj.execute(
                    """
                    CREATE TABLE {} (
                    name text PRIMARY KEY
                    )""".format(self.table_name))
        except sqlite3.OperationalError:
            pass

    def insert(self, group_obj: Group):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    INSERT INTO {} 
                    VALUES (:name)
                    """.format(self.table_name),
                    {
                        'name': group_obj.group_name
                    })
            except sqlite3.IntegrityError:
                raise DatabaseOperationError("Group already exists")

    def delete(self, group_obj: Group):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    DELETE from {} 
                    where name = :name""".format(self.table_name),
                    {'name': group_obj.group_name})
            except sqlite3.Error:
                pass

    def fetch_all(self):
        self.cursor_obj.execute(
            """
            SELECT name 
            FROM {}
            """.format(self.table_name))
        groups_list: List[Group] = list()
        result = self.cursor_obj.fetchall()
        for name in result:
            groups_list.append(Group(*name))
        return groups_list

    def exists(self, group_obj: Group):
        self.cursor_obj.execute(
            """
            SELECT name 
            FROM {}
            WHERE name = :name
            """.format(self.table_name),
            {'name': group_obj.group_name}
        )
        return self.cursor_obj.fetchone() is not None
