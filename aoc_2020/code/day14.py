from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "14"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def apply_mask_a(mask: str, number: int) -> int:
    result = ""
    number_bin = "{0:b}".format(number)
    number_bin = (mask.__len__() - number_bin.__len__()) * "0" + number_bin
    for i in range(0, mask.__len__()):
        bit = mask[i]
        if bit == "X":
            result += number_bin[i]
        else:
            result += bit
    return int(result, 2)


def part_a():
    """Part A"""
    mask = ""
    memory = dict()
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" ")[2]
        elif line.startswith("mem"):
            address = int(line[4:].split("]")[0])
            value = int(line.split(" ")[2])
            memory[address] = apply_mask_a(mask, value)
    mem_sum = 0
    for address in memory:
        mem_sum += memory[address]
    return mem_sum


def floating_possibilities(floating: str, start_index=0, current_solution="", results=None):
    if results is None:
        results = []
    for i in range(start_index, floating.__len__()):
        if floating[i] == "X":
            floating_possibilities(floating, i + 1, current_solution + "0", results)
            floating_possibilities(floating, i + 1, current_solution + "1", results)
            break
        else:
            current_solution += floating[i]
    if current_solution.__len__() >= floating.__len__():
        results.append(current_solution)
    return results


def apply_mask_b(mask, binary):
    res = ""
    for i in range(0, mask.__len__()):
        if mask[i] == "X" or mask[i] == "1":
            res += mask[i]
        else:
            res += binary[i]
    return res


def part_b():
    """Part B"""
    mask = ""
    memory = dict()
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" ")[2]
        elif line.startswith("mem"):
            address = int(line[4:].split("]")[0])
            value = int(line.split(" ")[2])
            address_bin = "{0:b}".format(address)
            address_bin = (mask.__len__() - address_bin.__len__()) * "0" + address_bin
            address_masked = apply_mask_b(mask, address_bin)
            for address_poss in floating_possibilities(address_masked):
                memory[int(address_poss, 2)] = value
    mem_sum = 0
    for address in memory:
        mem_sum += memory[address]
    return mem_sum


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
