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
    def bounds(self) -> "set[tuple[int,int]]":
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
        if rock.bounds.intersection(bottom):
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
            height = max(height, rock.height + rock.y - 1)
            iterations -= 1
            generate_new_rock = True

        # switch between moving sideways and down on every tick
        current_dir_ix = (current_dir_ix + 1) % len(DIRECTIONS)

        # every second tick is a move sideways in the next direction indicated by the input
        if counter % 2 == 0:
            current_movement_ix = (current_movement_ix + 1) % len(rock_movements)

        counter = (counter + 1) % 2

    return height


def simulate_rockfall_v2(rock_movements: str, iterations: int) -> int:
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

    rocks_simulated = 0
    cycle_height = 0

    states = {}

    bottom = {(x, 0) for x in range(width)}

    while rocks_simulated < iterations:
        rock = deepcopy(ROCKS[current_rock_ix])
        current_rock_ix = (current_rock_ix + 1) % len(ROCKS)
        rock.x = left_offset
        rock.y = height + bottom_offset + 1

        while True:
            movement = rock_movements[current_movement_ix]
            current_movement_ix = (current_movement_ix + 1) % len(rock_movements)

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

            rock.y -= 1
            if rock.bounds.intersection(bottom):
                rock.y += 1
                break

        bottom = bottom.union(rock.bounds)
        height = max(height, rock.height + rock.y - 1)

        # thanks to https://github.com/rossmacarthur/advent/blob/trunk/2022/17.rs
        # for the cycle detection logic.
        row_heights = tuple((x, height) in bottom for x in range(width))
        # store the next rock and movement type along with the current row heights
        # this allows us to identify when there is a cycle so we can skip simulating
        key = (current_rock_ix, current_movement_ix, row_heights)
        # the initial number of iterations doesn't contain a cycle so only check
        # once we have passed that value.
        if rocks_simulated > 2022 and cycle_height == 0:
            if key in states:
                r0, h0 = states[key]
                # difference between current rock count and count when cycle started
                dr = rocks_simulated - r0
                # difference between current height and height when cycle started
                dh = height - h0
                # calculate the number of cycles that will be repeated in the remaining iterations
                count = (iterations - rocks_simulated) // dr
                # increase the current rock count and height by the amounts that would be
                # added for each cycle
                rocks_simulated += count * dr
                cycle_height += count * dh
        states[key] = (rocks_simulated, height)

        rocks_simulated += 1

    return height + cycle_height


if __name__ == "__main__":
    movements = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    print(f"Q1 answer is {simulate_rockfall(movements, 2022)}")
    print(f"Q1 answer is {simulate_rockfall_v2(movements, 1000000000000)}")
