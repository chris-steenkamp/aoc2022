import pathlib
from os import path
from itertools import cycle
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node" = None
    prev: "Node" = None


@dataclass
class CircularList:
    tail: Node = None
    length: int = 0

    @property
    def head(self) -> Node:
        if self.is_empty():
            return None

        return self.tail.next

    def is_empty(self) -> bool:
        return self.tail is None

    def push_left(self, value: int):
        if self.is_empty():
            self.tail = Node(value)
            self.tail.next = self.tail
            self.tail.prev = self.tail
        else:
            node = Node(value, self.head, self.tail)
            self.head.prev = node
            self.tail.next = node

        self.length += 1

    def push_right(self, value: int):
        if self.is_empty():
            self.tail = Node(value)
            self.tail.next = self.tail
            self.tail.prev = self.tail
        else:
            node = Node(value, self.head, self.tail)
            self.head.prev = node
            self.tail.next = node
            self.tail = node

        self.length += 1

    def print_list(self, reverse: bool = False):
        if self.is_empty():
            return ""

        s = ""
        start = self.tail if reverse else self.head
        end = self.head if reverse else self.tail
        while start != end:
            s += f"{start.value}, "
            start = start.prev if reverse else start.next

        return s + str(end.value)

    def __str__(self) -> str:
        return self.print_list()


def load_data(path: str) -> "CircularList":
    data = CircularList()
    with open(path) as f:
        for value in [int(l.strip()) for l in f.readlines()]:
            data.push_right(value)
    return data


def unmix(coordinates: CircularList) -> CircularList:
    positions = convert_to_list(coordinates)

    for ix, node in enumerate(positions):
        # move node left or right by its value
        if node.value > 0:
            for _ in range(node.value):
                next_node = node.next
                previous_node = node.prev

                node.prev = next_node
                node.next = next_node.next
                node.next.prev = node

                next_node.next = node
                next_node.prev = previous_node

                previous_node.next = next_node
        elif node.value < 0:
            for _ in range(abs(node.value)):
                next_node = node.next
                previous_node = node.prev

                node.prev = previous_node.prev
                node.next = previous_node
                node.prev.next = node

                previous_node.next = next_node
                next_node.prev = previous_node

                previous_node.prev = node
        # Shift the node to the end of the list, rather than have it at
        # the beginning. The ordering in the list is the same either way.
        if node == coordinates.head:
            coordinates.tail = node

    return coordinates


def convert_to_list(coordinates):
    positions: "list[Node]" = []
    head = coordinates.head
    while head != coordinates.tail:
        positions.append(head)
        head = head.next

    positions.append(coordinates.tail)
    return positions


def get_grove_coordinates(coordinates: CircularList) -> int:
    mixed_cycle = cycle(convert_to_list(coordinates))

    coords = []
    p = next(mixed_cycle).value
    while p != 0:
        p = next(mixed_cycle).value
        if p == 0:
            break

    for _ in range(3):
        for _ in range(1000):
            p = next(mixed_cycle)

        coords.append(p.value)

    return sum(coords)


if __name__ == "__main__":
    data = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))
    print(f"Q1 answer is {get_grove_coordinates(unmix(data))}")
