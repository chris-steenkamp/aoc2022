def load_data(path):
    with open(path, "r") as f:
        data = []
        for line in f:
            ops = line.strip("\n").split(" ")
            data.append((ops[0], int(ops[1] if len(ops) > 1 else 0)))

    return data


def get_cycle_count(data):
    count = 0
    for instruction, _ in data:
        if "noop" == instruction:
            count += 1
            continue

        if "addx" == instruction:
            for _ in range(2):
                count += 1

    return count


def check_count(count):
    return (count + 20) % 40 == 0


def get_signal_strength(data):
    count = 0
    x = 1
    strengths = []
    for instruction, arg in data:
        if "noop" == instruction:
            count += 1
            if check_count(count):
                print(f"Instruction count is {count}")
                strengths.append(count * x)
            continue

        if "addx" == instruction:
            for i in range(2):
                count += 1
                if check_count(count):
                    print(f"Instruction count is {count}")
                    strengths.append(count * x)
                if 1 == i:
                    x += arg

    return sum(strengths)


if __name__ == "__main__":
    data = load_data("day10-input.txt")
    # print(f"Q1 signal strength is {sum(get_signal_strength(data))}")
