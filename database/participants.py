import sqlite3

from database.base import DATABASE
from database.base import Table
from process.participant import Participant
from database.errors import DatabaseOperationError

connection = sqlite3.connect(DATABASE)
connection.execute("PRAGMA foreign_keys = ON")
cursor_obj = connection.cursor()


class Participants(Table):
    """docstring for participants"""

    def __init__(self):
        super(Participants, self).__init__('participants')

    @classmethod
    def _create_instance(cls):
        return Participants()

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

    def insert(self, participant_obj):
        with connection:
            try:
                cursor_obj.execute("INSERT INTO {} VALUES (:name, :group_name)".format(self.table_name),
                                   {'name': participant_obj.participant_name, 'group_name': participant_obj.group_name})

            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete(self, participant_obj):
        with connection:
            try:
                cursor_obj.execute(
                    "DELETE from {} WHERE name = :participant_name AND group_name = :group_name".format(
                        self.table_name),
                    {'participant_name': participant_obj.participant_name, 'group_name': participant_obj.group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        cursor_obj.execute("SELECT * FROM {}".format(self.table_name))
        return cursor_obj.fetchall()

    def fetch_participants_in_a_group(self, group_name: str):
        cursor_obj.execute("SELECT name FROM {} WHERE group_name = :groupname".format(self.table_name),
                           {'groupname': group_name})
        participants_list = list()
        for participant_name in cursor_obj.fetchall():
            participants_list.append(
                Participant(
                    group_name=group_name,
                    *participant_name
                )
            )
        return participants_list
