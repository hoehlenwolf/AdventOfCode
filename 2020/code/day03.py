from pathlib import Path
from os.path import dirname, realpath
_DAY = "03"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def part_a():
    """Part A"""
    return count_trees(3, 1)


def part_b():
    """Part B"""
    # product of trees encountered on different slopes
    prod = 1
    # slopes (right,down)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    # loop through all the slopes to check
    for s_right, s_down in slopes:
        # multiply the trees encountered in each slope
        prod *= count_trees(s_right, s_down)
    return prod


def count_trees(s_right, s_down):
    """Counts the trees you encounter when following a slope of s_right to the right and s_down down"""
    # current position
    curr_x = 0
    curr_y = 0
    # width of the puzzle input (repeated after that)
    repeating = lines[0].__len__()
    # encountered trees
    trees = 0
    # traverse the puzzle input (repeated infinitely to the right) to the bottom
    while curr_y < lines.__len__():
        # if not yet reached the bottom and there's a '#' in the array, you encounter a tree
        if lines[curr_y][curr_x % repeating] == '#':
            trees += 1
        # modify current position
        curr_x += s_right
        curr_y += s_down
    return trees


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
