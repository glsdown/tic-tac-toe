from game import Game, TicTacToeWindow, TicTacToeWindowIn2D


def menu():
    """Display the main game menu"""

    print(
        "--------------------------------------------\n"
        "Hello and welcome to Tic Tac Toe.\n"
        "--------------------------------------------\n\n"
        "Which game would you like to play?\n"
        "1. Via the Command Line against a Bot\n"
        "2. Using a GUI against a Bot\n"
        "3. 2D Tic-Tac-Toe against a Human\n"
        "4. Leave and never return\n"
    )
    choice = ""
    while choice not in ["1", "2", "3", "4"]:
        choice = input("1, 2, 3 or 4: ")

    if choice == "1":
        Game().game_loop()
    elif choice == "2":
        TicTacToeWindow().mainloop()
    elif choice == "3":
        TicTacToeWindowIn2D().mainloop()

    print("\nGoodbye")


if __name__ == "__main__":
    menu()
