from queue import SimpleQueue
from dataclasses import dataclass
from copy import deepcopy
import pathlib
from os import path
import re

line = re.compile(
    r"^Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)

PATHS = []


@dataclass
class Node:
    label: str
    rate: int
    edges: list
    distance: int = -1
    previous: "Node" = None

    def __hash__(self) -> int:
        return self.label.__hash__()

    def __eq__(self, __o: object) -> bool:
        return self.label.__eq__(__o)


def load_data(path: str):
    valves = {}
    with open(path, "r") as f:
        for l in f.readlines():
            name, rate, links = line.search(l.strip()).groups()
            valves[name] = Node(name, int(rate), links.split(", "))

    return valves


def dfs(valves, node, depth, opened, visited, total_pressure, path):
    def calc_pressure():
        return sum(valves[v].rate for v in opened)

    global PATHS

    if depth == 1:
        PATHS.append((total_pressure, path))
        return

    # if we've already tried this node at this depth and the calculated
    # pressure was higher, then no need to explore this path further.
    if visited.get((node, depth), -1) >= total_pressure:
        return

    visited[node, depth] = total_pressure

    for should_open in [True, False]:
        if should_open:
            if node in opened or valves[node].rate <= 0:
                continue

            opened.add(node)

            dfs(
                valves,
                node,
                depth - 1,
                opened,
                visited,
                total_pressure + calc_pressure(),
                # calculating the total pressure that opening the valve
                # contributes until t = 1 is not working for some reason,
                # so rather calculate how much all open valves contribute
                # at each step.
                # total_pressure + ((depth - 1) * valves[node].rate),
                f"{path}/{node}",
            )

            opened.remove(node)
        else:
            for next_node in valves[node].edges:
                dfs(
                    valves,
                    next_node,
                    depth - 1,
                    opened,
                    visited,
                    total_pressure + calc_pressure(),
                    f"{path}/{next_node}",
                )


if __name__ == "__main__":
    valves = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )

    dfs(valves, "AA", 30, set(), {}, 0, "AA")
    w, p = sorted(PATHS)[-1]
    print(f"Q1 max pressure is {w} at path {p}")
