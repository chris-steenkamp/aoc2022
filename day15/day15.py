from dataclasses import dataclass
from os import path
import pathlib


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Sensor:
    location: Point
    beacon: Point
    _distance: int

    @classmethod
    def manhattan_distance(cls, p1: Point, p2: Point):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def __init__(self, location: Point, beacon: Point):
        self.location = location
        self.beacon = beacon
        self._distance = Sensor.manhattan_distance(location, beacon)

    @property
    def beacon_distance(self):
        return self._distance


def load_data(path: str) -> "list[Sensor]":
    def get_point(coords: str) -> Point:
        x, y = coords.split(", ")
        return Point(int(x.split("=")[1]), int(y.split("=")[1]))

    sensors = []

    with open(path, "r") as f:
        for line in [l.strip() for l in f.readlines()]:
            s, b = line.replace("Sensor at ", "").split(": closest beacon is at ")

            sensors.append(Sensor(get_point(s), get_point(b)))

    return sensors


def calc_coverage_line(sensors: "list[Sensor]", line_no: int) -> int:
    out_of_range = set()

    for s in sensors:
        height = abs(s.location.y - line_no)
        if height > s.beacon_distance:
            continue

        for x in range(
            s.location.x - (s.beacon_distance - height),
            s.location.x + (s.beacon_distance - height),
        ):
            p = Point(x, line_no)
            out_of_range.add(p)

    return len(out_of_range)


def calc_coverage_line_v2(sensors: "list[Sensor]", max_y: int) -> int:
    for current_y in range(max_y):
        ranges = []
        for s in sensors:
            height = abs(s.location.y - current_y)
            if height > s.beacon_distance:
                continue

            ranges.append(
                [
                    s.location.x - (s.beacon_distance - height),
                    s.location.x + (s.beacon_distance - height),
                ]
            )

        # order the ranges from low to high
        ranges.sort()

        merged_ranges = [ranges[0]]

        for start, end in ranges[1:]:
            _, prev_end = merged_ranges[-1]

            # if the two ranges are not overlapping, add the new range
            if start > prev_end + 1:
                merged_ranges.append([start, end])
                continue

            # otherwise merge the two ranges together
            merged_ranges[-1][1] = max(prev_end, end)

        x = 0
        for start, end in merged_ranges:
            # if x is to the left of the range then we have found the answer (? check this logic)
            if x < start:
                return x * 4000000 + current_y

            # otherwise update x to be to the right of the range.
            x = max(x, end + 1)

            # if x is outside of the valid bounds then the beacon can't be in this row
            if x > max_y:
                break

    return None


if __name__ == "__main__":
    sensors = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))

    print(f"Q1 answer is {calc_coverage_line(sensors, 2000000)}")
    print(f"Q2 answer is {calc_coverage_line_v2(sensors, 4000000)}")
