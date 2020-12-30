from os.path import isfile, dirname, realpath
from os import remove
from sys import platform, argv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# if on windows
if platform == "win32":
    _PYTHON = "python"
else:  # otherwise
    _PYTHON = "python3"
# Variables for printout and logging
per_day_output = True  # if for each day there should be a dayXX_output.txt
printout = True  # if printout in console is wanted
summarized_output = True  # if there should be Outputs.txt for combined Output of all days
TIME_MULTIPLIER = int(1E06)
# Number of iterations for constructing average runtime
ITERATIONS = {2015: 10, 2016: 10, 2017: 10, 2018: 10, 2019: 10, 2020: 1, 2021: 10}
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

    # create names day01 .. day25
    for day in range(1, 26):
        day_str = str(day)
        if day < 10:
            day_str = "0" + day_str
        name = "day" + day_str
        day_class = __import__("aoc_" + str(year_to_run) + ".code." + name, fromlist=[''])
        # if dayXX exists
        if isfile(_CODE_FOLDER / Path(name + ".py")):
            # run the file
            run_method_per_day = getattr(day_class, "run")
            for i in range(0, ITERATIONS[year_to_run]):
                part_a, part_b, time_setup, time_a, time_b = run_method_per_day()

                # enlarge time_values array if new day reached for the first time
                if day - 1 == time_values.__len__():
                    time_values.append([])
                # append time_diff to x-th row of 2-d array time_values
                time_values[day - 1].append((day_str, time_setup, time_a, time_b))
                if i == 0:
                    out = 10 * "-" + " Day " + day_str + " " + 10 * "-" + "\n"
                    out += "Part A: " + str(part_a) + "\n"
                    out += "Part B: " + str(part_b) + "\n"
                    log(out, name)
    if time_values.__len__() != 0 and time_values[0].__len__() != 0:
        averaged_time_values = []
        total_time = 0
        for days_times in time_values:
            avg_setup, avg_a, avg_b = 0, 0, 0
            day_name = ""
            for iteration in days_times:
                # index 0 is the day number in string representation (01, 02, ... 25)
                day_name = iteration[0]
                avg_setup += iteration[1]
                avg_a += iteration[2]
                avg_b += iteration[3]
            avg_setup /= ITERATIONS[year_to_run] * TIME_MULTIPLIER
            avg_a /= ITERATIONS[year_to_run] * TIME_MULTIPLIER
            avg_b /= ITERATIONS[year_to_run] * TIME_MULTIPLIER
            total_time += avg_setup + avg_a + avg_b
            averaged_time_values.append((day_name, avg_setup, avg_a, avg_b))
        log("---------------runtime duration (ms)---------------")
        log(13 * " " + "SETUP" + 17 * " " + "A" + 19 * " " + "B")
        for avg_day in averaged_time_values:
            log("Day " + avg_day[0] + ":" + "{:10.1f}".format(avg_day[1]) + 10 * " " + "{:10.1f}".format(
                avg_day[2]) + 10 * " " + "{:10.1f}".format(avg_day[3]))
        log("\nTotal execution time: " + "{:10.1f}".format(total_time) + " ms on average (" + str(
            ITERATIONS[year_to_run]) + " iterations)")
        create_runtime_vis(averaged_time_values, year_to_run)
        create_readme()

    else:
        log("There are no files in " + str(_CODE_FOLDER) + " to be run! :(")


def log(text: str, name: str = None):
    file_log_text = text
    if not file_log_text.endswith("\n"):
        file_log_text += "\n"
    file_log_text = file_log_text.encode("utf-8").decode("utf-8")
    if printout:
        print(text)

    if per_day_output and name is not None:
        with open(_OUTPUT_FOLDER / Path(name + "_output.txt"), 'w+') as f:
            f.write(file_log_text)

    if summarized_output:
        with open(_OUTPUTS, "ab+") as f:
            f.write(file_log_text.encode("UTF-8"))


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


def create_runtime_vis(runtime_durations, year_to_run):
    """Builds a visualization of a given runtime duration in relation to others in the same year"""
    times_setup = []
    times_a = []
    times_b = []
    day_names = []
    for day_runtime in runtime_durations:
        day_names.append(day_runtime[0])
        times_setup.append(day_runtime[1])
        times_a.append(day_runtime[2])
        times_b.append(day_runtime[3])
    days = np.arange(runtime_durations.__len__())
    bar_width = 0.35
    setup = plt.bar(days, times_setup, bar_width)
    part_a = plt.bar(days, times_a, bar_width, bottom=times_setup)
    part_b = plt.bar(days, times_b, bar_width, bottom=times_a)
    plt.ylabel("Milliseconds")
    plt.title("Runtime Durations AoC " + str(year_to_run))
    plt.xticks(days, day_names, rotation=90)
    plt.legend((part_b[0], part_a[0], setup[0]), ("Part B", "Part A", "Setup"))
    # plt.show()
    plt.savefig(_YEAR_FOLDER / "img" / "runtime_durations_2020.jpg")


if __name__ == '__main__':
    # Run all years within range
    if argv.__len__() < 2:
        print("No year specified, running for all years in range " + str(_MIN_YEAR) + "-" + str(_MAX_YEAR))
        for year in range(_MIN_YEAR, _MAX_YEAR + 1):
            run_all(year)
    # Run all existing days for specified year
    elif argv.__len__() == 2:
        run_all(int(argv[1]))
