from os.path import dirname, realpath
from pathlib import Path
from opcode_computer import OpcodeComputer
_DAY = "05"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    # there is only one line with comma separated values
    lines = [int(value) for value in f.readlines()[0].split(",")]


####################################################################################################
def part_a():
    oc = OpcodeComputer(lines, [1])
    oc.run()
    return oc.get_outputs()[-1:]


def part_b():
    """Part B"""
    oc = OpcodeComputer(lines, [5])
    oc.run()
    return oc.get_outputs()


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
