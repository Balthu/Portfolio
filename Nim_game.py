"""
Nim's game is a duel in which players remove 1 to 3 matches from a pile of 20. Whoever removes the last match loses.

This version of Nim's game features three game modes: a duel between two human players, a versus against an easy
artificial intelligence and a versus against a competitive artificial intelligence.

Easy artificial intelligence fires 1 to 3 matches at random. It only optimizes its shots when there are 3 matches
left at most.

Competitive artificial intelligence optimizes its moves by leaving a number of matches that is not a multiple of 4.In
addition, the number of matches can be between 20 and 100 in this game mode.
__author__ = 'Lio'
"""

from random import randint
from time import sleep


def game_mode() -> tuple[int, int]:
    """
    Allows the user to select the game mode and, if applicable, the number of matches.
    Returns:
        tuple: A tuple containing the selected game mode and the number of matches.
    """
    mode = 0
    nb_matches = 20
    print("Select your game mode \n 1 : VS Human \n 2 : VS Dumb AI \n 3 : VS Smart AI ")
    while True:
        try:
            mode = int(input("Choose your game mode by indicating its numerical value : "))
            if mode not in [1, 2, 3]:
                print("Please enter a valid mode : 1, 2 or 3")
            else:
                break
        except ValueError:
            print("Please enter a numerical value : 1, 2 or 3!")

    if mode == 3:
        while True:
            try:
                nb_matches = int(input("Enter number of matches (between 20 and 100 inclusive)"))
                if nb_matches < 20 or nb_matches > 100:
                    print("Please note that the number of matches must be between 20 and 100.")
                else:
                    break
            except ValueError:
                print("Please enter a numerical value : 1, 2 or 3!")
    return mode, nb_matches


def gameboard(nb_matches: int):
    """
    Displays the current state of the game board.
    Args:
        nb_matches (int): The number of matches remaining.
    """
    if nb_matches != 0:
        print(f"Number of matche(s) : {nb_matches} - " + ("I " * nb_matches))
    else:
        print("The game board is empty!")


def players_name(mode: int) -> list:
    """
    Allows the players to enter their names.
    Args:
        mode (int): The selected game mode.
    Returns:
        list: A list containing the names of the players.
    """
    nicknames = [str(input("Enter the nickname of the main player"))]
    if mode == 1:
        while True:
            player_2 = str((input("Enter the nickname of the challenger")))
            if player_2 == nicknames[0]:
                print("The challenger's nickname cannot be that of the main player.")
            else:
                nicknames.append(player_2)
                break
    else:
        nicknames.append("AI")
    return nicknames


def random_firstplayer(nicknames: list) -> int:
    """
    Randomly selects the first player and announces it.
    Args:
        nicknames (list): List containing the names of the players.
    Returns:
        int: The index of the first player in the list.
    """
    a = randint(1, 2)
    print(f"{nicknames[a - 1]} starts the game")
    return a


def alternate_player(a: int) -> int:
    """
    Alternates between players.
    Args:
        a (int): The index of the current player.
    Returns:
        int: The index of the next player.
    """
    if a == 1:
        a = 2
    else:
        a = 1
    return a


def withdraw_matches(nb_matches: int, player: str) -> int:
    """
    Handles the withdrawal of matches by human players.
    Args:
        nb_matches (int): The number of matches remaining.
        player (str) : nickname of playing player.
    Returns:
        int: The updated number of matches after withdrawal.
    """
    while True:
        try:
            withdraw = int(input(f"How many matches would you like to remove, {player}, (1, 2 or 3)?"))
            if withdraw <= 3 and 0 < withdraw <= nb_matches:
                break
            elif withdraw > 3:
                print("You cannot select more than 3 matche(s)")
            elif withdraw <= 0:
                print("Don't try to cheat. Only positive values between 1 and 3 inclusive work.")
            elif nb_matches < withdraw:
                print(f"{nb_matches} matche(s) left. Please do not enter a higher number. ")
        except ValueError:
            print("Please enter a numerical value : 1, 2 or 3!")
    return nb_matches - withdraw


def withdraw_ai(nb_matches: int, mode: int):
    """
    Handles the withdrawal of matches by the AI.
    Args:
        nb_matches (int): The number of matches remaining.
        mode (int): The selected game mode.
    Returns:
        int: The updated number of matches after withdrawal.
    """
    withdraw = 0
    sleep(1)
    print("The AI is thinking about its next move...")

    if mode == 2:
        withdraw = randint(1, 3)

    if mode == 3:
        # The AI's goal is to leave a multiple of 4 (+ 1) matches for the player.
        withdraw = (nb_matches % 4) - 1
        if withdraw == -1:
            withdraw = 3
        # Handling the case where the player has managed to trick the AI
        elif withdraw == 0:
            withdraw = randint(1, 3)

    # Endgame management with optimized moves
    if nb_matches == 2 or nb_matches == 3:
        withdraw = nb_matches - 1
    elif nb_matches == 1:
        withdraw = 1
    sleep(1)
    print(f"The AI has decided to remove {withdraw} matche(s)")
    return nb_matches - withdraw


def defeat(nb_matches: int, player: str) -> bool:
    """
    Checks if a player has lost.
    Args:
        nb_matches (int): The number of matches remaining.
        player (str): nickname of the losing player.
    Returns:
        bool: True if the player has lost, False otherwise.
    """
    if nb_matches == 0:
        print(f"You lose, {player}!")
        return True
    return False


if __name__ == '__main__':
    mode, nb_matches = game_mode()
    nicknames = players_name(mode)
    gameboard(nb_matches)
    a = random_firstplayer(nicknames)

    while True:
        if mode == 1:
            nb_matches = withdraw_matches(nb_matches, nicknames[a - 1])
            gameboard(nb_matches)

        if mode == 2 or mode == 3:
            if a == 2:
                nb_matches = withdraw_ai(nb_matches, mode)
                gameboard(nb_matches)

            else:
                nb_matches = withdraw_matches(nb_matches, nicknames[a - 1])
                gameboard(nb_matches)

        if defeat(nb_matches, nicknames[a - 1]):
            break

        # Allows you to alternate players and then restart the loop
        a = alternate_player(a)
