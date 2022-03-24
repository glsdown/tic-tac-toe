from copy import deepcopy
from typing import Optional, Union

from helpers.supporting_functions import check_for_win, get_player_move

__all__ = ["Game"]


class Game:
    def __init__(
        self,
        size: int = 3,
        board: Optional[list[list[Union[str, int]]]] = None,
    ):
        """create a new main_game object, consisting of an empty board

        size: the number of rows and columns on the board
        board: the main game board if a different board is required - this
        takes precedent over the size parameter
        """
        # Create the game board
        if board is None:
            board = [[0] * size for _ in range(size)]
        else:
            if len(board) != len(board[0]):
                raise ValueError("Invalid board - the board must be square")
            size = len(board)
        self.board = deepcopy(board)

        # Identify the number of moves
        self.moves = 0

        # Store the size of the board
        self.size = size

        # Get the possible counters
        self.counters = [" ", "o", "x"]

        # Start with player 1
        self.current_player = 1

        # Initialise the opponent
        self.opponent = Bot(2, self.board)

        # Record if the game is finished
        self.complete = False

    def place(self, player: int, i: int, j: int):
        """place a counter on square (i, j)"""
        self.board[i][j] = player
        self.moves += 1

    def check_for_win(self):
        """checks the board (a 3x3 array) to see whether there are 3 in a row the same

        returns:
        0: main_game not over
        -1: main_game ended with a draw
        1: Player 1 won
        2: Player 2 won"""
        return check_for_win(self.board)

    def visualise(self):
        """Display the board in a nice way"""
        # Create a line template
        line = "   " + "---".join(["+"] * (self.size + 1))
        # Print out the column numbers at the top
        print(
            "    "
            + " ".join([str(i).center(3) for i in range(1, self.size + 1)])
        )
        # Print a line forming the top row
        print(line)
        # Print each row:
        # - The row number on the left
        # - The left edge of the square
        # - The counters separated by borders
        # - The right edge of the square
        # - A line at the bottom
        for r in range(self.size):
            print(
                str(r + 1).join([" "] * 2)
                + "|"
                + "|".join(
                    [
                        (" " + self.counters[self.board[r][c]] + " ").center(3)
                        for c in range(self.size)
                    ]
                )
                + "|"
            )
            print(line)
        # Add a blank line at the bottom
        print("\n")

    def game_loop(self):
        """the main game loop"""

        # Display starting instructions
        print("You're playing tic-tac-toe!")
        print("Good luck!\n\n")

        # Play the game
        while True:
            # Display the board
            self.visualise()

            # Get the player's move
            if self.current_player == 1:
                i, j = get_player_move(self.board, self.current_player)
            else:
                i, j = self.opponent.choose_move(self)

            # Place the counter
            self.place(self.current_player, i, j)
            # Check if the board is in a 'win' state
            win_state = self.check_for_win()

            # If the game has ended display the results
            if win_state:
                self.complete = True
                self.visualise()
                if win_state == -1:
                    print("Draw! No... not your weapons...")
                else:
                    print("Player " + str(self.current_player) + " wins!")
                break

            # Change the player
            self.current_player = self.current_player % 2 + 1

        # Display the end result
        print("Thanks for playing!")


class Bot:
    def __init__(self, player: int, board: list[list[Union[str, int]]]):
        """Initialse the bot player

        board: a 'square' board grid of locations
        """
        self.current_player = player
        self.board_size = len(board)
        self.board = deepcopy(board)

    def update_board(self, board: list[list[Union[str, int]]]):
        """Update the board the bot is playing on

        board: a 'square' board grid of locations
        """
        self.board = deepcopy(board)

    def valid_moves(self) -> list[tuple[int]]:
        """Find the valid moves available

        returns: all moves (i, j) on the current board that do not have a
        counter on them
        """
        return [
            (i, j)
            for i in range(self.board_size)
            for j in range(self.board_size)
            if self.board[i][j] == 0
        ]

    def alphabeta(
        self,
        max_player: bool = True,
        alpha: float = -float("inf"),
        beta: float = float("inf"),
    ) -> tuple[int, tuple]:
        """Recursive function to simulate all possible moves, and use
        alpha-beta pruning to choose the optimum one

        max_player: Whether the current player is the one we are trying to
        make 'win' i.e. the player we want to maximise the score of
        alpha: The best (highest-value) score that has been identifier for the
        bot player.
        beta: The best (lowest-value) score that has been identified for the
        human player.
        returns: The score for the round, and the move that should be played
        next to have the best chance of achieving it.
        """
        # Check if the board is in a win state (base case)
        win_state = check_for_win(self.board)

        # Check if one of the players won
        if win_state in (1, 2):
            # If the bot won, then return a 'positive' result
            if win_state == self.current_player:
                return 1, None
            # If the bot didn't win, return a 'negative' result
            else:
                return -1, None
        # If the game ended in a draw, then return a 'neutral' result
        elif win_state == -1:
            return 0, None

        # If the player is the one that we are trying to make 'win'
        if max_player:
            # Playing as the bot
            player = self.current_player
            # Here we want to maximise the score, so set the comparison low
            best_value = -float("inf")
        else:
            # Playing as the other player
            player = (self.current_player % 2) + 1
            # Here we want to minimise the score, so set the comparison low
            best_value = float("inf")

        # Set the best move as a default value of None
        best_move = None

        # Check each move in turn to find the best one
        for move in self.valid_moves():

            # Mock 'play' that move on the current board
            self.board[move[0]][move[1]] = player

            # Identify the outcome by continuing to play
            val, _ = self.alphabeta(not max_player, alpha, beta)

            if max_player:
                # Work out whether the current 'max' value or the new 'score'
                # is better - this becomes the new 'alpha'
                alpha = max(alpha, val)
                update_best = val > best_value
            else:
                # Work out whether the current 'min' value or the new 'score'
                # is better - this becomes the new 'beta'
                beta = min(beta, val)
                update_best = val < best_value

            # If this move beats the previous move options...
            if update_best:

                # This becomes the next best move and we update the score
                best_move = move
                best_value = val

            # Reset the move on the board
            self.board[move[0]][move[1]] = 0

            # 'Prune' this branch if it doesn't look like it's going to
            # win
            if beta <= alpha:
                break

        # Once all potential moves have been simulated, return the best
        # option, as well as the score
        return best_value, best_move

    def choose_move(self, game: Game) -> tuple[int]:
        """Get the best next move

        returns: the integer row, column move as a tuple
        """
        # Update the bot's board with the latest layout in the game
        self.update_board(game.board)
        # Get the 'best' available move
        _, move = self.alphabeta()
        return move
