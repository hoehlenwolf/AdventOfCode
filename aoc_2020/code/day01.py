from pathlib import Path
from os.path import dirname, realpath
from time import time_ns

_DAY = "01"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")

# load puzzle input
lines = []


def load_puzzle():
    global lines
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
            if i == j:
                break
            for k in range(lines.__len__()):
                # don't check numbers against themselves
                if i != j and i != k and j != k:
                    # if the numbers add up to wanted_sum
                    if lines[i] + lines[j] + lines[k] == wanted_sum:
                        return lines[i] * lines[j] * lines[k]


def run():
    """Runs this day's solution and returns a tuple

    (result part A,
    Result part B,
    time for setup,
    time for part A,
    time for part B)

    """
    # Setup
    time_start_setup = time_ns()
    load_puzzle()
    time_setup = time_ns() - time_start_setup

    # Part A
    time_start_a = time_ns()
    result_a = part_a(2020)
    time_a = time_ns() - time_start_a

    # Part B
    time_start_b = time_ns()
    result_b = part_b(2020)
    time_b = time_ns() - time_start_b

    return result_a, result_b, time_setup, time_a, time_b


if __name__ == "__main__":
    a, b, _, _, _ = run()
    print("Part A: " + str(a))
    print("Part B: " + str(b))
