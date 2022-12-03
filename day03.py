def get_priority(item: str) -> int:
    o = ord(item) - 96

    return o + (58 if o < 0 else 0)


def check_items(items):
    count = len(items) // 2
    l = set(items[:count])
    r = set(items[count:])

    same = l.intersection(r)

    return sum(map(lambda x: get_priority(x), same))


def check_badge_priorities(items) -> int:
    badge = list(set(items[0]).intersection(set(items[1])).intersection(set(items[2])))[
        0
    ]

    return get_priority(badge)


with open("day03-input.txt", "r") as f:
    data = [l.strip() for l in f.readlines()]

print(f"Answer to Q1 is {sum([check_items(i) for i in data])}")

it = iter(data)
print(f"Answer to Q2 is {sum([check_badge_priorities(i) for i in zip(it, it, it)])}")
