import pathlib
from os import path
import re

DIRS = [">", "v", "<", "^"]
ROW_BOUNDS = {}
COLUMN_BOUNDS = {}


def load_data(path: str):
    def update_bounds(board):
        global COLUMN_BOUNDS
        global ROW_BOUNDS
        COLUMN_BOUNDS = {}
        ROW_BOUNDS = {}

        for y in range(len(board)):
            row = board[y]
            ROW_BOUNDS[y] = (
                find_min_row_tile(row),
                max(row.rfind("."), row.rfind("#")),
            )
            for x in range(len(row)):
                bounds = COLUMN_BOUNDS.get(x, (999999, -999999))
                if row[x] in [".", "#"]:
                    min_y = min(y, bounds[0])
                    max_y = max(y, bounds[1])
                    bounds = (min_y, max_y)
                COLUMN_BOUNDS[x] = bounds

    def find_min_row_tile(row: str) -> int:
        open_min = row.find(".")
        closed_min = row.find("#")

        return min(
            open_min if open_min > -1 else closed_min,
            closed_min if closed_min > -1 else open_min,
        )

    with open(path) as f:
        data = [l.rstrip("\n") for l in f.readlines()]

    max_len = max([len(l) for l in data[: len(data) - 2]])

    board = [b.ljust(max_len) for b in data[: len(data) - 2]]
    update_bounds(board)
    moves_list = [
        (int(m[:-1]), m[-1])
        for m in re.findall("\d+[R|L|S]?", data[len(data) - 1 :][0] + "S")
    ]

    return board, moves_list


def next_direction(current_direction: str, change: str) -> str:
    d_ix = DIRS.index(current_direction)

    return DIRS[
        (d_ix + (1 if "R" == change else -1 if "L" == change else 0)) % len(DIRS)
    ]


CUBES = {
    4: [
        (8, 11, 0, 3),
        (0, 3, 4, 7),
        (4, 7, 4, 7),
        (8, 11, 4, 7),
        (8, 11, 8, 11),
        (12, 15, 8, 11),
    ],
    50: [
        (50, 99, 0, 49),
        (100, 149, 0, 49),
        (50, 99, 50, 99),
        (0, 49, 100, 149),
        (50, 99, 100, 149),
        (0, 49, 150, 199),
    ],
}

CUBE_MAP = {
    4: {
        (3, ">"): (5, "v"),
        (1, "^"): (0, ">"),
        (0, "<"): (1, "v"),
        (5, "^"): (3, "<"),
    },
    50: {
        (0, "<"): (3, ">"),
        (0, "^"): (5, ">"),
        (1, "v"): (2, "<"),
        (1, ">"): (4, "<"),
        (1, "^"): (5, "^"),
        (2, ">"): (1, "^"),
        (2, "<"): (3, "v"),
        (3, "<"): (0, ">"),
        (3, "^"): (2, ">"),
        (4, ">"): (1, "<"),
        (4, "v"): (5, "<"),
        (5, "v"): (1, "v"),
        (5, ">"): (4, "^"),
        (5, "<"): (0, "v"),
    },
}


