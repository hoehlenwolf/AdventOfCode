from os.path import dirname, realpath
from pathlib import Path
_DAY = "15"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
    # extract all starting numbers from the first line (comma separated)
    starting_numbers = [int(nr) for nr in lines[0].split(",")]


####################################################################################################
def calc_nth_number(n: int) -> int:
    """Calculates the `n`-th spoken number"""
    # dict with spoken numbers consisting of key:value pairs (number: spoken_last_in_turn_number)
    spoken_numbers = dict()
    # previous number that was spoken (initialized with -1)
    prev_num = -1
    # add starting numbers with their appropriate turn number they were spoken to the dict
    # indices shifted one up, because turns start at 1 not 0
    for i in range(1, starting_numbers.__len__() + 1):
        spoken_numbers[starting_numbers[i - 1]] = i
        # update the most recently spoken number accordingly
        prev_num = starting_numbers[i - 1]
    # loop through given n iterations (starting with already added starting numbers, indices shifted 1 up)
    for i in range(starting_numbers.__len__() + 1, n + 1):
        # if number spoken in last round has been spoken before
        if prev_num in spoken_numbers:
            # get the last time (turn number) it was spoken before that
            previous = spoken_numbers[prev_num]
        # if number has not been spoken before the previous turn
        else:
            # turn in which prev_number was previously spoken (is the turn before the current one in this case,
            # because no earlier time exists)
            previous = i - 1
        # modify the turn number the prev_num was most recently spoken to the last turn's number
        spoken_numbers[prev_num] = i - 1
        # previously spoken number (for next round) is the difference between the last turn's number (where old
        # 'prev_num' has been spoken) and the turn number in which the old 'prev_num' was spoken *before* that
        prev_num = (i-1) - previous
    # return the n-th number spoken (prev_number for n+1-th turn)
    return prev_num


def part_a():
    """Part A"""
    return calc_nth_number(2020)


def part_b():
    """Part B"""
    return calc_nth_number(30000000)


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
