import math
from os.path import dirname, realpath
from pathlib import Path
import numpy as np
from time import time_ns

_DAY = "13"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
lines = []
arrival_timestamp = -1
bus_ids = []


def load_puzzle():
    global lines, arrival_timestamp, bus_ids
    with open(_INPUT_PATH, 'r') as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    # Arrival timestamp for A is in the first line
    arrival_timestamp = int(lines[0])
    # bus IDs are comma-separated in the second line
    bus_ids = [bus_id for bus_id in lines[1].split(",")]


####################################################################################################
def lcm(x: int, y: int) -> int:
    """Least common multiple"""
    # Calculate product of x * y, take the absolute value of that (in case one of the numbers is negative)
    # and divide ( // = integer division)  by "greatest common divisor".
    # This will produce "least common multiple"
    return abs(x*y) // math.gcd(x, y)


def part_a():
    """Part A"""
    # filter out buses that are not operating (id = "x")
    bus_ids_operating = [int(bus_id) for bus_id in bus_ids if bus_id != "x"]
    # convert to numpy array for easier calculation later on
    bus_ids_operating = np.array(bus_ids_operating)
    timestamps = np.array(bus_ids_operating)
    # loop until one timestamp in timestamps-array is >= than my arrival's timestamp
    while True:
        # go through all timestamps (one per bus)
        for i in range(timestamps.__len__()):
            # if one of them is greater than my arrival's timestamp
            if timestamps[i] >= arrival_timestamp:
                # return the bus ID multiplied by the waiting time
                return bus_ids_operating[i] * (timestamps[i] - arrival_timestamp)
        # if timestamps aren't large enough yet, add their buses' ID onto each of them
        # to go to the next "step"  or rather departing bus of that line's ID
        timestamps += bus_ids_operating


def part_b():
    """Part B"""
    # Create Dict with key:value pairs of {Bus-ID: Offset}
    # where Offset is the amount of numbers this bus should depart later than the first one
    bus_ids_operating = dict()
    for i in range(0, bus_ids.__len__()):
        # if bus is operating (has a number)
        if bus_ids[i] != "x":
            # add it to the operating bus dict with appropriate Offset 'i'
            bus_ids_operating[int(bus_ids[i])] = i
    # begin searching for timestamp at 0
    timestamp = 0
    # initial step_size is 1
    step_size = 1
    # go through all buses that are operating
    for bus in bus_ids_operating:
        # boolean to flag whether a timestamp for the current bus has been found so that it and all previous buses meet
        # the criteria (departing times after each other with the index being the offset)
        found = False
        # loop until a timestamp was found so that all buses' departures up to the current one meet the criteria
        while not found:
            # increase 'timestamp' by 'step_size'
            timestamp += step_size
            # if the timestamp at which the bus departs ( = "current" timestamp plus the offset) is divisible by the
            # buses' ID
            if (timestamp + bus_ids_operating[bus]) % bus == 0:
                # flag that timestamp has been found, to get out of the loop
                # break in combination with while True would also work
                found = True
                # increase the 'step_size' by multiplying it with the buses' ID. This can be done because the
                # previous 'step_size' was divisible by all the previous buses' IDs (plus their respective offset)
                # and multiplying it with an integer does not change that The new step_size thus keeps the criteria
                # for all previous buses valid and multiplying it with the current buses' ID will produce the next
                # bigger number that is divisible by all buses
                # --------------------------------------------------------------------------------------------------
                # step_size *= bus
                # NOTE: thinking about this I'm a bit surprised this worked, but it seems to be due
                # to the fact that all bus IDs are prime numbers, so this exploits that fact a bit. If the buses' IDs
                # are not all prime, you most likely will skip the right timestamp
                # -------------------------------------------------------------------------------------------------
                # **Solution** (Since there is no  guarantee that the bus IDs will be prime):
                # Set step_size to "least common multiple" of previous
                # 'step_size' and 'bus' ID. for prime 'bus' IDs this will be = 'bus' * previous 'step_size'
                # and this will *always* produce a number that is divisible by all previous bus IDs including
                # the current one
                step_size = lcm(step_size, bus)
    return timestamp


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
