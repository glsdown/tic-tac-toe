def check_for_win(board):
    """checks the board (a 3x3 array) to see whether there are 3 in a row the same

    returns:
    0: main_game not over
    -1: main_game ended with a draw
    1: Player 1 won
    2: Player 2 won"""

    size = len(board)

    # build triples for all possible rows
    rows = [[board[i][j] for i in range(size)] for j in range(size)]
    rows += [[board[i][j] for j in range(size)] for i in range(size)]
    rows += [[board[i][i] for i in range(size)]]
    rows += [[board[(size - 1) - i][i] for i in range(size)]]

    # check each in turn to see if all are one player's counter
    for row in rows:
        for i in (1, 2):
            if row.count(i) == size:
                return i

    # if that fails, check if board is full, if yes, draw
    board_contents = [board[i][j] for i in range(size) for j in range(size)]
    if 0 not in board_contents:
        return -1

    # main_game not over yet
    return 0


def get_player_move(board, player=1):
    """
    Requests an input from the player of a valid move. A valid
    move is one where an integer row and column are provided that
    are less than 3, and that location on the board is empty.

    board: a 3x3 array
    player: The player number (or name)
    returns: Tuple(Int, Int)
    """

    print(
        f"Player {player} is up! Please choose a move. Format: 'row column'\n"
    )

    # Force an input in the form "row column" where row and column
    # are integer values
    while True:
        try:
            i, j = (int(x) - 1 for x in input().split())
            if (
                board[i][j] == 0
                and i in range(3)
                and j in range(3)
            ):
                return i, j
            print(
                "Invalid choice, please try again. Format: "
                "'row column'\n"
            )
        except Exception:
            print("Please try again. Format: 'row column'\n")