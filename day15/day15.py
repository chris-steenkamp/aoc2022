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
    beacons = set()

    for s in sensors:
        beacons.add(s.beacon)
        height = abs(s.location.y - line_no)
        if height > s.beacon_distance:
            continue

        for x in range(
            s.location.x - (s.beacon_distance - height),
            s.location.x + (s.beacon_distance - height) + 1,
        ):
            p = Point(x, line_no)
            out_of_range.add(p)

    return len(out_of_range.difference(beacons))


if __name__ == "__main__":
    sensors = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "sample1.txt")
    )

    print(calc_coverage_line(sensors, 10))
    # print(calc_coverage_line(sensors, coverage_map, 2000000))
