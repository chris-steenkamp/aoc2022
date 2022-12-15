import pathlib
from os import path
from dataclasses import dataclass
from time import sleep
from copy import deepcopy


@dataclass
class Point:
    x: int
    y: int

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1


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


def load_data(path, initial_line: Line = None):
    MIN_X = min(initial_line.start.x, initial_line.end.x) if initial_line else 99999
    MIN_Y = 0
    MAX_X = max(initial_line.start.x, initial_line.end.x) if initial_line else -1
    MAX_Y = max(initial_line.start.y, initial_line.end.y) if initial_line else -1

    line_segments = [initial_line] if initial_line else []
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


def write_cave(cave):
    with open(
        path.join(pathlib.Path(__file__).parent.resolve(), "output.txt"), "wb"
    ) as f:
        for l in cave:
            for c in l:
                f.write(bytes(c, "UTF-8"))
            f.write(bytes("\n", "utf-8"))


def simulate_sand(
    cave,
    d_x,
    d_y,
    sand_location: Point,
    air_char: str = ".",
    sand_char: str = "+",
    save_frame: bool = False,
):
    def get_next_move(current: Point, direction: int = 0) -> "tuple[Point, Point]":
        next_p = deepcopy(current)
        while True:
            if direction == 0:
                next_p.move_down()
            elif direction == -1:
                next_p.move_down()
                next_p.move_left()
            elif direction == 1:
                next_p.move_down()
                next_p.move_right()
            elif direction == 2:
                return (current, current)

            if next_p.x < 0 or next_p.x >= max_x or next_p.y >= max_y:
                return (current, None)

            if cave[next_p.y][next_p.x] == air_char:
                return (current, next_p)
            else:
                next_p = deepcopy(current)
                direction = -1 if direction == 0 else 1 if direction == -1 else 2

    def restart(starting_x, starting_y):
        cave[starting_y][starting_x] = sand_char
        current = Point(starting_x, starting_y)

        return current

    starting_x = sand_location.x - d_x
    starting_y = sand_location.y - d_y
    max_x = len(cave[0])
    max_y = len(cave)
    sand_count = 0
    current = restart(starting_x, starting_y)
    while True:
        prev, current = get_next_move(current)

        if current is None:
            break

        if current.x == starting_x and current.y == starting_y:
            sand_count += 1
            break

        if prev != current:
            cave[prev.y][prev.x] = air_char
            cave[current.y][current.x] = sand_char
        else:
            current = restart(starting_x, starting_y)
            sand_count += 1

        if save_frame:
            write_cave(cave)

    write_cave(cave)

    return sand_count


if __name__ == "__main__":
    lines, width, height, d_x, d_y = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    rock = "🪨"
    air = "🌑"
    sand = "🫘"
    cave = generate_cave(lines, width, height, d_x, d_y, rock_char=rock, air_char=air)

    print(
        f"Q1 answer is {simulate_sand(cave, d_x, d_y, Point(500, 0), air_char=air, sand_char=sand)}"
    )

    lines, width, height, d_x, d_y = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"),
        Line(Point(0, 166), Point(1000, 166)),
    )
    cave = generate_cave(lines, width, height, d_x, d_y, rock_char=rock, air_char=air)

    print(
        f"Q2 answer is {simulate_sand(cave, d_x, d_y, Point(500, 0), air_char=air, sand_char=sand)}"
    )
