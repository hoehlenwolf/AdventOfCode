from os.path import dirname, realpath
from pathlib import Path
_DAY = "10"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [int(line.replace("\n", "")) for line in f.readlines()]
    # append outlet joltage
    lines.append(0)
    # sort them (ascending)
    lines.sort()


####################################################################################################
def count_possibilities(at_index: int, results: dict) -> dict:
    """Recursively counts all possibilities to reach a certain position in the
    sorted list of joltages (puzzle input: lines)"""
    # if end of file reached
    if at_index >= lines.__len__():
        # return the recursively calculated results-dict
        return results
    # otherwise: current number is = lines[at_index]
    current = lines[at_index]
    # loop through all possible successors (max 3 or less if file ends before that)
    for i in range(at_index + 1, min(at_index + 4, lines.__len__())):
        # if position 'i' can be reached by going via `at_index` position
        if lines[i] - current <= 3:
            # increase the possibilities to reach position 'i' by the possibilities to reach the current position
            # `at_index`
            results[i] += results[at_index]
    # recursively do the same for next `at_index` passing the modified `results`-dict
    return count_possibilities(at_index + 1, results)


def part_a():
    """Part A"""
    # dictionary of found joltage differences
    diffs = dict()
    # initialize possible differences with 0
    diffs[1] = 0
    diffs[2] = 0
    diffs[3] = 0
    # loop through all numbers in sorted puzzle input
    for i in range(1, lines.__len__()):
        # calculate difference between current and previous number and increase the corresponding dict-field by 1
        diffs[lines[i]-lines[i-1]] += 1
    # add your own joltage adapter (3 higher than the highest, so joltage difference = 3)
    diffs[3] += 1
    # return number of 1-joltage-diffs multiplied by number of 3-joltage-diffs
    return diffs[1]*diffs[3]


def part_b():
    """Part B"""
    # make a dictionary with possibilities (possibilities[5] = number of unique ways to reach joltage at lines[i]
    # (Note: lines has to be sorted!)
    possibilities = dict()
    # initialize all possible dict fields with 0
    for i in range(0, lines.__len__()):
        possibilities[i] = 0
    # for position 0 there is only one way to reach it
    possibilities[0]=1
    # count possibilities from position 0 starting, passing initialized dict
    result = count_possibilities(0, possibilities)
    # return the possibilities to reach the last position
    return result[(max(result))]


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
