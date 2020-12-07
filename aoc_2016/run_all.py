import subprocess
from os.path import isfile, dirname, realpath
from os import remove
from sys import platform
import time
from pathlib import Path

# if on windows
if platform == "win32":
    _PYTHON = "python"
else:  # otherwise
    _PYTHON = "python3"
# file where combined outputs of all days will be written
_OUTPUTS = Path("Outputs.txt")
# Variables for printout and logging
per_day_output = True  # if for each day there should be a dayXX_output.txt
printout = True  # if printout in console is wanted
summarized_output = True  # if there should be Outputs.txt for combined Output of all days
# Number of iterations for constructing average runtime
ITERATIONS = 10
# Folder in which the output should be stored into
_OUTPUT_FOLDER = Path(dirname(realpath(__file__))) / Path("outputs")
# create if doesn't exist yet
Path(_OUTPUT_FOLDER).mkdir(exist_ok=True)
# folder in which code files for each day are stored
_CODE_FOLDER = Path(dirname(realpath(__file__))) / Path("code")
# create that code folder if doesn't exist yet
Path(_CODE_FOLDER).mkdir(exist_ok=True)


def run_all():
    """Runs all existing dayXX.py in current directory"""
    # Clear existing _OUTPUTS.txt for writing in append-mode
    if isfile(_OUTPUTS):
        remove(_OUTPUTS)
    # 2-d array to store time values in (-> iterations; v days)
    time_values = [[]]
    for i in range(0, ITERATIONS):
        # log only on first iteration (save outputs of days)
        logging = (i == 0)
        # create names day01 .. day25
        for x in range(1, 25):
            x_str = str(x)
            if x < 10:
                x_str = "0" + x_str
            name = "day" + x_str
            # if dayXX exists
            if isfile(_CODE_FOLDER / Path(name + ".py")):
                # Start a timer
                time_start = time.time()
                # run the file
                run(name, logging)
                time_end = time.time()
                time_diff = time_end - time_start
                # enlarge time_values array if new day reached for the first time
                if x - 1 == time_values.__len__():
                    time_values.append([])
                # append time_diff to x-th row of 2-d array time_values
                time_values[x - 1].append(time_diff)
    if time_values.__len__() != 0 and time_values[0].__len__() != 0:
        averaged_time_values = [sum(tv) / len(tv) for tv in time_values]
        log(17 * "-" + "runtime duration" + 17 * "-")
        for i in range(0, averaged_time_values.__len__()):
            # Shift i one up because day 0 doesn't exist
            str_i = str(i + 1)
            # if str_i < "10"
            if i < 9:
                # add leading 0
                str_i = "0" + str_i
            # log average of the day (3 decimal places)
            log("Day " + str_i + ": " + str(format(averaged_time_values[i], ".3f")) + " seconds")
        log(50 * "-")
        # log total execution time (3 decimal places)
        log("Total execution time: " + str(format(sum(averaged_time_values), ".3f")) + " seconds on average")
    else:
        log("There are no files in " + str(_CODE_FOLDER) + " to be run! :(")


def log(text: str, name: str = None):
    file_log_text = text
    if not file_log_text.endswith("\n"):
        file_log_text += "\n"
    if printout:
        print(text)

    if per_day_output and name is not None:
        with open(_OUTPUT_FOLDER / Path(name + "_output.txt"), 'w+') as f:
            f.write(file_log_text)

    if summarized_output:
        with open(_OUTPUTS, "a+") as f:
            f.write(file_log_text)


def run(name: str, logging: bool):
    # get output from calling given python-script
    path = str(_CODE_FOLDER / Path(name + ".py"))
    out = str(subprocess.check_output([_PYTHON, path]), "UTF-8")
    # replace double linebreaks (windows)
    out = out.replace("\r\n", "\n")
    if logging:
        log(out, name)


# Run all existing days
run_all()
