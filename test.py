from unittest import TestCase

from day10 import get_cycle_count, process_instructions, load_data


class Day10(TestCase):
    def setUp(self) -> None:
        self.samples = [
            load_data("day10-sample1.txt"),
            load_data("day10-sample2.txt"),
            load_data("day10-input.txt"),
        ]

        with open("day10-sample-output.txt", "r") as f:
            self.sample_output = []
            for l in f:
                self.sample_output.extend(char for char in l.strip())
        return super().setUp()

    def test_part1(self):
        self.assertEqual(get_cycle_count(self.samples[0]), 5)
        self.assertEqual(process_instructions(self.samples[0])[0], 0)
        self.assertEqual(process_instructions(self.samples[1])[0], 13140)
        self.assertEqual(process_instructions(self.samples[2])[0], 17840)

    def test_part2(self):
        self.assertEqual(process_instructions(self.samples[1])[1], self.sample_output)
