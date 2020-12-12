import time
from os.path import dirname, realpath
from pathlib import Path
from copy import deepcopy

_DAY = "11"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
seats = []
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


def count_visible_seats(seat_config: list, i: int, j: int, seat_state: chr) -> int:
    # offsets
    # 1 2 3
    # 4 X 5
    # 6 7 8
    directions_to_check = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    counter = 0
    for row_off, col_off in directions_to_check:
        current = "."
        row = i
        col = j
        while current == "." and 0 <= row + row_off < seat_config.__len__() and 0 <= col + col_off < seat_config[row].__len__():
            row += row_off
            col += col_off
            current = seat_config[row][col]
        if current == seat_state and 0 <= row < seat_config.__len__() and 0 <= col < seat_config[row].__len__():
            counter += 1
    return counter


def next_step(previous: list, count_adjacent_function, tolerance_occupied_nearby: int) -> (list, int):
    """Return the next step calculated based on the `previous` step provided"""
    result = deepcopy(previous)
    seats_changed = 0
    for row in range(0, previous.__len__()):
        for col in range(0, previous[row].__len__()):
            st = time.time()
            current = previous[row][col]
            if current == "#" and count_adjacent_function(previous, row, col, "#") >= tolerance_occupied_nearby:
                result[row][col] = "L"
                seats_changed += 1
            elif current == "L" and count_adjacent_function(previous, row, col, "#") == 0:
                result[row][col] = "#"
                seats_changed += 1
    return result, seats_changed


def print_seats(seats):
    for row in seats:
        row_str = ""
        for seat in row:
            row_str += seat
        print(row_str)
    print(50 * "-")


def calculate_until_stable(count_adjacent_function, max_nearby_occupied: int) -> int:
    seat_configuration = seats
    seats_changed = 1
    while seats_changed != 0:
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



# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
