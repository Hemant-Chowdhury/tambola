import sqlite3
from typing import List

from data import Ticket, Participant, Group
from database.base import Table, DATABASE
from database.errors import DatabaseOperationError


class Tickets(Table):
    """docstring for tickets"""

    def __init__(self):
        super(Tickets, self).__init__('tickets')

    @classmethod
    def _create_instance(cls):
        return Tickets()

    def create_table(self):
        try:
            with self.connection:
                self.cursor_obj.execute(
                    """
                    CREATE TABLE {} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ticket_string text,
                    participant_name text,
                    group_name text,
                    CONSTRAINT fk_tickets FOREIGN KEY (participant_name, group_name)
                    REFERENCES participants(name, group_name)
                    ON DELETE CASCADE
                    )""".format(self.table_name))
        except sqlite3.OperationalError:
            pass

    def insert(self, ticket_obj: Ticket) -> int:
        inserted_ticket_id = None
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    INSERT INTO 
                    {}(id, ticket_string, participant_name, group_name )
                    VALUES
                    (null, :ticket_string, :participant_name, :group_name)
                    """.format(self.table_name),
                    {
                        'ticket_string': ticket_obj.ticket_string,
                        'participant_name': ticket_obj.participant_name,
                        'group_name': ticket_obj.group_name
                    }
                )
                inserted_ticket_id = self.cursor_obj.lastrowid
            except sqlite3.IntegrityError:
                raise DatabaseOperationError('Tickets with same ticket_id already exists')
        return inserted_ticket_id

    def delete(self, ticket_obj: Ticket):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    DELETE from {} 
                    WHERE id = :ticket_id
                    """.format(self.table_name),
                    {
                        'ticket_id': ticket_obj.ticket_id
                    })
            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete_all_tickets_in_a_group(self, group_obj: Group):
        with self.connection:
            try:
                self.cursor_obj.execute(
                    """
                    DELETE from {} 
                    WHERE group_name = :group_name
                    """.format(self.table_name),
                    {'group_name': group_obj.group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        result: List[Ticket] = list()
        self.cursor_obj.execute(
            """
            SELECT id, ticket_string, participant_name, group_name 
            FROM {}
            """.format(self.table_name))
        fetch_result = self.cursor_obj.fetchall()
        for ticket_id, ticket_string, ticket_participant_name, group_name in fetch_result:
            result.append(Ticket(
                ticket_string=ticket_string,
                ticket_id=ticket_id,
                participant_name=ticket_participant_name,
                group_name=group_name))
        return result

    def fetch_tickets_of_a_participant_in_a_group(self, participant_obj: Participant):
        result = list()
        self.cursor_obj.execute(
            """
            SELECT 
            id, ticket_string 
            FROM {} 
            WHERE 
            participant_name=:participant_name AND group_name=:group_name
            """.format(self.table_name),
            {
                'participant_name': participant_obj.participant_name,
                'group_name': participant_obj.group_name
            })
        fetch_result = self.cursor_obj.fetchall()
        for ticket_id, ticket_string in fetch_result:
            result.append(
                Ticket(
                    ticket_string=ticket_string,
                    ticket_id=ticket_id,
                    participant_name=participant_obj.participant_name,
                    group_name=participant_obj.group_name))
        return result
