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


def load_data(path: str, decryption_key: int = 1) -> "CircularList":
    data = CircularList()
    with open(path) as f:
        for value in [int(l.strip()) * decryption_key for l in f.readlines()]:
            data.push_right(value)
    return data


def mix(coordinates: CircularList) -> CircularList:
    positions = convert_to_list(coordinates)

    for node in positions:
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


def mix_v2(coordinates: CircularList, repetitions: int = 1) -> "list[Node]":
    # Use direct array manipulation because it is much faster.
    # Also convert the heavy Node class to a lightweight list (~60 secs -> ~6 secs)
    lightweight_list = [
        (n.value, ix) for ix, n in enumerate(convert_to_list(coordinates))
    ]
    mixed_list = list(lightweight_list)

    for _ in range(repetitions):
        for node in lightweight_list:
            ix = mixed_list.index(node)
            mixed_list.pop(ix)
            new_ix = (ix + node[0]) % len(mixed_list)
            mixed_list.insert(new_ix, node)

    return mixed_list


def get_grove_coordinates(coordinates) -> int:
    if isinstance(coordinates, CircularList):
        mixed_cycle = cycle([n.value for n in convert_to_list(coordinates)])
    else:
        mixed_cycle = cycle([n[0] for n in coordinates])

    while next(mixed_cycle) != 0:
        pass

    coords = []

    for _ in range(3):
        for _ in range(1000):
            p = next(mixed_cycle)

        coords.append(p)

    return sum(coords)


if __name__ == "__main__":
    data = load_data(path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"))
    print(f"Q1 answer is {get_grove_coordinates(mix_v2(data))}")

    data = load_data(
        path.join(pathlib.Path(__file__).parent.resolve(), "input.txt"), 811589153
    )
    print(f"Q2 answer is {get_grove_coordinates(mix_v2(data, 10))}")
