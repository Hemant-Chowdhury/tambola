# TODO Create a more sparsely generated ticket numbers
import random


class TicketGenerator(object):
    """docstring for ticket_generator"""

    def __init__(self, rows, columns, numbers_in_each_line):
        self.rows = rows
        self.columns = columns
        self.numbers_in_each_line = numbers_in_each_line
        self.numbers = [[0 for col in range(self.columns)] for row in range(self.rows)]
        self._mark_random_positions()
        self._fill_random_numbers()

    def _mark_random_positions(self):
        sample_space = set(range(0, self.columns))
        for row in range(self.rows - 1):
            for element in random.sample(sample_space, self.numbers_in_each_line):
                self.numbers[row][element] = 1

        # Handle the last row so that each column should have atlease 1 number
        required_nums = self.numbers_in_each_line
        for col in range(self.columns):
            present = 0
            for row in range(self.rows):
                present = present | self.numbers[row][col]
            if present:
                continue
            self.numbers[self.rows - 1][col] = 1
            required_nums = required_nums - 1
            sample_space.discard(col)

        for element in random.sample(sample_space, required_nums):
            self.numbers[self.rows - 1][element] = 1

    def _fill_random_numbers(self):
        for col in range(self.columns):
            rows_having_number = [i for i in range(self.rows) if self.numbers[i][col]]
            sample_space = list(range(col * 10 + 1, (col + 1) * 10))
            if not col:
                sample_space.append(col * 10)
            if col + 1 == self.columns:
                sample_space.append(self.columns * 10)

            random_numbers = random.sample(sample_space, len(rows_having_number))
            random_numbers.sort()
            for row, number in zip(rows_having_number, random_numbers):
                self.numbers[row][col] = number

    def get_numbers(self):
        return self.numbers
