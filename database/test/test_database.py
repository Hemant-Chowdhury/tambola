import unittest
import database.base
import database
from data import Group, Participant, Ticket, Board


class TestDatabase(unittest.TestCase):

    def test_complete_flow(self):
        test_group = Group(group_name='Test')
        database.groups_table.insert(test_group)
        groups_list = database.groups_table.fetch_all()
        self.assertTrue(test_group in groups_list)

        test_participant_1 = Participant(group_name=test_group.group_name, participant_name="participant_1")
        test_participant_2 = Participant(group_name=test_group.group_name, participant_name="participant_2")
        database.participants_table.insert(test_participant_1)
        database.participants_table.insert(test_participant_2)
        participant_list = database.participants_table.fetch_participants_in_a_group(test_group)
        self.assertTrue(test_participant_1 in participant_list)
        self.assertTrue(test_participant_2 in participant_list)

        test_board = Board(group_name=test_group.group_name, sequence_str='1_2_3_4_5_', pointer=0)
        database.boards_table.insert(test_board)
        fetched_board = database.boards_table.fetch_board(test_group)
        self.assertEqual(fetched_board, test_board)
        test_board.pointer = 3
        database.boards_table.update_board(test_board)
        fetched_board = database.boards_table.fetch_board(test_group)
        self.assertEqual(fetched_board, test_board)

        test_ticket_1 = Ticket(
            group_name=test_group.group_name,
            participant_name=test_participant_1.participant_name,
            ticket_string='1_2_3_4_5_')
        test_ticket_2 = Ticket(
            group_name=test_group.group_name,
            participant_name=test_participant_2.participant_name,
            ticket_string='33_44_55_66_77_')
        test_ticket_1.ticket_id = database.tickets_table.insert(test_ticket_1)
        test_ticket_2.ticket_id = database.tickets_table.insert(test_ticket_2)
        ticket_list = database.tickets_table.fetch_tickets_of_a_participant_in_a_group(test_participant_1)
        self.assertTrue(test_ticket_1 in ticket_list)
        ticket_list = database.tickets_table.fetch_tickets_of_a_participant_in_a_group(test_participant_2)
        self.assertTrue(test_ticket_2 in ticket_list)

        self.assertTrue(database.participants_table.exists(test_participant_2))

        database.groups_table.delete(test_group)

        self.assertFalse(database.participants_table.exists(test_participant_2))


if __name__ == '__main__':
    unittest.main()
