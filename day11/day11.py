from dataclasses import dataclass
from functools import reduce
import operator


@dataclass
class Monkey:
    items: list
    operation: list
    divisible_by: int
    next_monkey: tuple
    items_inspected: int = 0


def load_data(path):
    with open(path, "r") as f:
        data = []
        while True:
            monkey = [f.readline().strip("\n\t ") for _ in range(7)]
            if "" == monkey[0]:
                break

            data.append(
                Monkey(
                    list(map(int, monkey[1][16:].split(","))),
                    monkey[2][21:].split(" "),
                    int(monkey[3][19:]),
                    (int(monkey[5][26:]), int(monkey[4][25:])),
                )
            )

    return data


def increase_worry_level(old: int, operation: list) -> int:
    op, value = operation
    new_value = old if value.isalpha() else int(value)
    if "*" == op:
        return old * new_value
    elif "+" == op:
        return old + new_value


def get_most_active(monkeys):
    return sorted(monkeys, key=lambda x: x.items_inspected, reverse=True)


def process_monkeys(monkeys: "list[Monkey]", rounds: int):
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items.copy():
                worry_level = increase_worry_level(item, monkey.operation)
                worry_level //= 3

                next_monkey = monkey.next_monkey[0 == worry_level % monkey.divisible_by]

                monkey.items.pop(0)
                monkeys[next_monkey].items.append(worry_level)
                monkey.items_inspected += 1

    most_active_inspections = [x.items_inspected for x in get_most_active(monkeys)[:2]]
    return reduce(operator.mul, most_active_inspections)


if __name__ == "__main__":
    data = load_data("input.txt")
    print(f"Answer to Q1 is {process_monkeys(data,20)}")
