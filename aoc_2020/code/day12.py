from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "12"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def rotate(previous_direction: (int, int), rotate_direction: chr, deg: int) -> (int, int):
    """Rotates given input vector `previous_direction` by `deg`-many degrees either right ('R') or left ('L')
    given by `rotate_direction`
    `steps` have to be multiples of 90 degrees"""
    # Directions for N E S W
    # directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    # number of 90 degree turns
    turns_90_deg = int(deg / 90)
    # previous direction / vector
    x, y = previous_direction
    # if rotation should be counter-clockwise
    if rotate_direction == "L":
        # swap x and y values as many times as it needs 90-degrees turns to reach desired `deg`
        for i in range(turns_90_deg):
            # remember old x value
            x_help = x
            # new x is old y
            x = y
            # new y is negative old x
            y = -x_help
    # if rotation should be counter-clockwise
    elif rotate_direction == "R":
        # swap x and y values as many times as it needs 90-degrees turns to reach desired `deg`
        for i in range(turns_90_deg):
            # remember old x value
            x_help = x
            # new x is negative old y
            x = -y
            # new y is old x
            y = x_help
    # return the rotated vector
    return x, y


def part_a():
    """Part A"""
    # ship starts facing east (in positive x direction)
    curr_facing = (1, 0)
    # starting position of ship is (0,0)
    curr_x = 0
    curr_y = 0
    # work through all instructions / lines
    for instr in lines:
        # extract the direction ('F','N','E','S','W','R','L') from instruction
        direction = instr[0:1]
        # extract number of steps from instruction
        steps = int(instr[1:])
        # if instruction is to move forward
        if direction == "F":
            # move 'steps' into the current facing direction
            curr_x += steps * curr_facing[0]
            curr_y += steps * curr_facing[1]
        # if instruction is to move north
        elif direction == "N":
            # decrease current y position by 'steps'
            curr_y -= steps
        # if instruction is to move east
        elif direction == "E":
            # increase current x position by 'steps'
            curr_x += steps
        # if instruction is to move south
        elif direction == "S":
            # increase current y position by 'steps'
            curr_y += steps
        # if instruction is to move west
        elif direction == "W":
            # decrease current x position by 'steps'
            curr_x -= steps
        # if instruction is to rotate
        elif direction == "L" or direction == "R":
            # rotate current facing direction (vector) by 'steps'-many degrees into the given 'direction'
            curr_facing = rotate(curr_facing, direction, steps)
    # return Manhattan-distance between ship's final position and starting point (0,0)
    return abs(curr_x) + abs(curr_y)


def part_b():
    """Part B"""
    # set waypoint's initial position
    way_x, way_y = (10, -1)
    # set ship's initial position
    ship_x, ship_y = (0, 0)
    # loop through all instructions given (puzzle-input)
    for instr in lines:
        # extract direction and steps from the instruction
        direction = instr[0:1]
        steps = int(instr[1:])
        # move forward towards the waypoint 'steps' times
        if direction == "F":
            ship_x += steps * way_x
            ship_y += steps * way_y
        # move north
        elif direction == "N":
            way_y -= steps
        # move east
        elif direction == "E":
            way_x += steps
        # move south
        elif direction == "S":
            way_y += steps
        # move west
        elif direction == "W":
            way_x -= steps
        # rotate waypoint around the ship (works the same as in Part A)
        elif direction == "L" or direction == "R":
            way_x, way_y = rotate((way_x, way_y), direction, steps)
    # return the Manhattan-distance between starting position (0,0) and ship's final position
    return abs(ship_x) + abs(ship_y)


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
