from collections import defaultdict

elves = defaultdict(list)
with open("day01-input.txt", "r") as f:
    counter = 0

    for l in f.readlines():
        if l.strip() == "":
            counter += 1
        else:
            elves[counter].append(int(l))


elves_calories = {k: sum(v) for k, v in elves.items()}
sorted_elves = sorted(elves_calories.items(), key=lambda x: x[1], reverse=True)

print(f"first answer is: {sorted_elves[0][1]}")
print(f"second answer is: {sum(x[1] for x in sorted_elves[0:3])}")
