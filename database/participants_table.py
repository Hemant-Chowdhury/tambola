import sqlite3
from typing import List
from data import Participant, Group
from database.base import Table, DATABASE
from database.errors import DatabaseOperationError


class Participants(Table):
    """docstring for participants"""

    def __init__(self):
        super(Participants, self).__init__('participants')

    @classmethod
    def _create_instance(cls):
        return Participants()

    def create_table(self):
        try:
            with self.connection:
                self.cursor_obj.execute(
                    """
                    CREATE TABLE {} (
                    name text NOT NULL,
                    group_name text,
                    PRIMARY KEY (name, group_name),
                    CONSTRAINT fk_participants FOREIGN KEY (group_name) 
                    REFERENCES groups(name) 
                    ON DELETE CASCADE
                    )""".format(self.table_name))
        except sqlite3.OperationalError:
            pass

    def insert(self, participant_obj: Participant):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    INSERT INTO {} 
                    VALUES (:name, :group_name)
                    """.format(self.table_name),
                    dict(
                        name=participant_obj.participant_name,
                        group_name=participant_obj.group_name
                    ))

            except sqlite3.IntegrityError:
                raise DatabaseOperationError('Participant already exists')

    def delete(self, participant_obj: Participant):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    DELETE from {} 
                    WHERE name = :participant_name AND group_name = :group_name
                    """.format(self.table_name),
                    {
                        'participant_name': participant_obj.participant_name,
                        'group_name': participant_obj.group_name
                    })
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        self.cursor_obj.execute("SELECT name, group_name FROM {}".format(self.table_name))
        result: List[Participant] = list()
        for participant_name, group_name in self.cursor_obj.fetchall():
            result.append(Participant(
                participant_name=participant_name,
                group_name=group_name
            ))

        return self.cursor_obj.fetchall()

    def fetch_participants_in_a_group(self, group_obj: Group):
        self.cursor_obj.execute(
            """
            SELECT name 
            FROM {} 
            WHERE group_name = :group_name
            """.format(self.table_name),
            {
                'group_name': group_obj.group_name
            })
        participants_list = list()
        for participant_name in self.cursor_obj.fetchall():
            participants_list.append(
                Participant(
                    group_name=group_obj.group_name,
                    *participant_name
                )
            )
        return participants_list

    def exists(self, participant_obj: Participant) -> bool:
        self.cursor_obj.execute(
            """
            SELECT * 
            FROM {} 
            WHERE group_name = :group_name AND name = :name
            """.format(self.table_name),
            {
                'group_name': participant_obj.group_name,
                'name': participant_obj.participant_name
            })
        return self.cursor_obj.fetchone() is not None
