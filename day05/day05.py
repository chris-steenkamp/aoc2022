import re
import copy

r = re.compile("^move (\d+) from (\d+) to (\d+)$")
stacks = {i: [] for i in range(1, 10)}


def add_to_stack(stack_row: str):
    global stacks
    for i in range(0, len(stack_row), 4):
        stack = (i // 4) + 1
        deets = stack_row[i : i + 4].strip()
        if deets.startswith("["):
            stacks[stack].insert(0, deets.strip(" []"))


def process_movements(stack_row: str):
    return tuple(int(g) for g in r.search(stack_row).groups())


with open("day05-input.txt", "r") as f:
    movements = []
    moves = False
    for l in [l.strip("\n") for l in f.readlines()]:
        if l.strip() == "":
            moves = True
            continue
        if moves:
            movements.append(process_movements(l))
        else:
            add_to_stack(l)


def move_v1():
    s = copy.deepcopy(stacks)
    for m in movements:
        for _ in range(m[0]):
            s[m[2]].append(s[m[1]].pop())

    return s


def move_v2():
    s = copy.deepcopy(stacks)
    for m in movements:
        s[m[2]] += s[m[1]][-m[0] :]
        s[m[1]] = s[m[1]][: -m[0]]

    return s


print("".join([s[-1] for s in move_v1().values()]))
print("".join([s[-1] for s in move_v2().values()]))
