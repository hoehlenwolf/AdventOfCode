from os.path import dirname, realpath
from pathlib import Path
from time import time_ns

_DAY = "06"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []
groups = [[]]


def load_puzzle():
    global lines, groups
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    # convert read lines into 2-d-array of groups with each group being an array of answers
    group_counter = 0
    for line in lines:
        # if new group
        if line == "":
            # add another group
            groups.append([])
            # increment group counter
            group_counter += 1
        else:
            # otherwise append answer to current group
            groups[group_counter].append(line)


####################################################################################################
def check_question_in_all_answers(question: chr, group: list) -> bool:
    """Checks if *everyone* in the group answered "yes" to given question"""
    # loop through all answers in the given group
    for answer in group:
        # if at lest one person didn't answer "yes" to that question
        if question not in answer:
            return False
    # if this statement is reached, everyone in the group answered "yes"es to the given question
    return True


def part_a():
    """Part A"""
    # sum of question that were answered "yes" by *anyone*
    sum_yes = 0
    # loop through all groups
    for group in groups:
        # construct a unique set of all questions answered yes within that group
        answers = set()
        for person in group:
            for answer in person:
                answers.add(answer)
        # add the size of that set (=# questions anyone answered "yes" to within current group" to the sum_yes
        sum_yes += answers.__len__()
    return sum_yes


def part_b():
    """Part B"""
    # sum of questions, that *everyone* answered "yes" to per group
    sum_yes = 0
    # loop through all groups
    for group in groups:
        # remember which questions have already been counted
        seen_questions = set()
        # loop through all persons
        for person in group:
            # loop through all answers per person
            for answer in person:
                # if answer (letter) hasn't been counted yet and *everyone* in the group answered "yes" to that question
                if answer not in seen_questions and check_question_in_all_answers(answer, group):
                    # add processed answer to seen_questions
                    seen_questions.add(answer)
                    # increment sum_yes by 1
                    sum_yes += 1
    return sum_yes


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
