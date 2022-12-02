weights = {"r": 1, "p": 2, "s": 3}

points = {"win": 6, "draw": 3, "lost": 0}

beats = {"r": "s", "p": "r", "s": "p"}

opp_map = {"A": "r", "B": "p", "C": "s"}
you_map = {"X": "r", "Y": "p", "Z": "s"}
v2 = {"X": "lost", "Y": "draw", "Z": "win"}


def outcome_v1(turn) -> int:
    opponent = opp_map[turn[0]]
    you = you_map[turn[1]]

    if you == beats[opponent]:
        outcome = "lost"
    elif you == opponent:
        outcome = "draw"
    else:
        outcome = "win"

    return points[outcome] + weights[you]


def outcome_v2(turn) -> int:
    opponent = opp_map[turn[0]]
    you = turn[1]
    outcome = v2[you]

    if outcome == "draw":
        # Choose the same hand as the opponent
        hand = opponent
    elif outcome == "lost":
        # Choose the hand that the opponent will beat
        hand = beats[opponent]
    else:
        # Find the hand that beats the opponent's hand
        hand = list(filter(lambda x: x[1] == opponent, beats.items()))[0][0]

    return points[outcome] + weights[hand]


with open("day02-input.txt", "r") as f:
    data_v1 = [outcome_v1(l.strip().split(" ")) for l in f.readlines()]

print(sum(data_v1))

with open("day02-input.txt", "r") as f:
    data_v2 = [outcome_v2(l.strip().split(" ")) for l in f.readlines()]

print(sum(data_v2))
