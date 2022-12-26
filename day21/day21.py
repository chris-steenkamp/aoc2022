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
    "=": operator.eq,
}

captures = {}


def load_data(path: str):
    def get_node(value: str):
        try:
            int(value)
            node = {
                "left": None,
                "op": lambda x, y: int(value),
                "right": None,
                "label": value,
            }
        except ValueError:
            expr = EXPR.search(value).groups()
            node = {
                "left": expr[0],
                "op": FN_MAP[expr[1]],
                "right": expr[2],
                "label": expr[1],
            }

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
        calculate(expr_tree, left),
        calculate(expr_tree, right),
    )


def create_expression(expr_tree: dict, start: str) -> float:

    left = expr_tree[start]["left"]
    right = expr_tree[start]["right"]

    if left is None or right is None:
        return str(expr_tree[start]["op"](left, right))

    left_val = create_expression(expr_tree, left)
    right_val = create_expression(expr_tree, right)

    replace = None
    try:
        replace = f"{FN_MAP[expr_tree[start]['label']](int(left_val), int(right_val))}"
    except ValueError:
        replace = f"({left_val}{expr_tree[start]['label']}{right_val})"

    return replace


if __name__ == "__main__":
    expr_tree = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )
    print(f"Q1 answer is {calculate(expr_tree, 'root')}")

    expr_tree["root"]["op"] = operator.eq
    expr_tree["humn"]["op"] = lambda x, y: 3757272361782
    print(f"Q2 answer is {calculate(expr_tree, 'root')}")
