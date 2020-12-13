import subprocess
from os.path import isfile, dirname, realpath
from os import remove
from sys import platform, argv
import time
from pathlib import Path
from math import floor

# if on windows
if platform == "win32":
    _PYTHON = "python"
else:  # otherwise
    _PYTHON = "python3"
# Variables for printout and logging
per_day_output = True  # if for each day there should be a dayXX_output.txt
printout = True  # if printout in console is wanted
summarized_output = True  # if there should be Outputs.txt for combined Output of all days
# Number of iterations for constructing average runtime
ITERATIONS = 10
# Number of max Hashtags per day for visualization of runtime durations
_MAX_NUM_HASHTAGS_PER_DAY = 40
# Years that can be run
_MIN_YEAR = 2015
_MAX_YEAR = 2020
# global variables for folder structure, set in run_all
_YEAR_FOLDER = Path("")
_OUTPUTS = Path("")
_OUTPUT_FOLDER = Path("")
_CODE_FOLDER = Path("")


def run_all(year_to_run: int):
    global _YEAR_FOLDER, _OUTPUTS, _OUTPUT_FOLDER, _CODE_FOLDER
    """Runs all existing dayXX_template.py for specified year"""
    # Folder that contains all the years
    _YEAR_FOLDER = Path(dirname(realpath(__file__))) / Path("aoc_" + str(year_to_run))
    # file where combined outputs of all days will be written
    _OUTPUTS = _YEAR_FOLDER / Path("Outputs.txt")
    # Folder in which the output should be stored into
    _OUTPUT_FOLDER = _YEAR_FOLDER / Path("outputs")
    # create if doesn't exist yet
    Path(_OUTPUT_FOLDER).mkdir(exist_ok=True)
    # folder in which code files for each day are stored
    _CODE_FOLDER = _YEAR_FOLDER / Path("code")
    # create that code folder if doesn't exist yet
    Path(_CODE_FOLDER).mkdir(exist_ok=True)
    ##############################################################
    # Clear existing _OUTPUTS.txt for writing in append-mode
    if isfile(_OUTPUTS):
        remove(_OUTPUTS)
    # 2-d array to store time values in (-> iterations; v days)
    time_values = [[]]
    for i in range(0, ITERATIONS):
        # log only on first iteration (save outputs of days)
        logging = (i == 0)
        # create names day01 .. day25
        for x in range(1, 26):
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
        max_avg_time_per_day = max(averaged_time_values)
        log(17 * "-" + "runtime duration" + 17 * "-")
        for i in range(0, averaged_time_values.__len__()):
            # Shift i one up because day 0 doesn't exist
            str_i = str(i + 1)
            # if str_i < "10"
            if i < 9:
                # add leading 0
                str_i = "0" + str_i
            # log average of the day (3 decimal places)
            vis = floor((averaged_time_values[i] / max_avg_time_per_day) * _MAX_NUM_HASHTAGS_PER_DAY) * "#"
            log("Day " + str_i + ": " + str(format(averaged_time_values[i], ".3f")) + " seconds" + 5 * " " + vis)
        log(50 * "-")
        # log total execution time (3 decimal places)
        log("Total execution time: " + str(format(sum(averaged_time_values), ".3f")) + " seconds on average")
    else:
        log("There are no files in " + str(_CODE_FOLDER) + " to be run! :(")
    # Add runtime duration to current years' readme
    create_readme()


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


def create_readme():
    """Joins upper part of readme together with the runtime duration statistics and puts it all in
    the README.md for current year"""
    # lines that will be written to README
    rm_to_keep = []
    # Copy first part of Readme (until "--> \n" including)
    with open(_YEAR_FOLDER / "README.md", "r") as rm_f:
        for line in rm_f.readlines():
            rm_to_keep.append(line)
            if line.endswith("-->\n"):
                break
    # get the runtime duration lines
    runtime_dur_lines = []
    # copy from Outputs.txt
    copying = False
    # Begin the bash-code-section in Readme
    rm_to_keep.append("```bash \n")
    # pick out the last section of Outputs.txt
    with open(_OUTPUTS, "r") as o_f:
        for line in o_f.readlines():
            if line.__contains__("runtime duration"):
                copying = True
            if copying:
                runtime_dur_lines.append(line)
    # append the lines with runtime durations to the readme lines (first part)
    rm_to_keep.append(runtime_dur_lines)
    # close the code section
    rm_to_keep.append("``` \n")
    # Write the rm_to_keep lines to README.md, overwriting everything
    with open(_YEAR_FOLDER / "README.md", "w") as rm_f:
        for line in rm_to_keep:
            rm_f.writelines(line)


def run(name: str, logging: bool):
    # get output from calling given python-script
    path = str(_CODE_FOLDER / Path(name + ".py"))
    out = str(subprocess.check_output([_PYTHON, path]), "UTF-8")
    # replace double linebreaks (windows)
    out = out.replace("\r\n", "\n")
    if logging:
        log(out, name)


if __name__ == '__main__':
    # Run all years within range
    if argv.__len__() < 2:
        print("No year specified, running for all years in range " + str(_MIN_YEAR) + "-" + str(_MAX_YEAR))
        for year in range(_MIN_YEAR, _MAX_YEAR + 1):
            run_all(year)
    # Run all existing days for specified year
    elif argv.__len__() == 2:
        run_all(int(argv[1]))
