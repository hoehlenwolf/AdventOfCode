from os.path import dirname, realpath
from pathlib import Path
from math import floor
_DAY = "01"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [int(line.replace("\n", "")) for line in f.readlines()]


####################################################################################################
def part_a():
    """Part A"""
    # required fuel
    fuel = 0
    # loop through all lines in puzzle input
    for line in lines:
        # take mass, divide by 3, floor and subtract 2 to get fuel per module
        # add it all together
        fuel += floor(line/3) - 2
    return fuel


def part_b():
    """Part B"""
    # required fuel
    fuel = 0
    # loop through all lines in puzzle input
    for line in lines:
        # calculate the added fuel for module mass
        adding = floor(line/3) - 2
        # add fuel for the weight of the previously added fuel (if it was >0)
        while adding > 0:
            fuel += adding
            adding = floor(adding/3) - 2
    return fuel


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")