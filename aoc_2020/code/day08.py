from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "08"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def parse_line(line: str) -> (str, int):
    """Converts a line of code into the corresponding Operation `op` and the value behind it `number`"""
    # first part before the single whitespace
    op = line.split(" ")[0]
    # second part after the single whitespace
    number = int(line.split(" ")[1])
    return op, number


def execute_program(program: list) -> (int, bool):
    """Executes a given `program` (array of lines of code) and returns the accumulator value as well as a boolean to
    flag successful termination"""
    # indices (line numbers) that have been executed so far
    executed_commands = []
    # accumulator value
    acc = 0
    # current command (line number)
    current_command = 0
    # as long as program hasn't reached end of file and line to execute wasn't executed before
    while current_command < program.__len__() and current_command not in executed_commands:
        # remember current line as already executed
        executed_commands.append(current_command)
        # get op and number from the instruction
        op, number = parse_line(program[current_command])
        # if NOP
        if op == "nop":
            # go to next line
            current_command += 1
        # if ACC
        elif op == "acc":
            # increase acc value by number
            acc += number
            # go to next line
            current_command += 1
        # if JMP
        elif op == "jmp":
            # go number-many lines further from current line (backwards also allowed)
            current_command += number
    # if program reached end of file, it has terminated successfully
    if current_command >= lines.__len__():
        return acc, True
    # otherwise a loop was encountered
    else:
        return acc, False


def part_a():
    """Part A"""
    # run given program, return acc value when program starts looping
    acc, terminated = execute_program(lines)
    return acc


def part_b():
    """Part B"""
    # loop through all lines
    for i in range(0, lines.__len__()):
        # get op and number per line
        op, number = parse_line(lines[i])
        # make a copy of puzzle-input program
        modified_program = lines.copy()
        # if op is "JMP"
        if op == "jmp":
            # replace it with "NOP"
            modified_program[i] = modified_program[i].replace("jmp", "nop")
        # if op is "NOP"
        elif op == "nop":
            # replace it with "JMP"
            modified_program[i] = modified_program[i].replace("nop", "jmp")
        # run the modified program (1 line changed compared to original program)
        acc, success = execute_program(modified_program)
        # if modified program terminates successfully
        if success:
            # return the accumulator value the program produced
            return acc


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
