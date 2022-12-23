import pathlib
from collections import defaultdict
from itertools import product
from os import path

vertices = list(product([0, 1], repeat=3))


def load_data(path: str) -> "list[set[tuple[int,int,int]]]":
    def generate_vertices(point: "tuple[int,int,int]") -> "tuple[int,int,int]":
        return set(tuple(x + y for x, y in zip(point, n)) for n in vertices)

    with open(path, "r") as f:
        cubes = [
            generate_vertices(tuple(int(p) for p in l.strip().split(",")))
            for l in f.readlines()
        ]

    return cubes


def check_surface_area(cubes) -> int:
    shared_sides = defaultdict(int)
    for i, cube in enumerate(cubes):
        for j, check in enumerate(cubes):
            if i != j:
                shared_sides[i] += len(cube.intersection(check)) // 4

    return sum(6 - x for x in shared_sides.values())


if __name__ == "__main__":
    cubes = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))
    print(f"Q1 answer is {check_surface_area(cubes)}")
