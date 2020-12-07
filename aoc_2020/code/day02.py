from pathlib import Path
from os.path import dirname, realpath
_DAY = "02"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    # convert each line into array with 2 elements (split by ":") and produce 2-d array by doing that for each line
    # so lines[0] has [policy_0, passw_0] ...
    lines = [line.replace("\n", "").split(": ") for line in f.readlines()]


####################################################################################################
def part_a():
    """Part A"""
    # count valid passwords using A's interpretation of the policy
    valids = 0
    for el in lines:
        if is_valid_a(el[0], el[1]):
            valids += 1
    return valids


def part_b():
    """Part B"""
    # count valid passwords using B's interpretation of the policy
    valids = 0
    for el in lines:
        if is_valid_b(el[0], el[1]):
            valids += 1
    return valids


def is_valid_a(policy: str, passw: str):
    # get min_max string (e.g. "1-3")
    min_max = policy.split(" ")[0]
    # split min_max into p_min and p_max
    p_min = int(min_max.split("-")[0])
    p_max = int(min_max.split("-")[1])
    # get the letter the policy is for
    letter = policy.split(" ")[1]
    # count occurrences of that character in the password
    actual = 0
    for ch in passw:
        if ch == letter:
            actual += 1
    # check if policy is fulfilled
    if p_max >= actual >= p_min:
        return True
    else:
        return False


def is_valid_b(policy, passw: str):
    # get start_end string (e.g. "1-3")
    start_end = policy.split(" ")[0]
    # split start_end into start and end (offset them by -1 cause of index shift)
    start = int(start_end.split("-")[0]) - 1
    end = int(start_end.split("-")[1]) - 1
    # get letter the policy is for
    letter = policy.split(" ")[1]
    # check if we're still within the index range and
    # return True if position 'start' in passw has the character XOR position 'end'
    if (0 <= start < passw.__len__() and passw[start] == letter) != (
            0 <= end < passw.__len__() and passw[end] == letter):
        return True
    else:
        return False


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
