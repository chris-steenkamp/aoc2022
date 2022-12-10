from unittest import TestCase

from day10 import load_data, get_signal_strength, get_cycle_count


class Day10(TestCase):
    def setUp(self) -> None:
        self.samples = [
            load_data("day10-sample1.txt"),
            load_data("day10-sample2.txt"),
            load_data("day10-input.txt"),
        ]
        return super().setUp()

    def test_samples(self):
        self.assertEqual(get_cycle_count(self.samples[0]), 5)
        self.assertEqual(get_signal_strength(self.samples[0]), 0)
        self.assertEqual(get_signal_strength(self.samples[1]), 13140)
        self.assertEqual(get_signal_strength(self.samples[2]), 17840)
