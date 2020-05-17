import sqlite3
from process.ticket import Ticket
from database.base import DATABASE
from database.base import Table
from database.errors import DatabaseOperationError

connection = sqlite3.connect(DATABASE)
connection.execute("PRAGMA foreign_keys = ON")
cursor_obj = connection.cursor()


class Tickets(Table):
    """docstring for tickets"""

    def __init__(self):
        super(Tickets, self).__init__('tickets')

    @classmethod
    def _create_instance(cls):
        return Tickets()

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

    def insert(self, ticket_obj) -> int:
        inserted_ticket_id = None
        with connection:
            try:
                cursor_obj.execute("""INSERT INTO
                                {}(id, ticket_string, participant_name, group_name )
                                VALUES
                                (null, :ticket_string, :participant_name, :group_name)""".format(self.table_name),
                                   {'ticket_string': ticket_obj.ticket_string,
                                    'participant_name': ticket_obj.participant_name,
                                    'group_name': ticket_obj.group_name})
                inserted_ticket_id = cursor_obj.lastrowid
            except sqlite3.Error:
                raise DatabaseOperationError()
        return inserted_ticket_id

    def delete(self, participant_name, group_name):
        with connection:
            try:
                cursor_obj.execute(
                    "DELETE from {} WHERE participant_name = :participant_name AND group_name = :group_name".format(
                        self.table_name),
                    {'participant_name': participant_name, 'group_name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def delete_all_tickets_in_a_group(self, group_name):
        with connection:
            try:
                cursor_obj.execute("DELETE from {} WHERE group_name = :group_name".format(self.table_name),
                                   {'group_name': group_name})
            except sqlite3.Error:
                raise DatabaseOperationError()

    def fetch_all(self):
        result = list()
        cursor_obj.execute(
            "SELECT id, ticket_string, participant_name, group_name FROM {}".format(self.table_name))
        fetch_result = cursor_obj.fetchall()
        for ticket_id, ticket_string, ticket_participant_name, group_name in fetch_result:
            result.append(Ticket(
                ticket_string=ticket_string,
                ticket_id=ticket_id,
                participant_name=ticket_participant_name,
                group_name=group_name))
        return result

    def fetch_tickets_of_a_participant_in_a_group(self, group_name, participant_name):
        result = list()
        cursor_obj.execute(
            """SELECT 
            id, ticket_string 
            FROM {} 
            WHERE 
            participant_name=:participant_name AND group_name=:group_name""".format(
                self.table_name),
            {'participant_name': participant_name, 'group_name': group_name})
        fetch_result = cursor_obj.fetchall()
        for ticket_id, ticket_string in fetch_result:
            result.append(
                Ticket(
                    ticket_string=ticket_string,
                    ticket_id=ticket_id,
                    participant_name=participant_name,
                    group_name=group_name))
        return result
