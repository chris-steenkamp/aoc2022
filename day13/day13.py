import json
import pathlib
from os import path


def load_data(path):
    with open(path, "r") as f:
        data = [json.loads(l.strip()) for l in f if l.strip()]

    i = iter(data)
    return [(x, y) for x, y in zip(i, i)]


def sum_indices(pairs) -> int:
    return sum(
        [i + 1 for i, pair in enumerate(pairs) if check_pair_order(pair) in [-1, 0]]
    )


def check_pair_order(pair) -> str:
    l = pair[0]
    r = pair[1]

    if isinstance(l, int) and isinstance(r, int):
        return 0 if l == r else -1 if l < r else 1

    if isinstance(l, list) and isinstance(r, list):
        res = 0
        max_len = max(len(l), len(r))
        for i in range(max_len):
            try:
                res = check_pair_order((l[i], r[i]))
            except IndexError as e:
                if len(l) < len(r):
                    return -1
                if len(l) > len(r):
                    return 1
                raise e

            if res in (-1, 1):
                break

        return res

    if isinstance(l, int):
        return check_pair_order(([l], r))
    else:
        # otherwise create a list from single integer r
        return check_pair_order((l, [r]))


def sort_pairs(pairs):
    pairs.append(([[2]], [[6]]))

    data = []
    for i in range(len(pairs)):
        data.append(pairs[i][0])
        data.append(pairs[i][1])

    length = len(data)
    swapped = True
    while swapped:
        swapped = False
        for i in range(length - 1):
            if check_pair_order((data[i], data[i + 1])) > 0:
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True

    return data


def multiply_indices(pairs) -> int:
    result = 1
    for i, packet in enumerate(sort_pairs(pairs)):
        if packet == [[2]] or packet == [[6]]:
            result *= i + 1

    return result


if __name__ == "__main__":
    pairs = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))

    print(f"Q1 answer is {sum_indices(pairs)}")
    print(f"Q2 answer is {multiply_indices(pairs)}")
