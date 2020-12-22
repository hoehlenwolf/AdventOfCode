# NOTE: Please put two empty lines at the end of the input file (like the puzzle input)
from enum import Enum
from os.path import dirname, realpath
from pathlib import Path
import numpy as np

_DAY = "20"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")


####################################################################################################
class Direction(Enum):
    """Enum for possible Directions (UP, RIGHT, DOWN, LEFT) applies to neighbour-direction
    as well as to identify borders of an image
    Conversion with this Enum roughly costs 600ms total but makes the code much more readable"""
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


####################################################################################################
class Tile:
    """Tile that has an image, methods to rotate and flip it as well as a method to easily get the borders"""
    def __init__(self, tile_id: int, tile_image: np.ndarray):
        """Initializes a Tile (constructor) with a given `tile_id` and a `tile_image`"""
        # the original tile-image (puzzle input)
        orig_image = np.copy(tile_image)
        # dimensions of the tile-image
        rows, cols = np.shape(orig_image)
        # store the given `tile_id`
        self.id_ = int(tile_id)
        # create a dictionary to store all possible images (every possible transformed version)
        self.image = dict()
        # create a dictionary to store all possible borders (including transformed ones)
        self.borders = dict()
        # *initialize* the nested dictionaries, they are filled with values later
        # self.image and self.borders is a dict with True / False entries (for flipped version)
        for bool_ in [False, True]:
            self.image[bool_] = dict()
            self.borders[bool_] = dict()
            # sub dictionary at self.border[flipped] is a dict with possible rotated versions of the borders
            for dir_ in Direction:
                self.borders[bool_][dir_] = dict()
        # the tile's neighbours are not yet defined, thus every possible direction has 'None' neighbour
        self.neighbours = {Direction.UP: None, Direction.RIGHT: None, Direction.DOWN: None, Direction.LEFT: None}
        # tile is initially not flipped
        self.flipped = False
        # and not rotated
        self.rotate_steps = 0
        # fill the nested dictionaries for image and borders with values
        for flip in [False, True]:  # every possibility of flip
            if flip:
                self.flip()  # keep track of flip
                orig_image = np.flip(orig_image, 1)  # flip the image-matrix
            for rot in range(0, 4):  # every possibility of rotation
                self.rotate()  # keep track of rotation
                orig_image = np.rot90(orig_image)  # actually rotate the image-matrix by 90 degrees
                # put copy of the rotated and or flipped image to appropriate place in dictionary
                self.image[flip][Direction(self.rotate_steps)] = orig_image.copy()
                # put borders of rotated and or flipped image to appropriate place in dictionary
                self.borders[flip][Direction(self.rotate_steps)][Direction.UP] = "".join(orig_image[0])  # UP
                self.borders[flip][Direction(self.rotate_steps)][Direction.DOWN] = "".join(orig_image[rows - 1])  # DOWN
                # LEFT
                left = ""
                # extract first entry of each row and append it to the border
                for row in orig_image:
                    left += row[0]
                self.borders[flip][Direction(self.rotate_steps)][Direction.LEFT] = left
                # RIGHT
                right = ""
                # extract last entry of each row and append it to the border
                for row in orig_image:
                    right += row[cols - 1]
                self.borders[flip][Direction(self.rotate_steps)][Direction.RIGHT] = right

    def __str__(self):
        """Returns a String-representation of the Tile (it's ID)"""
        return str(self.id_)

    def print(self):
        """Pretty-prints the Tile (like an actual image)"""
        res = ""
        for line in self.image:
            for pixel in line:
                res += pixel
            res += "\n"
        print(res)

    def get_border(self, direction: Direction):
        """Returns the border of the Tile (border specified by `direction`; Direction.UP => upper border etc.)
        with respect to current flip and rotation of the tile"""
        return self.borders[self.flipped][Direction(self.rotate_steps)][direction]

    def flip(self):
        """Flips the Tile along the vertical axis (horizontal additionally would be redundant)"""
        # Note: Does not actually flip the tile, just keeps track of the flip
        # the flipped tile-image has already been created and stored in the self.image dict
        # at the appropriate position in __init__
        self.flipped = not self.flipped

    def rotate(self, num_turns_clockwise: int = 1):
        """Rotates the Tile clockwise by `num_turns_clockwise` 90-degree steps"""
        # Note: Does not actually rotate the tile, just keeps track of the rotation
        # the rotated tile-image has already been created and stored in the self.image dict
        # at the appropriate position in __init__
        self.rotate_steps = (self.rotate_steps + num_turns_clockwise) % 4  # account for more than 360 degree rotations

    def get_unset_neighbours(self):
        """Returns a list of Directions that this tile has no neighbour at"""
        res = []  # empty list/array
        # loop through all neighbouring position
        for n in self.neighbours:
            # if value there is None
            if self.neighbours[n] is None:
                # add Direction to the result-list
                res.append(n)
        return res

    def get_neighbour_count(self) -> int:
        """Returns the number of neighbours this Tile has"""
        # subtract the amount of *unset* neighbours from the total number of possible neighbours
        return self.neighbours.__len__() - self.get_unset_neighbours().__len__()

    def get_image(self):
        """returns the tile-image with respect to it's rotation and flip"""
        return self.image[self.flipped][Direction(self.rotate_steps)]


