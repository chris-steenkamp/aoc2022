test_data = [
    l.strip()
    for l in """
30373
25512
65332
33549
35390
""".splitlines()
    if l.strip()
]

with open("day08-input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]


def visible_from_left(data, x, y, height):
    if x == 0:
        return (True, 0)

    x -= 1
    score = 0
    while x > -1:
        score += 1
        if data[y][x] < height:
            x -= 1
        else:
            return (False, score)

    return (True, score)


def visible_from_right(data, x, y, height, bound):
    if x == bound:
        return (True, 0)

    score = 0
    x += 1
    while x < bound:
        score += 1
        if data[y][x] < height:
            x += 1
        else:
            return (False, score)

    return (True, score)


def visible_from_top(data, x, y, height):
    if y == 0:
        return (True, 0)

    y -= 1
    score = 0
    while y > -1:
        score += 1
        if data[y][x] < height:
            y -= 1
        else:
            return (False, score)

    return (True, score)


def visible_from_bottom(data, x, y, height, bound):
    if y == bound:
        return (True, 0)

    y += 1
    score = 0
    while y < bound:
        score += 1
        if data[y][x] < height:
            y += 1
        else:
            return (False, score)

    return (True, score)


def get_visible_count(data) -> int:
    # If data is not empty, then all the trees at the edges are visible
    VISIBLE_TREES = (2 * len(data)) + (2 * (len(data[0]) - 2))

    MAX_Y = len(data)
    MAX_X = len(data[0])

    for y in range(1, MAX_Y - 1):
        for x in range(1, MAX_X - 1):
            height = data[y][x]
            if (
                visible_from_left(data, x, y, height)[0]
                or visible_from_top(data, x, y, height)[0]
                or visible_from_bottom(data, x, y, height, MAX_Y)[0]
                or visible_from_right(data, x, y, height, MAX_X)[0]
            ):
                VISIBLE_TREES += 1

    return VISIBLE_TREES


def get_scenic_score(data, x, y) -> int:
    score = 1
    max_y = len(data)
    max_x = len(data[0])

    # for y in range(max_y):
    #     for x in range(max_x):
    height = data[y][x]
    score *= visible_from_left(data, x, y, height)[1]
    score *= visible_from_top(data, x, y, height)[1]
    score *= visible_from_bottom(data, x, y, height, max_x)[1]
    score *= visible_from_right(data, x, y, height, max_y)[1]

    return score


def get_max_scenic_score(data):
    scores = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            scores[(x, y)] = get_scenic_score(data, x, y)

    return max(scores.values())


assert get_visible_count(test_data) == 21
assert get_visible_count(data) == 1805
assert get_scenic_score(test_data, 2, 1) == 4
assert get_scenic_score(test_data, 2, 3) == 8

assert get_max_scenic_score(test_data) == 8
assert get_max_scenic_score(data) == 444528


print(f"Q1 answer is {get_visible_count(data)}")
print(f"Q2 answer is {get_max_scenic_score(data)}")
