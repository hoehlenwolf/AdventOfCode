from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "25"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
pub_key_1 = -1
pub_key_2 = -1


def load_puzzle():
    global pub_key_1, pub_key_2
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    pub_key_1 = int(lines[0])
    pub_key_2 = int(lines[1])


####################################################################################################
def find_loopsize(subject_number, target):
    val = 1
    loop_size = 0
    while True:
        val *= subject_number
        val = val % 20201227
        loop_size += 1
        if val == target:
            return loop_size


def transform_subject(subject_number, loop_size):
    val = 1
    for i in range(loop_size):
        val *= subject_number
        val = val % 20201227
    return val


def part_a():
    """Part A"""
    loop_size = find_loopsize(7, pub_key_1)
    encryption_key = transform_subject(pub_key_2, loop_size)
    return encryption_key


def part_b():
    """Part B"""
    return None


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
