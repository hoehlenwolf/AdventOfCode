from os.path import dirname, realpath
from pathlib import Path
from opcode_computer import OpcodeComputer

_DAY = "02"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    # there is only one line with comma separated values
    lines = [int(value) for value in f.readlines()[0].split(",")]


####################################################################################################
def part_a():
    """Part A"""
    oc = OpcodeComputer(lines)
    # set value at *Position* to `value` with mode being 1 because argument 1 is an address that needs to be
    # written to in immediate mode
    oc.set_value(1, 12,1)
    oc.set_value(2, 2,1)
    oc.run()
    return oc.get_memory()[0]


def part_b():
    """Part B"""
    target = 19690720
    oc = OpcodeComputer(lines)
    for noun in range(0, 100):
        for verb in range(0, 100):
            # set value at *Position* to `value` with mode being 1 because argument 1 is an address that needs to be
            # written to in immediate mode
            oc.set_value(1, noun, 1)
            oc.set_value(2, verb, 1)
            oc.run()
            # if target reached
            if target == oc.get_memory()[0]:
                # return noun and verb (NNVV)
                return 100 * noun + verb
            # reset memory for another run
            oc.reset()


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
