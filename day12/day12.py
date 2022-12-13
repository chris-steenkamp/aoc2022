from dataclasses import dataclass
from queue import SimpleQueue
import sys
from copy import deepcopy

START = None
END = None


@dataclass
class Node:
    location: tuple
    label: str
    height: int
    edges: "list[Node]"
    distance: int = -1
    previous: "Node" = None


def translate(elevation: str) -> int:
    return (
        ord("a")
        if elevation == "S"
        else ord("z")
        if elevation == "E"
        else ord(elevation)
    )


def load_data(path):
    global START, END

    def get_edges(x, y, current):
        edges = []

        current = translate(current)

        if y > 0:
            up = translate(data[y - 1][x])
            if up - current <= 1:
                edges.append((x, y - 1))

        if y < len(data) - 1:
            down = translate(data[y + 1][x])
            if down - current <= 1:
                edges.append((x, y + 1))

        if x > 0:
            left = translate(data[y][x - 1])
            if left - current <= 1:
                edges.append((x - 1, y))

        if x < len(data[y]) - 1:
            right = translate(data[y][x + 1])
            if right - current <= 1:
                edges.append((x + 1, y))

        return edges

    with open(path, "r") as f:
        data = [l.strip() for l in f.readlines()]

    g = {}

    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            edges = get_edges(x, y, cell)
            location = (x, y)
            node = Node(location, cell, translate(cell), edges)
            g[location] = node

            if "S" == cell:
                START = node
                node.distance = 0
            elif "E" == cell:
                END = node

    return g


def BFS(g):
    q = SimpleQueue()
    q.put(START)

    while not q.empty():
        current: Node = q.get(block=False)

        for next_node in [g[n] for n in current.edges]:
            if next_node == END:
                path = []
                while current is not None:
                    path.append(current)
                    current = current.previous
                return path

            distance = current.distance + 1

            if next_node.distance == -1 or next_node.distance > distance:
                next_node.distance = distance
                next_node.previous = current

                q.put(next_node)

    return []


def BFS_v2(g):
    a_s = {k: v for k, v in g.items() if v.label == "a"}

    min = sys.maxsize

    for a in deepcopy(a_s).values():
        found_solution = False
        a.distance = 0
        q = SimpleQueue()
        q.put(a)

        while not q.empty() and not found_solution:
            current: Node = q.get(block=False)

            for next_node in [g[n] for n in current.edges]:
                if next_node == END:
                    path = []
                    while current is not None:
                        path.append(current)
                        current = current.previous

                    if len(path) < min:
                        min = len(path)

                    found_solution = True
                    break

                distance = current.distance + 1

                if next_node.distance == -1 or next_node.distance > distance:
                    next_node.distance = distance
                    next_node.previous = current

                    q.put(next_node)

    return min


if __name__ == "__main__":
    data = load_data("input.txt")
    print(f"Anwer to Q1 is {len(BFS(data))}")

    data = load_data("input.txt")
    print(f"Anwer to Q2 is {BFS_v2(data)}")
