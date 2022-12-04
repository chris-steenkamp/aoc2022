with open("day04-input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]


def get_range(elf) -> set:
    elf = elf.split("-")
    return {i for i in range(int(elf[0]), int(elf[1]) + 1)}


def assignments_overlap_v1(pair: str) -> bool:
    e0, _, e1 = pair.partition(",")
    e0 = get_range(e0)
    e1 = get_range(e1)

    return e0.issubset(e1) or e0.issuperset(e1)


def assignments_overlap_v2(pair: str) -> bool:
    e0, _, e1 = pair.partition(",")
    e0 = get_range(e0)
    e1 = get_range(e1)

    return not e0.isdisjoint(e1)


print(len(list(filter(lambda x: x, [assignments_overlap_v1(d) for d in data]))))
print(len(list(filter(lambda x: x, [assignments_overlap_v2(d) for d in data]))))
