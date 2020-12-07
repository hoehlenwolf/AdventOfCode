from os.path import dirname, realpath
from pathlib import Path
_DAY = "04"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    values = f.readlines()[0].split("-")
# get min and max for range of numbers
min_nr = int(values[0])
max_nr = int(values[1])

####################################################################################################
def part_a():
    """Part A"""
    counter = 0
    for number in range(min_nr, max_nr + 1):
        number_str = str(number)
        # if 2 adjacent digits are the same
        adjacent_same = False
        # check if six digit number (should always be the case because of puzzle input range...)
        if number_str.__len__() == 6:
            # loop through each index position
            for i in range(0, number_str.__len__() - 1):
                # digits never decrease
                if int(number_str[i]) == int(number_str[i+1]):
                    adjacent_same = True
                elif int(number_str[i]) > int(number_str[i+1]):
                    # go to next number and set adjacent_same to False so that current number is counted as invalid
                    # 121999
                    if i < number_str.__len__() - 2:
                        number += 10**(i+1) - int(number_str[i+2:])
                    adjacent_same = False
                    break
        if adjacent_same:
            counter += 1
    return counter







    return None


def part_b():
    """Part B"""
    return None


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
