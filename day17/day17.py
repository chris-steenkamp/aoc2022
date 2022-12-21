from dataclasses import dataclass
import pathlib
from os import path
from copy import deepcopy


@dataclass
class Rock:
    name: int
    width: int
    height: int
    pattern: "list[str]"
    x: int = 0
    y: int = 0

    @property
    def bounds(self) -> set:
        return {
            (self.x + x, self.y + self.height - 1 - y)
            for x in range(self.width)
            for y in range(self.height)
            if self.pattern[y][x] == "#"
        }


ROCKS = [
    Rock(1, 4, 1, ["####"]),
    Rock(
        2,
        3,
        3,
        [".#.", "###", ".#."],
    ),
    Rock(
        3,
        3,
        3,
        ["..#", "..#", "###"],
    ),
    Rock(
        4,
        1,
        4,
        ["#", "#", "#", "#"],
    ),
    Rock(
        5,
        2,
        2,
        ["##", "##"],
    ),
]

DIRECTIONS = ["s", "d"]


def load_data(path: str) -> str:
    with open(path, "r") as f:
        return f.readline().strip()


def move_rock(
    rock: Rock, movement: str, bottom: "set[tuple[int,int]]"
) -> "tuple[bool,Rock,set[tuple[int,int]]]":
    # print(f"moving rock {rock.name} {movement}")
    rock_stopped = False
    if movement == ">":
        rock.x += 1
        if rock.bounds.intersection(bottom) or (rock.x + rock.width) > 7:
            # print("cant't move right")
            rock.x -= 1
    elif movement == "<":
        rock.x -= 1
        if rock.bounds.intersection(bottom) or rock.x < 0:
            # print("can't move left")
            rock.x += 1
    elif movement == "d":
        rock.y -= 1
        intersection = rock.bounds.intersection(bottom)
        if intersection:
            # print("can't move down")
            # for point in intersection:
            #     bottom.remove(point)
            rock.y += 1
            bottom = bottom.union(rock.bounds)
            rock_stopped = True

    return rock_stopped, rock, bottom


def simulate_rockfall(rock_movements: str, iterations: int) -> int:
    def generate_bottom_buffer():
        buffer = [[" " for _ in range(7)] for _ in range(height + 1)]
        for p in bottom:
            buffer[height - p[1]][p[0]] = "#"

        return buffer

    height = 0
    left_offset = 2
    bottom_offset = 3
    width = 7
    current_rock_ix = 0
    current_movement_ix = 0
    current_dir_ix = 0
    counter = 0

    generate_new_rock = True
    bottom = {(x, 0) for x in range(width)}

    while iterations > 0:
        if generate_new_rock:
            rock = deepcopy(ROCKS[current_rock_ix])
            rock.x = left_offset
            rock.y = height + bottom_offset + 1
            generate_new_rock = False

        direction = DIRECTIONS[current_dir_ix]
        movement = rock_movements[current_movement_ix]

        rock_landed, rock, bottom = move_rock(
            rock, movement if direction == "s" else direction, bottom
        )
        if rock_landed:
            current_rock_ix = (current_rock_ix + 1) % len(ROCKS)
            height = max(bottom, key=lambda x: x[1])[1]
            iterations -= 1
            generate_new_rock = True

        # switch between moving sideways and down on every tick
        current_dir_ix = (current_dir_ix + 1) % len(DIRECTIONS)

        # every second tick is a move sideways in the next direction indicated by the input
        if counter % 2 == 0:
            current_movement_ix = (current_movement_ix + 1) % len(rock_movements)

        counter += 1

    return height


if __name__ == "__main__":
    movements = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    print(f"Q1 answer is {simulate_rockfall(movements, 2022)}")
