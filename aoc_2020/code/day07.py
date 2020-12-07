from os.path import dirname, realpath
from pathlib import Path
import re

_DAY = "07"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace(".\n", "") for line in f.readlines()]
# pre-process input to make dict {outer_bag:[(inner_bag, number),...]}
bag_combs = dict()


def preprocess():
    global bag_combs
    for line in lines:
        inner_bags = []
        outer_colour = line.split(" bags")[0]
        inner_bags_enum = line.split("contain ")[1]
        if inner_bags_enum != "no other bags":
            for inner_bag in inner_bags_enum.split(", "):
                num = inner_bag.split(" ")[0]
                # cut away number plus whitespace in front
                inner_colour = inner_bag[num.__len__() + 1:]
                # cut away " bag" / " bags" / " bag." / " bags." at the end
                inner_color = re.sub(" bag[s.]{0,2}", "", inner_colour)
                # append (inner_color, num) to inner_bags
                inner_bags.append((inner_color, int(num)))
        bag_combs[outer_colour] = inner_bags


####################################################################################################
def can_contain(outer_colour: str, inner_colour: str) -> int:
    for possible_bag, number in bag_combs[outer_colour]:
        # if outer bag can contain the inner_colour directly
        if possible_bag == inner_colour:
            return True
    # if code reaches here, the inner_color can't be contained in the outer_color *directly*
    # loop through all possible inner colours of outer_colour and check if they can contain inner_colour recursively
    can_cont_rec = False
    for possible_bag, number in bag_combs[outer_colour]:
        can_cont_rec = can_cont_rec or can_contain(possible_bag, inner_colour)
    return can_cont_rec


def get_bags_inside(outer_colour: str) -> int:
    contains = 0
    for bag, number in bag_combs[outer_colour]:
        bags_inside = get_bags_inside(bag)
        # *one* given bag contains bags_inside bags of bags inside it
        # increment by 1 because the one bag technically "contains itself"
        # multiply by number, because outer_colour can hold `number`-many bags of type `bag` inside it
        # and add it to contains because outer_colour might contain multiple different bag types
        contains += ((bags_inside+1) * number)
    return contains


def part_a():
    """Part A"""
    # list of possible outermost colours
    possible_outermost_colours = []
    # loop through all existing colours
    for colour in bag_combs:
        # if the colour can eventually contain "shiny gold" add the colour to the possible_outermost_colours
        if can_contain(colour, "shiny gold"):
            possible_outermost_colours.append(colour)
    # return possibilities for outermost bag-colour to eventually contain "shiny gold"
    return possible_outermost_colours.__len__()


def part_b():
    """Part B"""
    return get_bags_inside("shiny gold")


preprocess()
# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
