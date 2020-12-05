import re
from pathlib import Path
from os.path import dirname, realpath
_DAY = "04"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
    passports = []
    pass_counter = 0
    for i in range(0, lines.__len__()):
        if lines[i] == "":  # if blank line
            pass_counter += 1  # "add" new passport

        else:
            if passports.__len__() <= pass_counter:  # make sure dict passports[pass_counter] exists
                passports.append({})
            for key_value in lines[i].split(" "):  # split into key:value pairs and split them into key and value
                key = key_value.split(":")[0]
                value = key_value.split(":")[1]
                passports[pass_counter][key] = value  # add them to the dict


####################################################################################################
def is_valid_a(passport: dict) -> bool:
    """Checks if a passport is valid by Part A's requirements"""
    # Check if every field is present
    for field in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:  # cid optional
        if field not in passport:
            return False
    return True


def is_valid_b(passport: dict) -> bool:
    """Checks if a passport is valid by Part B's requirements"""
    # birth year constraint
    if not 1920 <= int(passport["byr"]) <= 2002:
        return False
    # issue year constraint
    if not 2010 <= int(passport["iyr"]) <= 2020:
        return False
    # expiration year constraint
    if not 2020 <= int(passport["eyr"]) <= 2030:
        return False
    # height constraint
    if passport["hgt"].endswith("cm"):
        # if unit is "cm"
        if not 150 <= int(passport["hgt"][:-2]) <= 193:
            return False
    elif passport["hgt"].endswith("in"):
        # if unit is "in"
        if not 59 <= int(passport["hgt"][:-2]) <= 76:
            return False
    else:  # if unit is other than "cm" or "in"
        return False
    # hair color constraint: 7 characters (# + 6 *hexadecimal* characters)
    if passport["hcl"].__len__() != 7 or re.match("#[0-9a-f]{6}", passport["hcl"]) is None:
        return False
    # eye-color constraint: must be one of these
    if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    # passport id constraint (9 digits incl. leading 0's)
    # check length extra because re.match would be != None if 10 digits present
    if passport["pid"].__len__() != 9 or re.match("[0-9]{9}", passport["pid"]) is None:
        return False
    return True


def part_a():
    """Part A"""
    # valid passport counter
    counter = 0
    # loop through all passports
    for passport in passports:
        # if valid by Part A's definition
        if is_valid_a(passport):
            # increment valid passport counter
            counter += 1
    return counter


def part_b():
    """Part B"""
    # valid passport counter
    counter = 0
    # loop through all passports
    for passport in passports:
        # if valid by Part A's *AND* Part B's definition
        if is_valid_a(passport) and is_valid_b(passport):
            # increment valid passport counter
            counter += 1
    return counter


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