####################################################################################################
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
tiles = []  # list of tiles
id_ = -1  # initialize tile-id with -1
image = []  # initialize tile-image with empty array
# go through every line
for line in lines:
    if line == "":  # if empty line the current Tile's definition has ended
        # create a Tile from the previously gathered information
        t = Tile(id_, np.array(image))
        # and append it to the list of Tiles
        tiles.append(t)
    else:  # if not empty line, gather information
        if line.startswith("Tile"):  # if line begins with "Tile"
            # extract the tile-id (after the first whitespace without ending ":")
            id_ = line.split(" ")[1][:-1]
            # (re-)set image to an empty array
            image = []
        else:  # if line is not empty and does not start with "Tile", it contains the current Tile's pixel
            line_arr = []  # array for one line
            # append every character in the current line to the 'line_arr'
            for c in line:
                line_arr.append(c)
            # append the 'line_arr' to the Tile's image
            image.append(line_arr)


####################################################################################################
def docks_to(locked: Tile, to_dock: Tile, modify_to_dock: bool) -> bool:
    """Checks if two tiles fit together"""
    if not modify_to_dock:  # if 'to_dock' tile can *NOT* be rotated and or flipped and is fixed in it's orientation
        for poss_dock_positions in locked.get_unset_neighbours():  # check possible free neighbours for 'locked' Tile
            # get opposing side (side at which 'to_dock' has to dock onto 'locked'
            opposing_site = Direction((poss_dock_positions.value - 2) % 4)
            # if the borders match
            if locked.get_border(poss_dock_positions) == to_dock.get_border(opposing_site):
                # if they match, store them as neighbours mutually
                locked.neighbours[poss_dock_positions] = to_dock
                to_dock.neighbours[opposing_site] = locked
                return True  # docking was successful
        return False  # could not dock them together
    else:  # if 'to_dock' can be rotated
        for poss_dock_positions in locked.get_unset_neighbours():  # check possible free neighbours for 'locked' Tile
            # get opposing side (side at which 'to_dock' has to dock onto 'locked'
            opposing_site = Direction((poss_dock_positions.value - 2) % 4)
            # go through all possibilities of flip
            for flip in [False, True]:
                if flip:
                    to_dock.flip()
                # go through all possibilities of rotation
                for rot in range(0, 4):
                    to_dock.rotate()
                    # check if the Tiles match with current orientation of 'to_dock'
                    if locked.get_border(poss_dock_positions) == to_dock.get_border(opposing_site):
                        # if they match, store them as neighbours mutually
                        locked.neighbours[poss_dock_positions] = to_dock
                        to_dock.neighbours[opposing_site] = locked
                        return True  # docking was successful
        return False  # could not dock them together

