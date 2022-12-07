from collections import defaultdict

test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()

stack = []
dirs = defaultdict(int)


def get_size():
    total = sum(map(lambda x: x[1], filter(lambda x: x[1] <= 100000, dirs.items())))

    return total


def parse_command(cmd: str) -> int:
    def parse_input_command(c):
        _, cmd, arg = c.split(" ")
        if "cd" == cmd:
            if ".." == arg:
                stack.pop()
            else:
                stack.append(arg)

    def parse_file(c: str):
        size, _ = c.split(" ")
        for i in range(len(stack)):
            dirs[tuple(stack[: i + 1])] += int(size)

    if cmd.startswith("$ cd"):
        parse_input_command(cmd)
    elif cmd.startswith("dir") or cmd.startswith("$ ls"):
        pass
    else:
        parse_file(cmd)


with open("day07-input.txt", "r") as f:
    commands = [l.rstrip() for l in f.readlines()]


for c in commands:
    parse_command(c)

print(f"Q1 answer is {get_size()}")

used_space = dirs[("/",)]
total_space = 70000000
free_space = total_space - used_space
required_space = 30000000
min_dir_size = required_space - free_space

print(f"Q2 answer is {min(filter(lambda x: x >= min_dir_size, dirs.values()))}")


assert get_size() == 95437