def map_cube_coords(x, y, direction, cube_size: int):
    def find_cube(x, y) -> int:
        for ix, cube in enumerate(CUBES[cube_size]):
            if cube[0] <= x <= cube[1] and cube[2] <= y <= cube[3]:
                next_cube = CUBE_MAP[cube_size][ix, direction]
                return ix + 1, cube, CUBES[cube_size][next_cube[0]], next_cube[1]

    next_x, next_y, new_direction = x, y, direction
    in_cube, src_cube, tgt_cube, new_direction = find_cube(x, y)

    if (
        (">" == direction and "<" == new_direction)
        or ("<" == direction and ">" == new_direction)
        or ("^" == direction and "^" == new_direction)
        or ("v" == direction and "v" == new_direction)
    ):
        # invert y
        x_delta = x - src_cube[0]
        y_delta = y - src_cube[2]
        return tgt_cube[0] + x_delta, tgt_cube[3] - y_delta, new_direction
    elif (">" == direction and "^" == new_direction) or (
        "v" == direction and "<" == new_direction
    ):
        # x and y are swapped
        x_delta = x - src_cube[0]
        y_delta = y - src_cube[2]
        return tgt_cube[0] + y_delta, tgt_cube[2] + x_delta, new_direction
    elif (">" == direction and "v" == new_direction) or (
        "^" == direction and "<" == new_direction
    ):
        # x and y swapped and inverted
        x_delta = x - src_cube[0]
        y_delta = y - src_cube[2]
        return tgt_cube[1] - y_delta, tgt_cube[3] - x_delta, new_direction
    elif ("^" == direction and ">" == new_direction) or (
        "<" == direction and "v" == new_direction
    ):
        # x and y are swapped
        x_delta = x - src_cube[0]
        y_delta = y - src_cube[2]
        return tgt_cube[0] + y_delta, tgt_cube[2] + x_delta, new_direction

    return next_x, next_y, new_direction


def move_cube(
    board: "list[str]", x: int, y: int, direction: str
) -> "tuple[bool,int,int,str]":

    new_direction = direction
    if direction in ["<", ">"]:
        board_start_x, board_end_x = ROW_BOUNDS[y]
        next_x = x + (1 if ">" == direction else -1 if "<" == direction else 0)
        next_y = y
        if next_x > board_end_x or next_x < board_start_x:
            next_x, next_y, new_direction = map_cube_coords(x, y, direction, 50)
    else:
        board_start_y, board_end_y = COLUMN_BOUNDS[x]
        next_y = y + (1 if "v" == direction else -1 if "^" == direction else 0)
        next_x = x
        if next_y > board_end_y or next_y < board_start_y:
            next_x, next_y, new_direction = map_cube_coords(x, y, direction, 50)

    if board[next_y][next_x] in [" ", "#"]:
        return False, x, y, direction

    board[next_y] = "".join(
        [direction if ix == next_x else c for ix, c in enumerate(board[next_y])]
    )

    return True, next_x, next_y, new_direction


def generate_password(
    board: "list[str]", moves_list: "list[tuple[int,str]]", version: int = 1
):
    def move(
        x: int, y: int, direction: str, do_increment: bool = True
    ) -> "tuple[bool,int,int]":
        next_x = x
        next_y = y
        if do_increment:
            if direction in ["<", ">"]:
                board_start_x, board_end_x = ROW_BOUNDS[y]
                next_x = (
                    (x + (1 if ">" == direction else -1 if "<" == direction else 0))
                    % (board_end_x - board_start_x + 1)
                ) + board_start_x
            else:
                board_start_y, board_end_y = COLUMN_BOUNDS[x]
                next_y = (
                    (y + (1 if "v" == direction else -1 if "^" == direction else 0))
                    % (board_end_y - board_start_y + 1)
                ) + board_start_y

        if board[next_y][next_x] in [" ", "#"]:
            return False, x, y

        board[next_y] = "".join(
            [direction if ix == next_x else c for ix, c in enumerate(board[next_y])]
        )

        return True, next_x, next_y

    y = 0
    # start at the first open position in the first line
    x = ROW_BOUNDS[y][0] - 1
    direction = ">"

    for steps, next_dir in moves_list:
        # print(
        #     f"Move {direction} {steps} and then {'stop' if 'S' == next_dir else f'turn {next_dir}'}"
        # )

        for _ in range(steps):
            if version == 1:
                moved, next_x, next_y = move(x, y, direction)
            elif version == 2:
                moved, next_x, next_y, direction = move_cube(board, x, y, direction)
            if moved:
                x = next_x
                y = next_y
            else:
                break

        direction = next_direction(direction, next_dir)
        # update the current tile with the changed direction
        move(x, y, direction, False)

    return 1000 * (y + 1) + 4 * (x + 1) + DIRS.index(direction)


if __name__ == "__main__":
    board, moves = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    print(f"Q1 answer is {generate_password(board, moves,2)}")
