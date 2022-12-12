from unittest import TestCase

from day10 import day10
from day11 import day11
from day12 import day12


class Day10(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day10.load_data("day10/day10-sample1.txt"),
            day10.load_data("day10/day10-sample2.txt"),
            day10.load_data("day10/day10-input.txt"),
        ]

        with open("day10/day10-sample-output.txt", "r") as f:
            self.sample_output = []
            for l in f:
                self.sample_output.extend(char for char in l.strip())
        return super().setUp()

    def test_part1(self):
        self.assertEqual(day10.get_cycle_count(self.samples[0]), 5)
        self.assertEqual(day10.process_instructions(self.samples[0])[0], 0)
        self.assertEqual(day10.process_instructions(self.samples[1])[0], 13140)
        self.assertEqual(day10.process_instructions(self.samples[2])[0], 17840)

    def test_part2(self):
        self.assertEqual(
            day10.process_instructions(self.samples[1])[1], self.sample_output
        )


class Day11(TestCase):
    def test_part_1(self):
        samples = [
            day11.load_data("day11/sample1.txt"),
            day11.load_data("day11/input.txt"),
        ]
        self.assertNotEqual(samples[0], [])
        self.assertEqual(day11.process_monkeys(samples[0], 20), 10605)
        self.assertEqual(day11.process_monkeys(samples[1], 20), 58322)

    def test_part_2(self):
        samples = [
            day11.load_data("day11/sample1.txt"),
            # day11.load_data("day11/input.txt"),
        ]
        m = samples[0]
        d = day11.process_monkeys(samples[0], 10000, 1)
        self.assertEqual(d, 2713310158)


class Day12(TestCase):
    def test_part_1(self):

        self.assertEqual(
            len(
                day12.BFS(
                    day12.load_data("day12/sample1.txt"),
                )
            ),
            31,
        )
        self.assertEqual(
            len(
                day12.BFS(
                    day12.load_data("day12/input.txt"),
                )
            ),
            520,
        )

    def test_part_2(self):

        self.assertEqual(
            day12.BFS_v2(
                day12.load_data("day12/sample1.txt"),
            ),
            29,
        )
        self.assertEqual(
            day12.BFS_v2(
                day12.load_data("day12/input.txt"),
            ),
            508,
        )
