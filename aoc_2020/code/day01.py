from pathlib import Path
from os.path import dirname, realpath
_DAY = "01"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    # convert each line to int and store it in array
    lines = [int(line.replace("\n", "")) for line in f.readlines()]


####################################################################################################
def part_a(wanted_sum: int) -> int:
    """Part A: Searches for 2 numbers that sum up to 'wanted_sum' and returns their product"""
    # 2 nested for loops
    for i in range(lines.__len__()):
        for j in range(lines.__len__()):
            # don't check numbers against themselves (i!=j)
            if i != j and lines[i] + lines[j] == wanted_sum:
                # if the numbers add up to wanted_sum
                return lines[i] * lines[j]


def part_b(wanted_sum: int) -> int:
    """Part B: Searches for 3 numbers that sum up to 'wanted_sum' and returns their product"""
    # 3 nested for loops
    for i in range(lines.__len__()):
        for j in range(lines.__len__()):
            for k in range(lines.__len__()):
                # don't check numbers against themselves
                if i != j and i != k and j != k:
                    # if the numbers add up to wanted_sum
                    if lines[i] + lines[j] + lines[k] == wanted_sum:
                        return lines[i] * lines[j] * lines[k]


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a(2020)))
print("Part B: " + str(part_b(2020)))
print(28 * "-")
