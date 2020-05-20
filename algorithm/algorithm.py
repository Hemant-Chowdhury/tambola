import random
from typing import List


class TicketGenerator(object):
    """docstring for ticket_generator"""

    def __init__(self, rows, columns, numbers_in_each_line):
        self.rows = rows
        self.columns = columns
        self.numbers_in_each_line = numbers_in_each_line
        self.numbers: List[List[int]] = [list() for row in range(self.rows)]
        self._mark_random_positions()
        self._fill_random_numbers()
        self.print_numbers()

    def _mark_random_positions(self):
        sample_space = set(range(0, self.columns))
        for row in range(self.rows - 1):
            self.numbers[row] = self.get_new_binary_list()

        # Handle the last row so that each column should have at least 1 number
        must_positions = list()
        for col in range(self.columns):
            present = 0
            for row in range(self.rows - 1):
                present = present | self.numbers[row][col]
            if present:
                continue
            if not present:
                must_positions.append(col)
        self.numbers[self.rows - 1] = self.get_new_binary_list(must_positions=must_positions)

    def _fill_random_numbers(self):
        for col in range(self.columns):
            rows_having_number = [i for i in range(self.rows) if self.numbers[i][col]]
            sample_space = list(range(col * 10 + 1, (col + 1) * 10))
            if col == 0:
                sample_space.append(10)
            if col + 1 == self.columns:
                sample_space.append(self.columns * 10)

            random_numbers = random.sample(sample_space, len(rows_having_number))
            random_numbers.sort()
            for row, number in zip(rows_having_number, random_numbers):
                self.numbers[row][col] = number

    def get_new_binary_list(self, must_positions=None):
        if must_positions is None:
            must_positions = list()
        binary_list = [1 for _ in range(self.numbers_in_each_line - len(must_positions))] +\
                      [0 for _ in range(self.columns - self.numbers_in_each_line)]
        binary_list_a = self.shuffle_list(binary_list=binary_list[:], must_positions=must_positions)
        binary_list_b = self.shuffle_list(binary_list=binary_list[:], must_positions=must_positions)
        return self.best_binary_list(binary_list_a, binary_list_b)

    @staticmethod
    def shuffle_list(binary_list: List[int], must_positions: List[int]):
        random.shuffle(binary_list)
        must_positions.sort()
        for pos in must_positions:
            binary_list.insert(pos, 1)
        return binary_list

    @staticmethod
    def best_binary_list(list1: List[int], list2: List[int]):
        if TicketGenerator.evaluate_list(list1) > TicketGenerator.evaluate_list(list2):
            return list1
        return list2

    @staticmethod
    def evaluate_list(binary_list: List[int]):
        initial_val = 5
        count = 0
        for num in binary_list:
            if num:
                count += 1
                if count >= 3:
                    initial_val -= 1
            else:
                count = 0
        return initial_val

    def print_numbers(self):
        for row in self.numbers:
            num_str = ''
            for num in row:
                num_str += f'{num} \t'
            print(num_str)

    def get_numbers(self):
        return self.numbers


TicketGenerator(rows=3, columns=9, numbers_in_each_line=5)
