from os.path import dirname, realpath
from pathlib import Path
from sys import platform
import ctypes
from time import time_ns

_DAY = "15"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []
starting_numbers = []


def load_puzzle():
    global lines, starting_numbers
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
        # extract all starting numbers from the first line (comma separated)
        starting_numbers = [int(nr) for nr in lines[0].split(",")]


####################################################################################################
def calc_nth_number_slow(n: int) -> int:
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
        prev_num = (i - 1) - previous
    # return the n-th number spoken (prev_number for n+1-th turn)
    return prev_num


def calc_nth_number(n: int) -> int:
    # try to use the lightning fast (~20x speedup) C-function (day15.c) compiled as a dynamic library
    # ("day15_win.dll" on Windows/ "day15_linux.so" on Linux)
    try:
        # create type for int array if appropriate length (len(starting_numbers))
        c_int_array = ctypes.c_int * starting_numbers.__len__()
        # fill it with the starting values extracted from inputs/day15_input.txt
        c_starting_numbers = c_int_array(*starting_numbers)
        # if on windows
        if platform == "win32":
            c_calc_nth_number = ctypes.CDLL(str(Path(dirname(realpath(__file__))) / "day15_win.dll"))
        else:  # otherwise
            c_calc_nth_number = ctypes.CDLL(str(Path(dirname(realpath(__file__))) / "day15_linux.so"))
        # call the function calcNthNumber in the Library
        c_calc_nth_number.calcNthNumber.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
        result = c_calc_nth_number.calcNthNumber(n, c_starting_numbers, starting_numbers.__len__())
    except:
        print("Error: Lightning fast C-Solution for Day 15 could not be loaded via ctypes. Make sure a compiled .dll "
              "or .so file exists in aoc_2020/code/ named day15_win.dll or day15_linux.so")
        print("The Makefile in the root directory should work for Windows and Linux, if you have cl.exe or gcc "
              "installed")
        print("Falling back to slow python-only solution")
        # if something failed, use the slow python version of the function
        result = calc_nth_number_slow(n)
    return result


def part_a():
    """Part A"""
    return calc_nth_number(2020)


def part_b():
    """Part B"""
    return calc_nth_number(30000000)


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
    result_b = part_b()
    time_b = time_ns() - time_start_b

    return result_a, result_b, time_setup, time_a, time_b


if __name__ == "__main__":
    a, b, _, _, _ = run()
    print("Part A: " + str(a))
    print("Part B: " + str(b))
