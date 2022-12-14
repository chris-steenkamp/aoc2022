import pathlib
from os import path
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point

    @property
    def width(self) -> int:
        return abs(self.start.x - self.end.x) + 1

    @property
    def height(self) -> int:
        return abs(self.start.y - self.end.y) + 1


def load_data(path):
    MIN_X = 9999
    MIN_Y = 0
    MAX_X = -1
    MAX_Y = MAX_X

    line_segments = []
    with open(path, "r") as f:
        for lines in [l.strip().split(" -> ") for l in f]:
            prior_point = None
            for p in lines:
                point = Point(*map(int, p.split(",")))

                MIN_X = min(MIN_X, point.x)
                MAX_X = max(MAX_X, point.x)
                MIN_Y = min(MIN_Y, point.y)
                MAX_Y = max(MAX_Y, point.y)

                if prior_point is not None:
                    line_segments.append(Line(prior_point, point))
                prior_point = point

    return (line_segments, (MAX_X - MIN_X) + 1, (MAX_Y - MIN_Y) + 1, MIN_X, MIN_Y)


def generate_cave(
    points: "list[Line]",
    width,
    height,
    d_x,
    d_y,
    rock_char: str = "#",
    air_char: str = ".",
):
    cave = [[air_char for x in range(width)] for y in range(height)]

    for l in points:
        if l.width == 1:
            x = l.start.x - d_x
            y = min(l.start.y, l.end.y) - d_y
            for y_i in range(l.height):
                new_y = y + y_i
                cave[new_y][x] = rock_char
        else:
            y = l.start.y - d_y
            x = min(l.start.x, l.end.x) - d_x
            for x_i in range(l.width):
                new_x = x + x_i
                cave[y][new_x] = rock_char

    return cave


def simulate_sand(cave, sand_location: Point = Point(500, 0), sand_char: str = "+"):
    cave[sand_location.y - d_y][sand_location.x - d_x] = sand_char

    return cave


if __name__ == "__main__":
    lines, width, height, d_x, d_y = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    cave = generate_cave(
        lines, width, height, d_x, d_y, rock_char="🪨", air_char="  ", sand_char="🫘"
    )

    with open(
        path.join(pathlib.Path(__file__).parent.resolve(), "output.txt"), "wb"
    ) as f:
        for l in cave:
            for c in l:
                f.write(bytes(c, "UTF-8"))
            f.write(bytes("\n", "utf-8"))
