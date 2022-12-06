def find_marker(buffer: str, unique: int) -> int:
    pos = unique
    window = set(buffer[:pos])

    while len(window) < unique:
        pos += 1
        window = set(buffer[pos - unique : pos])
    return pos


with open("day06-input.txt", "r") as f:
    data = f.readline().strip()
    stream_length_v1 = find_marker(data, 4)
    stream_length_v2 = find_marker(data, 14)

print(f"Q1 answer is: {stream_length_v1}")
print(f"Q2 answer is: {stream_length_v2}")


assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11
assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26
