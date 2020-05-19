import unittest
from process import GameProcess, ParticipantProcess, BoardProcess, TicketProcess
from process.errors import GroupProcessError, ParticipantProcessError, BoardProcessError
from process.board_process import BOARD_SIZE


class TestTicketProcess(unittest.TestCase):

    def test_complete_game_process(self):
        game = GameProcess()
        test_group = game.create_new_group("Test")
        test_participant_1 = test_group.add_participant("part1")
        test_participant_2 = test_group.add_participant("part2")
        ticket_1 = test_participant_1.add_ticket()
        ticket_2 = test_participant_2.add_ticket()
        self.assertTrue(ticket_1 in test_participant_1.ticket_process_list)
        self.assertTrue(ticket_2 in test_participant_2.ticket_process_list)
        self.assertTrue(test_participant_1 in test_group.participant_process_list)
        self.assertTrue(test_participant_2 in test_group.participant_process_list)
        self.assertTrue(test_group in game.group_process_list)
        print(ticket_1.numbers)
        print(ticket_2.numbers)
        for i in range(BOARD_SIZE):
            print(i + 1, ':', test_group.board_process.get_next_number())
            self.assertEqual(test_group.board_process.pointer, i + 1)
        with self.assertRaises(BoardProcessError) as context:
            test_group.board_process.get_next_number()
        self.assertEqual(str(context.exception), 'All the numbers checked')
        game.delete_group(test_group)

    def test_duplicate_value_errors(self):
        game = GameProcess()
        test_group = game.create_new_group("Test")
        with self.assertRaises(GroupProcessError) as context:
            game.create_new_group("Test")
        self.assertEqual(str(context.exception), 'Group already exists')
        test_group.add_participant("part1")
        with self.assertRaises(ParticipantProcessError) as context:
            test_group.add_participant("part1")
        self.assertEqual(str(context.exception), 'Participant already exists')
        game.delete_group(test_group)

    def test_new_game(self):
        game = GameProcess()
        test_group = game.create_new_group("Test")
        test_participant_1 = test_group.add_participant("part1")
        test_participant_2 = test_group.add_participant("part2")
        ticket_1 = test_participant_1.add_ticket()
        ticket_2 = test_participant_2.add_ticket()
        test_board_sequence = test_group.board_process.board.sequence_str
        for i in range(10):
            test_group.board_process.get_next_number()
            self.assertEqual(test_group.board_process.pointer, i + 1)
        test_group.refresh_group_variables()
        self.assertFalse(ticket_1 in test_participant_1.ticket_process_list)
        self.assertFalse(ticket_2 in test_participant_2.ticket_process_list)
        self.assertTrue(test_participant_1 in test_group.participant_process_list)
        self.assertTrue(test_participant_2 in test_group.participant_process_list)
        self.assertEqual(test_group.board_process.pointer, 0)
        self.assertNotEqual(test_board_sequence, test_group.board_process.board.sequence_str)
        game.delete_group(test_group)


if __name__ == '__main__':
    unittest.main()
