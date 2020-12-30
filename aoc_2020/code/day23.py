from os.path import dirname, realpath
from pathlib import Path
_DAY = "23"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
nums = [int(cup)-1 for cup in lines[0]]    # down shift of cup numbers 1->0
cups_arr = nums.copy()
for i in range(0, nums.__len__()):
    index_ = nums.index(i)
    next_cup_index = (index_+1) % nums.__len__()
    next_cup = nums[next_cup_index]
    cups_arr[i] = next_cup


####################################################################################################
def get_cup_config(cups: list):
    cup_config = []
    current = 0
    while (current+1) not in cup_config:
        cup_config.append(current+1)
        current = cups[current]
    config = ""
    for cup in cup_config[1:]:
        config += str(cup)
    return config


def cups(cups_circle: list, start_cup: int, steps: int) -> str:
    current = start_cup
    for step in range (0, steps):
        cups_taken_beginning = cups_circle[current]
        cups_taken_middle = cups_circle[cups_taken_beginning]
        cups_taken_end = cups_circle[cups_taken_middle]
        cup_3_after = cups_circle[cups_taken_end]
        found = False
        destination = (current-1) % cups_circle.__len__()
        while not found:
            if not (destination == cups_taken_beginning or destination == cups_taken_middle or destination == cups_taken_end):
                found = True
            else:
                destination = (destination - 1) % cups_circle.__len__()

        cups_circle[cups_taken_end] = cups_circle[destination]
        cups_circle[current] = cup_3_after
        cups_circle[destination] = cups_taken_beginning
        current = cup_3_after
    return cups_circle



def part_a():
    """Part A"""
    result = cups(cups_arr.copy(),nums[0], 100)
    return get_cup_config(result)


def part_b():
    """Part B"""
    million_cups_arr = cups_arr.copy()
    old_last_cup = million_cups_arr.index(nums[0])
    million_cups_arr[old_last_cup] = million_cups_arr.__len__()
    million_cups_arr += range(10, 1000001)
    million_cups_arr[million_cups_arr.__len__()-1] = nums[0]
    result = cups(million_cups_arr, nums[0], 10000000)
    star_1, star_2 = result[0], result[result[0]]
    star_1 += 1
    star_2 += 1
    return str(star_1 * star_2) + 10*" " + "(" + str(star_1) + " and " + str(star_2) + ")"


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
