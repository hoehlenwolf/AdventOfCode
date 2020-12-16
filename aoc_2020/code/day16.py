import itertools
from os.path import dirname, realpath
from pathlib import Path

_DAY = "16"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################


def get_ranges(line: str) -> list:
    """Extracts the ranges specified by a string 'a-b or c-d or e-f' and returns the corresponding
    array [(a,b),(c,d),(e,f)]"""
    ranges = []
    # loop through all specified ranges (split by OR): (a-b) OR (c-d) ...
    for range_ in line.split(" or "):
        # extract lower and upper limit
        lower = int(range_.split("-")[0])
        upper = int(range_.split("-")[1])
        # append lower and upper as a tuple to the list of ranges
        ranges.append((lower, upper))
    # return the list of range-tuples (lower,upper)
    return ranges


# split input into valid field ranges, my ticket and array of other tickets
# preprocessing and parsing the puzzle input
section = 0  # current section (0: ranges per field name, 1: my ticket, 2: nearby tickets)
fields = dict()  # dict to store key-value pairs {field_name:allowed_ranges_list}
tickets = []  # array of tickets, with each ticket being an array with the values of the fields in the same order
# Filled py part A
valid_tickets = []
# loop through all lines
for line in lines:
    if line == "":  # empty line, increase section
        section += 1
        continue  # skip to next line
    if section == 0:  # if we are defining fields and their ranges (section 0)
        field = line.split(":")[0]  # get field name
        # add that field name to the dict with it's name as key and it's corresponding allowed ranges as value
        fields[field] = get_ranges(line.split(": ")[1])
    elif section == 1:  # if we are extracting my ticket (section 1)
        if line == "your ticket:":  # skip line "your ticket:"
            continue
        else:  # extract the values (split by comma) and build array from them
            my_ticket = [int(val) for val in line.split(",")]
    elif section == 2:  # if we reached the nearby tickets (section 2)
        if line == "nearby tickets:":  # skip line "nearby tickets:"
            continue
        else:  # append an array of values (current ticket) to the list of tickets
            tickets.append([int(val) for val in line.split(",")])


####################################################################################################
def check_valid_number(number: int, field_name: str = None) -> bool:
    """Checks if a given `number` is valid for given `field_name`. Checks if value is valid for *any* field
    if `field_name` not specified"""
    # check if number valid for any field if 'field_name' not specified
    if field_name is None:
        # loop through all field_ranges (is an array of allowed ranges per field name)
        for field_ranges in fields.values():
            # loop through every range in the allowed ranges per field
            for lower, upper in field_ranges:
                # if number is within boundaries
                if lower <= number <= upper:
                    # number is valid
                    return True
        # this return statement is only reached if the number is not valid for any field. Thus return False
        return False
    # check if number valid for given 'field_name' ('field_name' is specified)
    else:
        # loop through all allowed ranges for that given 'field_name'
        for lower, upper in fields[field_name]:
            # if number is within boundaries
            if lower <= number <= upper:
                # number is valid
                return True
        # this return statement is only reached if the number is not valid for the given 'field_name'. Thus return False
        return False


def part_a():
    """Part A"""
    # Sum of invalid values (multiple per ticket allowed)
    invalid_sums = 0
    # loop through all tickets
    for ticket in tickets:
        # ticket is valid (initially)
        ticket_valid = True
        # check every value in the ticket
        for value in ticket:
            # if the value is not valid for *any* field
            if not check_valid_number(value):
                # ticket is invalid
                ticket_valid = False
                # add the value to the sum of invalid values
                invalid_sums += value
        # if ticket is valid
        if ticket_valid:
            # append it to the 'valid_tickets' list (from global scope)
            valid_tickets.append(ticket)
    # return the sum of all invalid numbers
    return invalid_sums


def part_b():
    """Part B"""
    # create 2-D array where the array at index i contains all possible 'field_names' for the i-th value in a ticket
    # at the beginning everything is possible for every field-index
    possible_fields = []
    # fill all sub-array (as many as there are fields) with all field_names
    for i in range(0, fields.__len__()):
        # add new sub-array
        possible_fields.append([])
        # append all field names that exist to that sub-array
        for field_name in fields:
            possible_fields[i].append(field_name)
    # loop over every array in possible_fields
    for i in range(0, fields.__len__()):
        # loop through all field names that exist
        for field_name in fields:
            # check every ticket, if the value at index i is valid for field_name
            for ticket in valid_tickets:
                # if it's not valid
                if not check_valid_number(ticket[i], field_name):
                    # this field_name is not possible for i-th index, thus remove it from sub-array (i-th index)
                    possible_fields[i].remove(field_name)
    # now we can end up with 'possible_fields' = [['row'], ['class', 'row'], ['class', 'row', 'seat']]
    # therefore we must look at the sub-array i with lowest length l, remove it's contents from every other array
    # and move on to find the next lowest length sub-array
    # This array does *not* have to be in order
    # so we create an array of tuples (index, number of possible fields for index)
    lengths = []
    for i in range(0, possible_fields.__len__()):
        lengths.append((i, possible_fields[i].__len__()))
    # no we have an array 'lengths': [(0,1),(1,2),(3,4)]
    # we sort that ascending by second value in the tuple
    lengths.sort(key=lambda tup: tup[1])
    # now we have an ascending list of the respective indices for possible_fields (sorted by their length)
    # loop over them all (in order 1,2,3...)
    for at_index, length in lengths:
        # for every other field
        for i in range(0, fields.__len__()):
            # that is not the current one
            if i != at_index:
                # remove possible field names of current index 'at_index' from the field (!= current on)
                for to_remove in possible_fields[at_index]:
                    if to_remove in possible_fields[i]:  # if exists, remove it
                        possible_fields[i].remove(to_remove)
    # now 'possible_fields' is an array containing sub-arrays where sub-array at index i has the *only* valid field_name
    # for i-th value in tickets
    # flatten 2D array into 1D array since every sub-array now contains only 1 element
    field_names = list(itertools.chain.from_iterable(possible_fields))
    # multiply all values of my own ticket whose field names start with "departure" together
    result = 1  # initialized as 1, because of *= later on
    # loop through all field names ('field_names' is sorted so that index i specifies name of i-th value in any ticket)
    for field_name in field_names:
        # if field name starts with "departure"
        if str(field_name).startswith("departure"):
            # multiply my ticket's value at the right index (of field_name in field_names) with 'result'
            result *= my_ticket[field_names.index(field_name)]
    return result


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
