from os.path import dirname, realpath
from pathlib import Path

_DAY = "03"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    wires = [line.replace("\n", "").split(",") for line in f.readlines()]
points_a = []
points_b = []


####################################################################################################
def part_a():
    """Part A"""
    # sort intersections ascending by the Manhattan-distance
    intersections.sort(key=lambda intersection: intersection[0])
    # return information about distance and position
    return str(intersections[0][0]) + 10 * " " + "at " + str(intersections[0][2])


def part_b():
    """Part B"""
    # sort intersections ascending by the combined steps needed to reach it
    intersections.sort(key=lambda intersection: intersection[1])
    return str(intersections[0][1]) + 8 * " " + "at " + str(intersections[0][2])


def get_points(wire: list) -> list:
    # list of points reached by wire
    points = []
    # current x and y
    x = 0
    y = 0
    # loop through all instructions for wire
    for instr in wire:
        # go right
        if instr[0] == "R":
            # for specified number of steps
            for val in range(int(instr[1:])):
                x += 1
                points.append((x, y))
        # go left
        if instr[0] == "L":
            # for specified number of steps
            for val in range(int(instr[1:])):
                x -= 1
                points.append((x, y))
        # go up
        if instr[0] == "U":
            # for specified number of steps
            for val in range(int(instr[1:])):
                y += 1
                points.append((x, y))
        # go down
        if instr[0] == "D":
            # for specified number of steps
            for val in range(int(instr[1:])):
                y -= 1
                points.append((x, y))
    return points


# Get Points per wire for part A and B
points_a = get_points(wires[0])
points_b = get_points(wires[1])
# create list consisting of all intersections: (distance to origin, combined steps, (x,y))
intersections = [(abs(point[0]) + abs(point[1]), points_a.index(point) + points_b.index(point) + 2, point) for point in
                 (set(points_a) & set(points_b))]
# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
