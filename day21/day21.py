import pathlib
from os import path
import re
import operator

LINE = re.compile("(\w{4}): (\d+|(.*))")
EXPR = re.compile("(\w{4}) ([+-/\*]) (\w{4})")
FN_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
    "*": operator.mul,
}


def load_data(path: str):
    def get_node(value: str):
        try:
            int(value)
            node = {"left": None, "op": lambda x, y: int(value), "right": None}
        except ValueError:
            expr = EXPR.search(value).groups()
            node = {"left": expr[0], "op": FN_MAP[expr[1]], "right": expr[2]}

        return node

    with open(path) as f:
        data = [l.strip() for l in f.readlines()]

    expr_tree = {}
    for line in data:
        parts = LINE.search(line).groups()
        expr_tree[parts[0]] = get_node(parts[1])
    return expr_tree


def calculate(expr_tree: dict, start: str) -> float:

    if start is None:
        return 0

    left = expr_tree[start]["left"]
    right = expr_tree[start]["right"]

    return expr_tree[start]["op"](
        calculate(expr_tree, left), calculate(expr_tree, right)
    )


if __name__ == "__main__":
    data = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))
    print(f"Q1 answer is {calculate(data, 'root')}")
