from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "09"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [int(line.replace("\n", "")) for line in f.readlines()]


####################################################################################################
def find_sum_pair(preamble: list, target: int) -> (int, int):
    """Searches for 2 distinct number within a `preamble` to add up to the `target`"""
    # for every possible number n2
    for n1 in preamble:
        # for every possible number n2
        for n2 in preamble:
            # if n1 and n2 are distinct and they add up to the `target`
            if n1 != n2 and target == n1 + n2:
                # return them
                return n1, n2
    # if no such pair found
    return None


def find_contiguous_group(group_size: int, invalid_number: int):
    """Method to find a contiguous group of `group_size` within lines, summing up to `invalid_number`"""
    # go through all possible starting indices
    for i in range(0, lines.__len__()):
        # get contiguous set of size `group_size`
        contiguous_set = lines[i:i + group_size]
        # if they all sum up to the passed `invalid_number`
        if sum(contiguous_set) == invalid_number:
            # return the sum of the smallest and biggest number in that group
            return max(contiguous_set) + min(contiguous_set)
    return None


def part_a():
    """Part A"""
    # length of preamble (group of previous numbers where 2 have to sum current number)
    preamble_len = 25
    # loop through all indices for which there must be 2 numbers adding up to the number at the index
    for start_index in range(preamble_len, lines.__len__()):
        # current number
        target = lines[start_index]
        # find pair of numbers to add up to target within the previous `preamble_len` numbers
        result = find_sum_pair(lines[start_index - preamble_len: start_index], target)
        # if no such pair found
        if result is None:
            # return the current (invalid) number
            return target


def part_b(invalid_number: int):
    """Part B"""
    # NOTE: this is kinda exploiting the fact, that the group_size for the/my solution is relatively small (17)
    # to get a faster result I start with group size 3 (because Part A failed for that number 2 can't be an option)
    # and push this "group window" over the number-array and increment group_size
    # Thus reaching the solution (with group_size=17) relatively fast.
    # Significantly faster (about 15x) than two nested loops
    # for start_index in range(0,lines.__len__()):
    # for end_index in range(start_index + 3, lines.__len__())

    # loop through possible group sizes (at least 3 numbers, because number did not pass Part A)
    for i in range(3, lines.__len__()):
        # try to find a contiguous set of size i of numbers adding up to invalid_number
        result = find_contiguous_group(i, invalid_number)
        # if found
        if result is not None:
            # return it
            return result


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
    result_a = part_a()
    time_a = time_ns() - time_start_a

    # Part B
    time_start_b = time_ns()
    result_b = part_b(result_a)
    time_b = time_ns() - time_start_b

    return result_a, result_b, time_setup, time_a, time_b


if __name__ == "__main__":
    a, b, _, _, _ = run()
    print("Part A: " + str(a))
    print("Part B: " + str(b))
