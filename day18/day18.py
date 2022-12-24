import pathlib
from collections import defaultdict
from itertools import product
from os import path

vertices = list(product([0, 1], repeat=3))


def load_data(path: str) -> "list[set[tuple[int,int,int]]]":
    def generate_vertices(point: "tuple[int,int,int]") -> "tuple[int,int,int]":
        return set(tuple(x + y for x, y in zip(point, n)) for n in vertices)

    with open(path, "r") as f:
        cubes = set(tuple(int(p) for p in l.strip().split(",")) for l in f.readlines())

    return (
        [generate_vertices(cube) for cube in cubes],
        cubes,
        min([min(p) for p in cubes]),
        max([max(p) for p in cubes]),
    )


def check_surface_area(cubes) -> int:
    shared_sides = defaultdict(int)
    for i, cube in enumerate(cubes):
        for j, check in enumerate(cubes):
            if i != j:
                shared_sides[i] += len(cube.intersection(check)) // 4

    return sum(6 - x for x in shared_sides.values())


def check_surface_area_v2(
    cubes: "set[tuple[int,int,int]]",
    start: "tuple[int,int,int]",
    min_val: int,
    max_val: int,
) -> int:
    free_sides = 0
    queue = [start]
    visited = set()

    while queue:
        current = queue.pop(0)
        visited.add(current)
        for delta in [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
        ]:
            next_node = tuple(x + y for x, y in zip(current, delta))

            if (
                min_val <= next_node[0] <= max_val
                and min_val <= next_node[1] <= max_val
                and min_val <= next_node[2] <= max_val
                and next_node not in visited
                and next_node not in queue
            ):
                if next_node in cubes:
                    free_sides += 1
                else:
                    queue.append(next_node)

    return free_sides


if __name__ == "__main__":
    cubes, origins, min_val, max_val = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt")
    )
    print(f"Q1 answer is {check_surface_area(cubes)}")
    print(
        f"Q1 answer is {check_surface_area_v2(origins, (0,0,0), min_val - 1, max_val + 1)}"
    )
