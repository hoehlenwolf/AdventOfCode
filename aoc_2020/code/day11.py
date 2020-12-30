from os.path import dirname, realpath
from pathlib import Path
from copy import deepcopy
from time import time_ns

_DAY = "11"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []
seats = []


def load_puzzle():
    global lines, seats
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    row_counter = 0
    for line in lines:
        seats.append([])
        for seat in line:
            seats[row_counter].append(seat)
        row_counter += 1


####################################################################################################
def count_adjacent(seat_config: list, i: int, j: int, seat_state: chr) -> int:
    # offsets
    # 1 2 3
    # 4 X 5
    # 6 7 8
    pos_to_check = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    counter = 0
    for row_off, col_off in pos_to_check:
        row = i + row_off
        col = j + col_off
        if 0 <= row < seat_config.__len__() and 0 <= col < seat_config[row].__len__():
            if seat_config[row][col] == seat_state:
                counter += 1
    return counter


directions_to_check = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_visible_seats(seat_config: list, i: int, j: int, seat_state: chr) -> int:
    # offsets
    # 1 2 3
    # 4 X 5
    # 6 7 8
    counter = 0
    for row_off, col_off in directions_to_check:
        row = i
        col = j
        current = "."
        broken = False
        while current == ".":
            row += row_off
            col += col_off
            if 0 <= row < seat_config.__len__() and 0 <= col < seat_config[row].__len__():
                current = seat_config[row][col]
            else:
                broken = True
                break

        if not broken and seat_config[row][col] == seat_state:
            counter += 1

    return counter


gcounter = 0


def next_step(previous: list, count_adjacent_function, tolerance_occupied_nearby: int) -> (list, int):
    """Return the next step calculated based on the `previous` step provided"""
    global gcounter
    result = deepcopy(previous)
    gcounter += 1
    seats_changed = 0
    for row in range(0, previous.__len__()):
        for col in range(0, previous[row].__len__()):
            current = previous[row][col]
            if current != ".":
                occupied_seats = count_adjacent_function(previous, row, col, "#")
                if current == "L" and occupied_seats == 0:
                    result[row][col] = "#"
                    seats_changed += 1
                elif current == "#" and occupied_seats >= tolerance_occupied_nearby:
                    result[row][col] = "L"
                    seats_changed += 1

    return result, seats_changed


def print_seats(seats_to_print):
    for row in seats_to_print:
        row_str = ""
        for seat in row:
            row_str += seat
        print(row_str)
    print(50 * "-")


def calculate_until_stable(count_adjacent_function, max_nearby_occupied: int) -> int:
    seat_configuration = seats
    seats_changed = 1
    while seats_changed != 0:
        # print_seats(seat_configuration)
        seat_configuration, seats_changed = next_step(seat_configuration, count_adjacent_function, max_nearby_occupied)
    occupied_seats = 0
    for row in seat_configuration:
        for curr_seat in row:
            if curr_seat == "#":
                occupied_seats += 1
    return occupied_seats


def part_a():
    """Part A"""
    return calculate_until_stable(count_adjacent, 4)


def part_b():
    """Part B"""
    return calculate_until_stable(count_visible_seats, 5)


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