def print_tiles():
    """Prints all Tile's ID in matrix form to represent the order of tiles"""
    # Only works if all Tiles in global tiles-array have correct neighbours set
    tile = tiles[0]  # get the first Tile (can be at any position in the resulting stitched together image)
    # go Up one Tile as often as possible
    while tile.neighbours[Direction.UP] is not None:
        tile = tile.neighbours[Direction.UP]
    # go Left one Tile as often as possible
    while tile.neighbours[Direction.LEFT] is not None:
        tile = tile.neighbours[Direction.LEFT]
    # tile is now the leftmost uppermost Tile in the whole image
    t_line = tile  # current Tile is the leftmost uppermost Tile tile
    line = ""  # current line to be printed
    # loop through all rows of Tiles
    while t_line is not None:
        # loop through all columns of Tiles
        while t_line is not None:
            # append the Tile's id to the line (with some whitespace)
            line += "   " + str(t_line)
            # if current Tile has a right-neighbour
            if t_line.neighbours[Direction.RIGHT] is not None:
                # go the the right adjacent Tile
                t_line = t_line.neighbours[Direction.RIGHT]
            else:  # otherwise break out of the loop for columns
                break
        print(line)  # print the current line
        tile = tile.neighbours[Direction.DOWN]  # go one row down (tile is for remembering the beginning of current row)
        line = ""  # reset current line
        t_line = tile  # set next Tile to be processed to the beginning of the new row


def find_sea_monster(stitched_image: np.ndarray):
    """Checks for sea-monsters in the given `stitched_image`"""
    correct_orientation = False  # boolean to flag whether the image is rotated correctly (for returning a boolean
    # if the given `stitched_image` is correctly oriented and thus contains any sea-monsters)
    #
    # offsets of "#" pixel that also have to be "#" in format of (row_offset, col_offset) starting with leftmost
    # pixel in sea-monster pattern -> Represents the Hashtag-pattern in a sea-monster
    offsets = [(0, 0), (1, 1), (1, 4), (0, 5), (0, 6), (1, 7), (1, 10), (0, 11), (0, 12), (1, 13), (1, 16), (0, 17),
               (0, 18), (0, 19), (-1, 18)]
    # loop through all rows (first and last row are ignored, because I identify sea-monsters starting from the leftmost
    # pixel in the second row of the sea-monster pattern
    for row_index in range(1, stitched_image.__len__() - 1):
        # loop through all columns (the last 19 columns are ignored because a sea-monster is 20 pixels long and thus
        # the starting pixel has to be >= 20 pixels away from right border)
        for col_index in range(0, stitched_image[row_index].__len__() - 19):
            # flag if current pixel at [row_index][col_index] can be a starting pixel of a sea-monster
            possible = True
            # go through all offsets to check (from the starting pixel)
            for row_off, col_off in offsets:
                # if there is no "#" at the offset positions
                if stitched_image[row_index + row_off][col_index + col_off] != "#":
                    # there is no sea monster starting at the starting pixel
                    possible = False
                    # break out (because other offsets don't need to be checked if one has already failed)
                    break
            # if starting pixel is the beginning of a sea-monster
            if possible:
                # mark all the "#" in it with "O" (to later count the residual "#")
                for row_off, col_off in offsets:
                    stitched_image[row_index + row_off][col_index + col_off] = "O"
                    # set the flag for 'correct_orientation' to True to signal that the given image is
                    # rotated correctly and does contain one or more sea-monsters
                    correct_orientation = True
    # return if given image was oriented correctly
    return correct_orientation


