from os.path import dirname, realpath
from pathlib import Path
_DAY = "25"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
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
    val=1
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


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
