import pathlib
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from os import path

BLUEPRINT_RE = re.compile(
    "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)

MAX_GEODES_MINED = defaultdict(int)
# PATHS = []


class RobotType(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class Robot:
    robot_type: RobotType
    blueprint_id: int
    ore: int
    clay: int
    obsidian: int


class RobotFactory:
    id: int
    blueprint: dict

    def __init__(self, blueprint: str) -> None:
        robot_costs = list(map(int, BLUEPRINT_RE.search(blueprint).groups()))

        self.id = robot_costs[0]
        self.blueprint = {
            RobotType.ORE: {"ore": robot_costs[1]},
            RobotType.CLAY: {"ore": robot_costs[2]},
            RobotType.OBSIDIAN: {"ore": robot_costs[3], "clay": robot_costs[4]},
            RobotType.GEODE: {"ore": robot_costs[5], "obsidian": robot_costs[6]},
        }

    def create_robot(self, robot_type: RobotType) -> Robot:
        specs = self.blueprint[robot_type]
        return Robot(
            robot_type,
            self.id,
            specs.get("ore", 0),
            specs.get("clay", 0),
            specs.get("obsidian", 0),
        )


def load_data(path: str) -> "list[RobotFactory]":
    with open(path) as f:
        factories = [RobotFactory(l.strip()) for l in f.readlines()]

    return factories


def create_robot(
    factory: RobotFactory, robot_type: RobotType, minerals: "list[int]"
) -> "tuple[bool, list[int]]":
    robot = factory.create_robot(robot_type)
    if (
        robot.ore > minerals[0]
        or robot.clay > minerals[1]
        or robot.obsidian > minerals[2]
    ):
        return False, minerals

    return True, [
        minerals[0] - robot.ore,
        minerals[1] - robot.clay,
        minerals[2] - robot.obsidian,
        minerals[3],
    ]


def get_weighted_sum(minerals) -> int:
    return (
        minerals[0]
        + (minerals[1] * 1000)
        + (minerals[2] * 1000000)
        + (minerals[3] * 1000000000)
    )


def dfs(
    factory: RobotFactory,
    time_remaining: int,
    robots: "tuple[int,int,int,int]",
    minerals: "tuple[int,int,int,int]",
    visited,
    # current_path: str,
):
    global MAX_GEODES_MINED
    # global PATHS

    if time_remaining == 0:
        MAX_GEODES_MINED[factory.id] = max(MAX_GEODES_MINED[factory.id], minerals[3])
        # PATHS.append((minerals[3], current_path))
        return

    if visited.get((robots, time_remaining), -1) >= get_weighted_sum(minerals):
        return

    visited[robots, time_remaining] = get_weighted_sum(minerals)

    for try_create_robot in [True, False]:
        if try_create_robot:
            for t in RobotType:
                robot_created, new_minerals = create_robot(factory, t, minerals)
                if not robot_created:
                    continue

                # increase each mineral by one for each robot that we had
                # when we started the loop
                new_minerals = [x + y for x, y in zip(new_minerals, robots)]

                # increase the number of robots of type `t`
                new_robots = tuple(
                    robot + (1 if i == t.value else 0) for i, robot in enumerate(robots)
                )
                dfs(
                    factory,
                    time_remaining - 1,
                    new_robots,
                    new_minerals,
                    visited,
                    # f"{current_path}/{new_robots},{new_minerals}",
                )
        else:
            new_minerals = [x + y for x, y in zip(minerals, robots)]
            dfs(
                factory,
                time_remaining - 1,
                robots,
                new_minerals,
                visited,
                # f"{current_path}/{robots},{new_minerals}",
            )


if __name__ == "__main__":
    data = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))

    starting_minerals = [0, 0, 0, 0]
    robots = (1, 0, 0, 0)

    # dfs(data[1], 24, robots, starting_minerals, {}, "(1, 0, 0, 0),[0, 0, 0, 0]")
    # w, p = sorted(PATHS)[-1]

    for i in range(len(data)):
        dfs(data[i], 24, robots, starting_minerals, {})

    print(f"Q1 answer is {sum([k * v for k,v in MAX_GEODES_MINED.items()])}")

    # reset calculated max values
    MAX_GEODES_MINED = defaultdict(int)

    for i in range(3):
        dfs(data[i], 32, robots, starting_minerals, {})

    prod = 1
    for v in MAX_GEODES_MINED.values():
        prod *= v

    print(f"Q2 answer is {prod}")
