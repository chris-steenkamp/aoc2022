from unittest import TestCase
import json

from day10 import day10
from day11 import day11
from day12 import day12
from day13 import day13
from day14 import day14
from day15 import day15
from day16 import day16
from day17 import day17


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


class Day13(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day13.load_data("day13/sample1.txt"),
            day13.load_data("day13/input.txt"),
        ]
        return super().setUp()

    def test_part_1(self):
        self.assertEqual(day13.check_pair_order((1, 2)), -1)
        self.assertEqual(day13.check_pair_order((1, 1)), 0)
        self.assertEqual(day13.check_pair_order((2, 1)), 1)

        self.assertEqual(day13.check_pair_order(([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])), -1)
        self.assertEqual(day13.check_pair_order(([1, 1, 3, 2, 1], [1, 1, 3, 2, 1])), 0)
        self.assertEqual(day13.check_pair_order(([1, 1, 5, 1, 1], [1, 1, 3, 1, 1])), 1)

        self.assertEqual(day13.check_pair_order(([[1], [2, 3, 4]], [[1], 4])), -1)
        self.assertEqual(day13.check_pair_order(([9], [[8, 7, 6]])), 1)
        self.assertEqual(
            day13.check_pair_order(([[4, 4], 4, 4], [[4, 4], 4, 4, 4])), -1
        )
        self.assertEqual(day13.check_pair_order(([7, 7, 7, 7], [7, 7, 7])), 1)
        self.assertEqual(day13.check_pair_order(([], [3])), -1)
        self.assertEqual(day13.check_pair_order(([[[]]], [[]])), 1)
        self.assertEqual(
            day13.check_pair_order(
                (
                    [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                    [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                )
            ),
            1,
        )

        self.assertEqual(day13.sum_indices(self.samples[0]), 13)
        self.assertEqual(day13.sum_indices(self.samples[1]), 5882)

    def test_part_2(self):
        with open("day13/sample1-output.txt", "r") as f:
            output = [json.loads(l.strip()) for l in f.readlines()]

        self.assertEqual(
            day13.sort_pairs(
                [
                    (
                        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                    ),
                ]
            ),
            [
                [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                [[2]],
                [[6]],
            ],
        )
        self.assertEqual(day13.sort_pairs(self.samples[0]), output)
        self.assertEqual(day13.multiply_indices(self.samples[1]), 24948)


class Day14(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day14.load_data("day14/sample1.txt"),
            day14.load_data("day14/input.txt"),
            day14.load_data(
                "day14/sample1.txt",
                day14.Line(day14.Point(0, 11), day14.Point(1000, 11)),
            ),
        ]
        return super().setUp()

    def test_part_1(self):
        lines, width, height, d_x, d_y = self.samples[0]
        cave = day14.generate_cave(lines, width, height, d_x, d_y)
        self.assertEqual(
            cave,
            [
                [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", "#", ".", ".", ".", "#", "#"],
                [".", ".", ".", ".", "#", ".", ".", ".", "#", "."],
                [".", ".", "#", "#", "#", ".", ".", ".", "#", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
                ["#", "#", "#", "#", "#", "#", "#", "#", "#", "."],
            ],
        )

        self.assertEqual(day14.simulate_sand(cave, d_x, d_y, day14.Point(500, 0)), 24)

        lines, width, height, d_x, d_y = self.samples[1]
        cave = day14.generate_cave(lines, width, height, d_x, d_y)
        self.assertEqual(day14.simulate_sand(cave, d_x, d_y, day14.Point(500, 0)), 1016)
        # 25402

    def test_part_2(self):
        lines, width, height, d_x, d_y = self.samples[2]
        cave = day14.generate_cave(lines, width, height, d_x, d_y)
        self.assertEqual(day14.simulate_sand(cave, d_x, d_y, day14.Point(500, 0)), 93)


class Day15(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day15.load_data("day15/sample1.txt"),
            day15.load_data("day15/input.txt"),
        ]
        return super().setUp()

    def test_part_1(self):
        self.assertEqual(day15.calc_coverage_line(self.samples[0], 10), 26)
        # self.assertEqual(day15.calc_coverage_line(self.samples[1], 2000000), 5716881)

    def test_part_2(self):
        self.assertEqual(day15.calc_coverage_line_v2(self.samples[0], 20), 56000011)
        # self.assertEqual(day15.calc_coverage_line_v2(self.samples[1], 4000000), 10852583132904)


class Day16(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day16.load_data("day16/sample1.txt"),
            day16.load_data("day16/input.txt"),
        ]
        return super().setUp()

    def test_part_1(self):
        day16.PATHS = []
        day16.dfs(self.samples[0], "AA", 30, set(), {}, 0, "AA")
        w, _ = sorted(day16.PATHS)[-1]
        self.assertEqual(w, 1651)

        day16.PATHS = []
        day16.dfs(self.samples[1], "AA", 30, set(), {}, 0, "AA")
        w, _ = sorted(day16.PATHS)[-1]
        self.assertEqual(w, 1728)

    def test_part_2(self):
        day16.PATHS = []
        day16.dfs_v2(self.samples[0], ("AA", "AA"), 26, set(), {}, 0, "('AA','AA')")
        w, _ = sorted(day16.PATHS)[-1]
        self.assertEqual(w, 1707)

        day16.PATHS = []
        day16.dfs_v2(self.samples[1], ("AA", "AA"), 26, set(), {}, 0, "('AA','AA')")
        w, _ = sorted(day16.PATHS)[-1]
        self.assertEqual(w, 2304)


class Day17(TestCase):
    def setUp(self) -> None:
        self.samples = [
            day17.load_data("day17/sample.txt"),
            day17.load_data("day17/input.txt"),
        ]
        return super().setUp()

    def test_part_1(self):
        self.assertEqual(day17.simulate_rockfall(self.samples[0], 2022), 3068)
        self.assertEqual(day17.simulate_rockfall(self.samples[1], 2022), 3127)
