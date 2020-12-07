from pathlib import Path
from os.path import dirname, realpath
_CURR_DIR = Path(dirname(realpath(__file__)))
def inputs():
    for i in range(1, 26):
        if i < 10:
            i_str = "0" + str(i)
        else:
            i_str = str(i)
        name = Path("day" + i_str + "_input.txt")
        pfad = _CURR_DIR / Path("inputs") / name
        f = open(pfad, "w+")
inputs()