def part_a():
    """Part A"""
    # add first Tile in tile-list to the list of already set Tiles (can not be moved / rotated / flipped anymore)
    # Thus others need to dock to the already_set tiles, not the other way around
    tiles_already_set = [tiles[0]]
    # tiles that have not been placed yet (they are on their own / solo)
    tiles_solo = tiles.copy()
    # remove the one starting Tile that has already been set from the tiles_solo
    tiles_solo.remove(tiles[0])
    # as long as there are Tiles that have not been docked yet
    while tiles_solo.__len__() != 0:
        # list of Tiles a solo-Tile has been placed next to (they can potentially be removed
        # from tiles_already_set if they have 4 neighbours; this increases performance a bit)
        placed = []
        solo_index = 0  # start at solo_index 0 in the tiles_solo list
        while solo_index < tiles_solo.__len__():
            # get the solo Tile at solo_index
            solo = tiles_solo[solo_index]
            # try to dock it to any of the already-set Tiles
            for already_set in tiles_already_set:
                # Note: because this keeps running after solo has been docked to *one* already-set Tile
                # every neighbour will be found and set appropriately
                #
                # also pass if solo_tile can be rotated and flipped or if it should stay in place
                # if placed.__len__() is > 0 solo should *NOT* be modified as this would mess up the stored neighbours
                if docks_to(already_set, solo, placed.__len__() == 0):
                    # if it succeeded, remember it
                    placed.append(already_set)
            if placed.__len__() > 0:  # if solo Tile has been placed
                for already_set in placed:  # check all Tiles it has been placed next to
                    if already_set.get_neighbour_count() == 4:  # if they have 4 neighbours
                        tiles_already_set.remove(already_set)  # they don't need to be checked again in the next rounds
                tiles_solo.remove(solo)  # solo-Tile is no longer solo
                if solo.get_neighbour_count() != 4:  # if solo-Tile has empty neighbours
                    tiles_already_set.append(solo)  # add it to the already set Tiles (to be checked in the next rounds
                    # if another solo-Tile can dock to them)
                break  # break out and start over
            solo_index += 1  # if solo-Tile could not be placed, go to the next possible solo-Tile in tiles_solo
    # print the configuration of Tile-IDs
    print_tiles()
    # product is 1 (modified later by *= )
    prod = 1
    # loop through all Tiles
    for tile in tiles:
        # if tile is a corner-Tile (has only 2 neighbours)
        if tile.get_neighbour_count() == 2:
            # multiply 'prod' by tile's Tile-ID
            prod *= tile.id_
    # return the product
    return prod


def part_b():
    """Part B"""
    # get first Tile
    tile = tiles[0]
    # go to uppermost leftmost Tile
    while tile.neighbours[Direction.UP] is not None:
        tile = tile.neighbours[Direction.UP]
    while tile.neighbours[Direction.LEFT] is not None:
        tile = tile.neighbours[Direction.LEFT]
    # t is now upper left Tile
    whole_image = []  # whole_image after stitching the Tiles together
    t_cur_row_beginning = tile  # Tile at the beginning of the current row
    row_counter = 1  # row counter (always start with 1 and ignore the upper border of Tiles)
    rows, cols = np.shape(t.get_image())  # get dimensions of tile-image
    while t_cur_row_beginning is not None:  # loop through all rows
        whole_row = []  # Stitch together Pixels per row in tile-image for all Tiles in this row
        t_current = t_cur_row_beginning  # current Tile
        while t_current is not None:
            for pixel in t_current.get_image()[row_counter][1:-1]:
                whole_row.append(pixel)
            t_current = t_current.neighbours[Direction.RIGHT]  # move current Tile one to the right
        whole_image.append(whole_row)  # if row finished, append the PIXEL-Row to the whole image
        # increment row_counter (for rows in the tile-image per Tile)
        row_counter += 1
        if row_counter == rows - 1:  # if row previous to last row was just processed(last row in Tile-image is ignored)
            row_counter = 1  # reset row_counter to 1
            t_cur_row_beginning = t_cur_row_beginning.neighbours[Direction.DOWN]  # move one TILE-Row down
    # convert whole_image to a numpy array (2D char-Array)
    whole_image = np.array(whole_image)
    # Now 'whole_image' is the finished image stitched together from the Tiles in the correct order
    # Try to rotate and flip this 'whole_image' until sea-monsters can be found
    for flip in [False, True]:  # every possibility of flip (along vertical axis)
        if flip:
            whole_image = np.flip(whole_image, 1)
        for rot in range(0, 4):  # every possibility of rotation
            whole_image = np.rot90(whole_image)
            res = find_sea_monster(whole_image)  # look for sea-monsters in whole_image with current orientation
            if res:  # if sea-monster could be found (image was rotated and flipped correctly)
                for row in whole_image:  # print out the correctly oriented 'whole_image' with marked sea-monsters
                    print("".join(row))
                # count hashtags that don't belong to a sea-monster ("#" in sea-monster have been replaced by "O")
                hashtags_not_in_monster = 0
                for row in whole_image:  # loop through all rows
                    for pixel in row:  # loop through every pixel
                        if pixel == "#":  # if pixel is hashtag
                            hashtags_not_in_monster += 1  # increment counter
                return hashtags_not_in_monster  # return counter


# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
# fetch results because part_a() and part_b() will print a lot, final result will be at the bottom this way)
res_a = str(part_a())
res_b = str(part_b())
print("Part A: " + res_a)
print("Part B: " + res_b)
print(28 * "-")
