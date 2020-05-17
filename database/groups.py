import sqlite3
from database.base import DATABASE
from database.base import Table
from database.errors import DatabaseOperationError

connection = sqlite3.connect(DATABASE)
connection.execute("PRAGMA foreign_keys = ON")
cursor_obj = connection.cursor()


class Groups(Table):
    """docstring for groups"""

    def __init__(self):
        super(Groups, self).__init__('groups')

    @classmethod
    def _create_instance(cls):
        return Groups()

    def create_table(self):
        try:
            with connection:
                cursor_obj.execute("""CREATE TABLE {} (
                                    name text PRIMARY KEY
                                    )""".format(self.table_name))
        except sqlite3.Error:
            pass

    def insert(self, group_obj):
        with connection:
            try:
                cursor_obj.execute("INSERT INTO {} VALUES (:name)".format(self.table_name),
                                   {'name': group_obj.group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, group_obj):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} where name = :name".format(self.table_name),
                                   {'name': group_obj.group_name})
            except sqlite3.Error:
                pass

    def fetch_all(self):
        cursor_obj.execute("SELECT name FROM {}".format(self.table_name))
        groups_list = list()
        result = cursor_obj.fetchall()
        for name in result:
            from process.group import Group
            groups_list.append(Group(*name))
        return groups_list
