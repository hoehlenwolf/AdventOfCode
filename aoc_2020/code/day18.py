from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "18"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []


def load_puzzle():
    global lines
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]


####################################################################################################
def evaluate_exp_without_parenthesis(expression, advanced_mode=False):
    """Evaluates an expression left to right without parentheses if `advanced_mode` is False or not
    specified, otherwise it respects the advanced Math-Mode's precedence (+ before *)"""
    # start at index 0
    index_ = 0
    # loop through whole expression
    while index_ < expression.__len__():
        # if + Operator found
        if expression[index_] == "+":
            # add number before and after the operator together, store it at first number's position
            expression[index_ - 1] = int(expression[index_ - 1]) + int(expression[index_ + 1])
            # delete + Operator and second number from the expression (since the result was evaluated)
            del expression[index_:index_+2]
        # if * Operator found and we're not in advanced Math-Mode
        elif expression[index_] == "*" and not advanced_mode:
            # multiply number before and after the operator together, store it at first number's position
            expression[index_ - 1] = int(expression[index_ - 1]) * int(expression[index_ + 1])
            # delete * Operator and second number from the expression (since the result was evaluated)
            del expression[index_:index_ + 2]
        # if something else found (can only be number, as the expression can now only consist of numbers and operators)
        else:
            # go to the next index
            index_ += 1
    # if we're in 'advanced_mode' we just evaluated all + operations, so now we need to evaluate the left over
    # * operations (just call the same function again *without 'advanced_mode'*)
    if advanced_mode:
        return evaluate_expression(expression, False)
    # if not in 'advanced_mode' return the only (first) number in the expression, as everything has been
    # evaluated and only a single number is left
    return int(expression[0])


def evaluate_expression(expression: list, advanced_mode=False):
    """Evaluates a given expression (possibly with parentheses). Math-Mode can be set to *advanced*"""
    # copy the given expression, as this function will delete it successively while evaluating it
    expression = expression.copy()
    # initialize start value (where outermost opening parenthesis started)
    start = 0
    # count how many opening parenthesis need to be closed
    opening = 0
    # if there's no parenthesis in this expression
    if "(" not in expression and ")" not in expression:
        # evaluate it with respect to given Math-Mode 'advanced_mode'
        return evaluate_exp_without_parenthesis(expression, advanced_mode)
    # start at leftmost position in expression
    i = 0
    # loop through the whole expression (looking for outermost parenthesized block)
    while i < expression.__len__():
        # if opening parenthesis found
        if expression[i] == "(":
            # if it's the first seen (opening an outermost block)
            if opening == 0:
                # remember position where this block started
                start = i
            # increase seen opening parentheses
            opening += 1
        # if closing parenthesis found
        elif expression[i] == ")":
            # reduce seen opening parentheses, because we "consumed" one with this closing one
            opening -= 1
            # if it was the closing one related to the opening one at 'start' position
            if opening == 0:
                # copy that parenthesized block
                old_exp = expression[start+1:i].copy()
                # evaluate that (might still contain lower-level-parentheses)
                # passing th specified math-mode 'advanced_mode'
                expression[start] = evaluate_expression(old_exp, advanced_mode)
                # remove that block from the expression (first element was replaced by it's fully evaluated result)
                del expression[start+1:i+1]
                # modify i to start looking for parenthesis at the beginning of the previously evaluated block
                # could also be one higher, will be increased at the end of the while-loop
                i = start
                # reset 'start' position (because we need to look for new parenthesized blocks)
                start = 0
        # increment current index 'i'
        i += 1
    # now we got rid of all parentheses, thus simply evaluate it with respect to given 'advanced_mode'
    return int(evaluate_exp_without_parenthesis(expression, advanced_mode))


def prepare_line(line: str) -> list:
    """Prepares a line and converts it to an array with each number / operand / parenthesis being one element."""
    # add spaces after opening brackets and before closing ones
    # because puzzle input looks like "(3 + 2)" and we want to split by whitespace, so we need "( 3 + 2 )"
    # then split by whitespace " "
    return line.replace("(", "( ").replace(")", " )").split(" ")


def part_a():
    """Part A"""
    # sum of all evaluated lines
    sum_ = 0
    # loop through all lines
    for line in lines:
        # prepare the line (convert to appropriate array)
        line = prepare_line(line)
        # add the evaluated line's value to the 'sum_'
        sum_ += evaluate_expression(line)
    # return the 'sum_'
    return sum_


def part_b():
    """Part B"""
    # sum of all evaluated lines
    sum_ = 0
    # loop through all lines
    for line in lines:
        # prepare the line (convert to appropriate array)
        line = prepare_line(line)
        # add the evaluated line's value to the 'sum_' with Math-Mode set to advanced (True)
        # This leads to higher precedence of "+" compared to "*"
        sum_ += evaluate_expression(line, True)
    return sum_


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
