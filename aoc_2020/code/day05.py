from pathlib import Path
from os.path import dirname, realpath
from time import time_ns

_DAY = "05"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def get_seat_pos(binary_code: str) -> (int, int):
    """Converts a given binary seat code to it's seat id"""
    # lower and upper column/row number of region in which the seat is in
    lower_row = 0
    upper_row = 127
    lower_col = 0
    upper_col = 7
    # number of columns / rows in that region
    row_range = upper_row - lower_row + 1
    col_range = upper_col - lower_col + 1
    # loop through given code step by step
    for code in binary_code:
        # if in the front part
        if code == "F":
            # modify upper_row accordingly
            upper_row -= row_range / 2
        if code == "B":
            # modify lower_row accordingly
            lower_row += row_range / 2
        if code == "L":
            # modify upper_col accordingly
            upper_col -= col_range / 2
        if code == "R":
            # modify lower_col accordingly
            lower_col += col_range / 2
        # if code was there to divide into right/left
        if code == "R" or code == "L":
            # adjust the col_range (halved every step)
            col_range /= 2
        # if code was there to divide into front/back
        if code == "F" or code == "B":
            # adjust the row_range (halved every step)
            row_range /= 2
    # assert that a certain seat has been found (lower and upper values should be the same)
    assert (upper_col == lower_col)
    assert (upper_row == lower_row)
    # return tuple of (row, column)
    return int(upper_row), int(upper_col)


def get_seat_id(row: int, col: int) -> int:
    """Converts a tuple of (row, column) into the related seat_id"""
    return 8 * row + col


def part_a():
    """Part A"""
    # current maximum (=0)
    max_seat_id = 0
    # initialize row and column
    row, col = 0, 0
    # loop through all codes given in puzzle input
    for line in lines:
        # convert them to row and column numbers
        row, col = get_seat_pos(line)
        # get the seat_id from that
        seat_id = get_seat_id(row, col)
        # if current seat_id higher than maximum
        if seat_id > max_seat_id:
            # set maximum to current seat_id
            max_seat_id = seat_id
    # return the max seat_id found plus information in which row/column this seat is
    return str(max_seat_id) + 10 * " " + "row:" + str(row) + ",column:" + str(col)


def part_b():
    """Part B"""
    seat_ids = []
    # get every seat_id from puzzle input codes
    for line in lines:
        row, col = get_seat_pos(line)
        seat_ids.append(get_seat_id(row, col))
    # sort it (ascending)
    seat_ids.sort()
    # initialize previous correctly (previous should always be one less than current, first current is seat_ids[0]
    previous = seat_ids[0] - 1
    # loop through all seat_id's
    for seat_id in seat_ids:
        # if current is not one bigger than previous
        if seat_id != previous + 1:
            # my seat is between current and previous
            my_seat_id = seat_id - 1
            # get col and row from my_seat_id
            col = int(my_seat_id % 8)
            row = int((my_seat_id - col) / 8)
            # return my id plus information about the row and column
            return str(my_seat_id) + 10 * " " + "row:" + str(row) + " column:" + str(col)
        # change previous to current, if my seat wasn't found yet
        previous = seat_id


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
