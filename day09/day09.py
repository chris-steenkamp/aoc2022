from itertools import product


def get_new_tail_position(h, t):
    change_x = abs(h[0] - t[0])
    change_y = abs(h[1] - t[1])
    if (change_x, change_y) in list(product([0, 1], repeat=2)):
        return t

    if h[1] == t[1]:
        return (t[0] + 1, t[1]) if h[0] > t[0] else (t[0] - 1, t[1])

    if h[0] == t[0]:
        return (t[0], t[1] + 1) if h[1] > t[1] else (t[0], t[1] - 1)

    return (t[0] + (1 if h[0] > t[0] else -1), t[1] + (1 if h[1] > t[1] else -1))


def get_positions_v1(data):
    head = (1, 1)
    tail = head
    tail_positions = [tail]

    for current_move in data:
        direction, steps = current_move.split(" ")
        steps = int(steps)

        for _ in range(1, steps + 1):
            if "R" == direction:
                head = (head[0] + 1, head[1])
            elif "L" == direction:
                head = (head[0] - 1, head[1])
            elif "U" == direction:
                head = (head[0], head[1] + 1)
            elif "D" == direction:
                head = (head[0], head[1] - 1)

            tail = get_new_tail_position(head, tail)
            tail_positions.append(tail)

    return tail_positions


def get_positions_v2(data):
    head = (1, 1)
    tails = [head for _ in range(9)]
    tail_positions = [tails[-1]]

    for current_move in data:
        direction, steps = current_move.split(" ")
        steps = int(steps)
        for _ in range(1, steps + 1):
            if "R" == direction:
                head = (head[0] + 1, head[1])
            elif "L" == direction:
                head = (head[0] - 1, head[1])
            elif "U" == direction:
                head = (head[0], head[1] + 1)
            elif "D" == direction:
                head = (head[0], head[1] - 1)

            for i in range(9):
                new_head = head if i == 0 else tails[i - 1]
                tails[i] = get_new_tail_position(new_head, tails[i])

            tail_positions.append(tails[-1])

    return tail_positions


def draw(data, width, height):
    board = [[0 for _ in range(width)] for __ in range(height)]

    for x, y in data:
        board[height - (y)][x - 1] = 1

    return board


with open("day09-input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]

print(f"Q1 size is {len(set(get_positions_v1(data)))}")
print(f"Q2 size is {len(set(get_positions_v2(data)))}")
