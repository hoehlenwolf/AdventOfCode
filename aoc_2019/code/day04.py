from os.path import dirname, realpath
from pathlib import Path

_DAY = "04"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    values = f.readlines()[0].split("-")
# get min and max for range of numbers
min_nr = values[0]
max_nr = values[1]
# global counters for valid numbers in A and B
counter_a = 0
counter_b = 0

####################################################################################################
def check_a(number: int) -> bool:
    """Checks if a number is valid for Part A"""
    number_str = str(number)
    prev = ""
    for digit in number_str:
        # at least 2 adjacent numbers have to be same
        if digit == prev:
            return True
        prev = digit
    return False


def check_b(number: int) -> bool:
    """Checks if a number is valid for Part A"""
    number_arr = [c for c in str(number)]
    # number_arr is already sorted ascending (digits never decrease)
    # add last dummy element in array
    number_arr.append("")
    # how often numbers occur
    counts = []
    # previous digit
    prev = ""
    # counter for occurrences of digits
    counter = 1
    # loop through all digits
    for digit in number_arr:
        # if same as previous
        if digit == prev:
            # increment counter
            counter += 1
        else:
            # otherwise reset counter and append the value of it to counts
            counts.append(counter)
            counter = 1
        # adjust previous digit `prev`
        prev = digit
    # some digit has to occur *exactly* 2 times
    if 2 in counts:
        return True
    else:
        return False


def calculate():
    """Calculates results for A and B combined (better performance because the numbers are the same,
    only the condition in check_a and check_b varies"""
    # write results in global variable `counter_a` and `counter_b`
    global counter_a, counter_b
    # loop through every number in the given range (puzzle input)
    for number in range(int(min_nr), int(max_nr) + 1):
        number_str = str(number)
        # number is valid
        valid = True
        # loop through index position in the number (-string)
        for i in range(0, number_str.__len__() - 1):
            # if digits decrease from left to right
            if int(number_str[i]) > int(number_str[i + 1]):
                # number is invalid
                valid = False
                # break out of the loop checking for decreasing digits
                break
        # if valid and satisfies B's condition
        if valid and check_b(number):
            counter_b += 1
        # if valid and satisfies A's condition
        if valid and check_a(number):
            counter_a += 1


# calculate results for A and B simultaneously
calculate()
# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(counter_a))
print("Part B: " + str(counter_b))
print(28 * "-")
