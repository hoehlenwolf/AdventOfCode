from os.path import dirname, realpath
from pathlib import Path
_DAY = "06"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
# convert read lines into 2-d-array of groups with each group being an array of answers
groups = [[]]
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
def check_question_in_all_answers(question : chr, group : list) -> bool:
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


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
