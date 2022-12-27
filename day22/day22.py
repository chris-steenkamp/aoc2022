import pathlib
from os import path
import re

DIRS = [">", "v", "<", "^"]
ROW_BOUNDS = {}
COLUMN_BOUNDS = {}


def load_data(path: str):
    global COLUMN_BOUNDS
    COLUMN_BOUNDS = {}

    def update_column_bounds(board):
        for y in range(len(board)):
            row = board[y]
            for x in range(len(row)):
                bounds = COLUMN_BOUNDS.get(x, (999999, -999999))
                if row[x] in [".", "#"]:
                    min_y = min(y, bounds[0])
                    max_y = max(y, bounds[1])
                    bounds = (min_y, max_y)
                COLUMN_BOUNDS[x] = bounds

    def update_row_bounds(board):
        global ROW_BOUNDS
        ROW_BOUNDS = {}
        for y in range(len(board)):
            b = board[y]
            ROW_BOUNDS[y] = (find_min(b), max(b.rfind("."), b.rfind("#")))

    def find_min(l: str) -> int:
        open_min = l.find(".")
        closed_min = l.find("#")

        return min(
            open_min if open_min > -1 else closed_min,
            closed_min if closed_min > -1 else open_min,
        )

    with open(path) as f:
        data = [l.rstrip("\n") for l in f.readlines()]

    max_len = max([len(l) for l in data])

    board = [b.ljust(max_len) for b in data[: len(data) - 2]]
    update_row_bounds(board)
    update_column_bounds(board)
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


def generate_password(
    board: "list[tuple[str,int,int]]", moves_list: "list[tuple[int,str]]"
):
    def move_horizonally(x: int, y: int) -> bool:
        board_start_x = ROW_BOUNDS[y][0]
        board_end_x = ROW_BOUNDS[y][1]
        check_x = (x % (board_end_x - board_start_x + 1)) + board_start_x
        if board[y][check_x] in [" ", "#"]:
            return False, x

        board[y] = "".join(
            [direction if ix == check_x else c for ix, c in enumerate(board[y])]
        )

        return True, check_x

    def move_vertically(x: int, y: int) -> bool:
        board_start_y = COLUMN_BOUNDS[x][0]
        board_end_y = COLUMN_BOUNDS[x][1]
        check_y = (y % (board_end_y - board_start_y + 1)) + board_start_y
        if board[check_y][x] in [" ", "#"]:
            return False, y

        board[check_y] = "".join(
            [direction if ix == x else c for ix, c in enumerate(board[check_y])]
        )

        return True, check_y

    y = 0
    # start at the first open position in the first line
    x = ROW_BOUNDS[y][0] - 1
    direction = ">"

    for steps, next_dir in moves_list:
        # print(
        #     f"Move {direction} {steps} and then {'stop' if 'S' == next_dir else f'turn {next_dir}'}"
        # )

        for _ in range(steps):
            if direction in [">", "<"]:
                next_x = x + (1 if ">" == direction else -1 if "<" == direction else 0)
                moved, next_x = move_horizonally(next_x, y)
                if moved:
                    x = next_x
                else:
                    break
            else:
                next_y = y + (1 if "v" == direction else -1 if "^" == direction else 0)
                moved, next_y = move_vertically(x, next_y)
                if moved:
                    y = next_y
                else:
                    break

        direction = next_direction(direction, next_dir)
        # update the current tile with the changed direction
        move_horizonally(x, y)

    return 1000 * (y + 1) + 4 * (x + 1) + DIRS.index(direction)


if __name__ == "__main__":
    board, moves = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    print(f"Q1 answer is {generate_password(board, moves)}")
