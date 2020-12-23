from os.path import dirname, realpath
from pathlib import Path
_DAY = "22"
_INPUT_PATH = Path(dirname(realpath(__file__))).parent / Path("inputs") / Path("day" + _DAY + "_input.txt")
# load puzzle input
with open(_INPUT_PATH, 'r') as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
# Player counter (initialized with -1 because it will be incremented if first Player's deck is found)
player_counter = -1
players = []  # decks for the players 1 and 2
# go through all lines
for line in lines:
    # if blank line, skip
    if line == "":
        continue
    # if at start of new deck-definition
    if line.startswith("Player"):
        # increment player counter
        player_counter += 1
        # append a new, empty deck to 'players'
        players.append([])
    else:  # otherwise, line is somewhere inside the deck-definition. Simply append the number in the line to the list
        players[player_counter].append(int(line))


####################################################################################################
def recursive_combat(p1: list, p2: list, p1_previous=None, p2_previous=None):
    """Simulates a round of recursive combat. Returns whether Player 1 won and the winner's final deck as a tuple"""
    # if previous configurations undefined, create them as empty lists
    if p1_previous is None:
        p1_previous = []
    if p2_previous is None:
        p2_previous = []
    # loop until some abort criteria is met (return)
    while True:
        # if configuration has been there before (infinity rule)
        if p1 in p1_previous and p2 in p2_previous:
            # player 1 wins
            return True, get_score(p1)
        # add current configuration to the already seen ones (as a *copy*)
        p1_previous.append(p1.copy())
        p2_previous.append(p2.copy())
        # if Player 1 is out of cards
        if p1.__len__() == 0:
            # Player 2 wins
            return False, p2
        # if Player 2 is out of cards
        elif p2.__len__() == 0:
            # Player 1 wins
            return True, p1
        # draw cards per Player and remove them from the deck
        card_1 = p1[0]
        del p1[0]
        card_2 = p2[0]
        del p2[0]
        # if both have enough cards to recurse
        if p1.__len__() >= card_1 and p2.__len__() >= card_2:
            # go into recursion with a *copy* of the decks and empty previous configurations (whole new game)
            p1_win, _ = recursive_combat(p1[0:card_1].copy(), p2[0:card_2].copy(), [], [])
            # if Player 1 won that sub-game
            if p1_win:
                # append first Player 1's card and then the opponent's card to its deck
                p1.append(card_1)
                p1.append(card_2)
            else:  # if Player 2 won that sub-game
                # append first Player 2's card and then the opponent's card to its deck
                p2.append(card_2)
                p2.append(card_1)
        else:  # if not enough cards for recursion
            # do a "normal" round like in Part A
            if card_1 > card_2:  # Player 1 has higher card
                p1.append(card_1)
                p1.append(card_2)
            else:  # Player 2 has higher card
                p2.append(card_2)
                p2.append(card_1)


def get_score(deck: list) -> int:
    """Calculates the score from a given deck"""
    multiplier = 1  # last number multiplied by 1, second-last by 2, ...
    score = 0  # current score
    for card in deck[::-1]:  # loop through all cards in the deck in *reverse*
        score += multiplier * card  # add the card's value multiplied by 'multiplier' to the score
        multiplier += 1  # increment the multiplier by 1
    return score


def part_a():
    """Part A"""
    # Copy the decks from puzzle-input
    player_1 = players[0].copy()
    player_2 = players[1].copy()
    # as long as both of them have cards left in the deck
    while player_1.__len__() > 0 and player_2.__len__() > 0:
        # draw a card each
        card_1 = player_1[0]
        card_2 = player_2[0]
        # remove them from the deck
        del player_2[0]
        del player_1[0]
        # if Player 1 has a higher card
        if card_1 > card_2:
            # append first Player 1's and then the opponents card to its deck
            player_1.append(card_1)
            player_1.append(card_2)
        else:  # Player 2's card is higher
            # append first Player 2's and then the opponents card to its deck
            player_2.append(card_2)
            player_2.append(card_1)
    # if while-loop has been left
    # if Player 1 is out of cards
    if player_1.__len__() == 0:
        # Player 2 won
        winning_player = player_2
        winner = "Player 2"
    else:  # if Player 2 is out of cards
        # Player 1 won
        winning_player = player_1
        winner = "Player 1"
    # construct return string "Player X wins. Score: XXXX"
    return winner + " wins. Score: " + str(get_score(winning_player))


def part_b():
    """Part B"""
    # *Copy* the decks from puzzle-input
    player_1 = players[0].copy()
    player_2 = players[1].copy()
    # Play a game of recursive combat
    p1_win, deck = recursive_combat(player_1, player_2)
    score = get_score(deck)
    if p1_win:  # if Player 1 won
        return "Player 1 wins. Score: " + str(score)
    else:  # otherwise Player 2 won
        return "Player 2 wins. Score: " + str(score)

# Print out results
print(10 * "-" + " Day " + _DAY + " " + 10 * "-")
print("Part A: " + str(part_a()))
print("Part B: " + str(part_b()))
print(28 * "-")
