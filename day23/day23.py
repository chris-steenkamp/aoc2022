import pathlib
from os import path


def load_data(path: str):
    with open(path) as f:
        data = [l.strip() for l in f.readlines()]

    return data


if __name__ == "__main__":
    board, moves = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    # print(f"Q1 answer is {generate_password(board, moves,2)}")
