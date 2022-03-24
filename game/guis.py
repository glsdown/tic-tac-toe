import tkinter as tk
from copy import deepcopy

from .game_class import Game

__all__ = ["TicTacToeWindow", "TicTacToeWindowIn2D"]


class TicTacToeWindow(tk.Tk):
    """class defining the window that the main_game will play in"""

    def __init__(self):
        """initialiser - subclass of Tk"""
        super().__init__()

        # The main title for the window
        self.title("Tic Tac Toe")
        # Create a 'game' instance
        self.game = Game()
        # Create the basic outline
        self.create_gameboard_widget("Your Turn! Click a square to begin.")

    def create_gameboard_widget(self, status: str):
        """initialise the main_game board graphics

        status: the message to display on the page
        """

        # reset the board
        try:
            # remove previous main_game boards
            self.gameboard.destroy()
            self.message.destroy()
            self.button_play.destroy()
            self.button_cancel.destroy()
        except Exception:
            pass

        # add the main_game board outline
        self.gameboard = tk.Frame(height=300, width=300, bd=3, relief=tk.RIDGE)
        self.gameboard.pack(padx=20, pady=20)

        # add the labels in the grid
        self.labels = [[0] * 3 for _ in range(3)]
        for r in range(3):
            # set the rowheight
            self.gameboard.rowconfigure(r, minsize=100)
            for c in range(3):
                # set the column width
                self.gameboard.columnconfigure(c, minsize=100)
                # create a label with the correct counter displayed on it
                label = tk.Label(
                    self.gameboard,
                    font=("Courier", 48, "bold"),
                    bd=1,
                    relief=tk.RIDGE,
                    text=self.game.counters[self.game.board[r][c]],
                )
                # expand the label to fit the grid
                label.grid(sticky=tk.E + tk.W + tk.N + tk.S, row=r, column=c)
                # add a click event to the label
                label.bind(
                    "<Button-1>",
                    lambda event, arg={
                        "row": r,
                        "column": c,
                    }: self.on_mouse_down(event, arg),
                )
                # add the label to the graphic list of labels
                self.labels[r][c] = label

        # add the status label
        self.message = tk.Label(text=status)
        self.message.pack(padx=20, fill=tk.X)

        # add the reset button
        self.button_play = tk.Button(self, command=self.reset, text="Reset")
        self.button_play.pack(padx=20, fill=tk.X)

        # add the cancel button
        self.button_cancel = tk.Button(
            self, command=self.cancel, text="Cancel"
        )
        self.button_cancel.pack(padx=20, pady=20, fill=tk.X)

    def update_board(self, r: int, c: int, status: str):
        """replace the counter in the label in position r,c in the grid
        and update the message label to read status"""

        # update label
        self.labels[r][c].config(
            text=self.game.counters[self.game.board[r][c]]
        )
        # update message
        self.message.config(text=status)

    def on_mouse_down(self, _, arg: dict):
        """event handler for clicking the labels"""
        # check whether it is the correct turn
        if self.game.current_player == 1:
            r = arg["row"]
            c = arg["column"]
            # if that is a possible move
            if self.game.board[r][c] == 0:
                # place the new counter, and allow the computer to play
                self.play_game(r, c)

    def reset(self):
        """restarts the main_game"""
        # create a new main_game
        self.game = Game()
        # update display
        self.create_gameboard_widget("Your Turn! Click a square to begin.")

    def play_game(self, r: int, c: int):
        """simulates a main_game play. r and c will refer to the grid
        reference of the label they will have clicked

        r: the row clicked
        c: the column clicked
        """

        # player takes their turn
        self.player_turn(r, c)

        # check for win state
        if not self.win_message(r, c):
            # if player not won, then change the player to player 2
            self.game.current_player = 2
            # update the board
            self.update_board(r, c, "Waiting...")
            # allow the computer to play
            r, c = self.opponent_turn()
            # if computer not won, then change the player to player 1
            if not self.win_message(r, c):
                self.game.current_player = 1
                # update the board
                self.update_board(r, c, "Your turn!")

    def player_turn(self, r: int, c: int):
        """player turn

        r: the row to pick
        c: the column to pick
        """
        # place the counter on the square picked
        self.game.place(self.game.current_player, r, c)

    def opponent_turn(self) -> tuple[int]:
        """computer determines its move, and plays it

        returns: the row and column that the opponent played
        """
        # computer determines the move it is going to make
        r, c = self.game.opponent.choose_move(self.game)
        # place the counter on the square picked
        self.game.place(self.game.current_player, r, c)
        # return the move picked
        return r, c

    def win_message(self, r: int, c: int) -> bool:
        """check for a win, and display appropriate message

        r: the row
        c: the column
        returns: whether the board has been completed or not
        """
        # check if the board is in a finished position
        win_state = self.game.check_for_win()
        if win_state:
            # check for a draw
            if win_state == -1:
                self.update_board(r, c, "Draw! No... not your weapons...")
            # otherwise it is a win
            else:
                self.update_board(
                    r, c, "Player " + str(self.game.current_player) + " wins!"
                )

            return True
        return False

    def cancel(self):
        """stops the whole program"""
        exit()


class TicTacToeWindowIn2D(tk.Tk):
    """class defining the window that the main_game will play in"""

    def __init__(self):
        """initialiser - subclass of Tk"""
        super().__init__()

        # The main title for the window
        self.title("Tic Tac Toe")

        # Reset the board
        self.reset()

    def reset(self):
        """recreate the key pieces of information for the game"""

        # initialise the games
        self.main_game = Game()
        self.games = [[Game() for i in range(3)] for _ in range(3)]

        # determine where the next move must be - -1 indicates any square
        self.nextrow = -1
        self.nextcolumn = -1

        # create a tracker for the last counter placed & the next allowed move
        self.lastlabel = None
        self.nextboard = None

        # initialise an array of labels for the 9 games, each with 9 squares
        grid_labels = [[0 for i in range(3)] for _ in range(3)]
        self.labels = [
            [deepcopy(grid_labels) for i in range(3)] for _ in range(3)
        ]

        # initialise the gameboards
        self.gameboards = [[0] * 3 for _ in range(3)]

        # create the gameboard display
        self.create_gameboard_widget("Player O: Click a square to begin.")

    def create_gameboard_widget(self, status: str):
        """initialise the main_game board graphics

        status: the text to display on the main screen
        """

        # reset the board
        try:
            # remove previous main_game boards if possible
            self.main_gameboard.destroy()
            self.message.destroy()
            self.button_reset.destroy()
            self.button_quit.destroy()
        except Exception:
            pass

        # add the main_game board outline
        self.main_gameboard = tk.Frame(
            height=297, width=297, bd=3, relief=tk.RIDGE
        )
        self.main_gameboard.pack(padx=20, pady=20)

        # loop through each row of the large board
        for game_r in range(3):
            # set the large board rowheight
            self.main_gameboard.rowconfigure(game_r, minsize=99)
            # loop through each column of the large board
            for game_c in range(3):
                # set the large board column width
                self.main_gameboard.columnconfigure(game_c, minsize=99)

                # add the frame for the individual board
                self.gameboards[game_r][game_c] = tk.Frame(
                    self.main_gameboard,
                    height=99,
                    width=99,
                    bd=2,
                    relief=tk.RIDGE,
                )
                # expand the frame to fit the grid
                self.gameboards[game_r][game_c].grid(
                    sticky=tk.E + tk.W + tk.N + tk.S, row=game_r, column=game_c
                )

                # add the labels in the individual board
                for r in range(3):
                    # set the rowheight for the individual board
                    self.gameboards[game_r][game_c].rowconfigure(r, minsize=33)
                    for c in range(3):
                        # set the column width for the individual board
                        self.gameboards[game_r][game_c].columnconfigure(
                            c, minsize=33
                        )
                        # create a label with the correct counter icon
                        # displayed on it
                        label = tk.Label(
                            self.gameboards[game_r][game_c],
                            font=("Courier", 12, "bold"),
                            bd=1,
                            relief=tk.RIDGE,
                            text=self.games[game_r][game_c].counters[
                                self.games[game_r][game_c].board[r][c]
                            ],
                        )
                        # expand the label to fit the grid
                        label.grid(
                            sticky=tk.E + tk.W + tk.N + tk.S, row=r, column=c
                        )
                        # add a click event to the label
                        label.bind(
                            "<Button-1>",
                            lambda event, arg={
                                "row": r,
                                "column": c,
                                "game_row": game_r,
                                "game_column": game_c,
                            }: self.on_mouse_down(event, arg),
                        )
                        # add the label to the graphic list of labels
                        self.labels[game_r][game_c][r][c] = label

        # add the status label
        self.message = tk.Label(text=status)
        self.message.pack(padx=20, fill=tk.X)

        # add the reset button
        self.button_reset = tk.Button(self, command=self.reset, text="Reset")
        self.button_reset.pack(padx=20, fill=tk.X)

        # add the quit button
        self.button_quit = tk.Button(self, command=self.quit, text="Quit")
        self.button_quit.pack(padx=20, pady=20, fill=tk.X)

    def update_board(self, game_r, game_c, r, c, status):
        """replace the counter in the label in position r,c in the grid
        in position game_r, game_c of the main board
        and update the message label to read status"""

        # update label (if it still exists)
        try:
            self.labels[game_r][game_c][r][c].config(
                text=self.games[game_r][game_c].counters[
                    self.games[game_r][game_c].board[r][c]
                ]
            )
        except Exception:
            pass
        # update status message
        self.message.config(text=status)

    def update_main(self, game_r: int, game_c: int, status: str):
        """replaces the gameboard in game_r, game_c with an icon displaying
        which player won that square and updates the message label to read
        status

        game_r: the row of the game to replace
        game_c: the column of the game to replace
        status: the text to display in the message
        """

        # destroy grid of labels currently in that position
        self.gameboards[game_r][game_c].destroy()
        # add label displaying winning counter
        self.gameboards[game_r][game_c] = tk.Label(
            self.main_gameboard,
            font=("Courier", 48, "bold"),
            text=self.main_game.counters[self.main_game.board[game_r][game_c]],
            bd=2,
            relief=tk.RIDGE,
        )
        # expand label to fill grid
        self.gameboards[game_r][game_c].grid(
            sticky=tk.E + tk.W + tk.N + tk.S, row=game_r, column=game_c
        )

        # update message
        self.message.config(text=status)

    def on_mouse_down(self, _, arg: dict):
        """event handler for clicking the labels"""

        # check whether the main game has been completed or not
        if not self.main_game.complete:
            # extract the grid position from the arguments
            game_r = arg["game_row"]
            game_c = arg["game_column"]

            # check if move is in next allowed square
            if self.nextrow == -1 or (
                self.nextrow == game_r and self.nextcolumn == game_c
            ):
                # extract the specific cell clicked by the user
                r = arg["row"]
                c = arg["column"]
                # check if that is a position with a counter in
                if self.games[game_r][game_c].board[r][c] == 0:
                    # place the new counter in position r, c of grid in
                    # game_r, game_c
                    self.play_game(game_r, game_c, r, c)

    def play_game(self, game_r: int, game_c: int, r: int, c: int):
        """simulates a move. r and c will refer to the grid reference of the label
        they will have clicked in the game in grid game_r, game_c

        game_r: the row of the mini game currently being played
        game_c: the column of the mini game currently being played
        r: the row within the mini game to play the move in
        c: the column within the mini game to play the move in
        """

        # change the colour of the previously selected label to black
        # (if possible)
        try:
            self.lastlabel.config(fg="black")
        except Exception:
            pass
        # change the colour of the previously allowed game to white
        # (if possible)
        try:
            self.nextboard.config(bg="white")
        except Exception:
            pass
        # simulate the player move in game game_r, game_c, position r, c
        self.player_turn(game_r, game_c, r, c)
        # update the label last selected
        self.lastlabel = self.labels[game_r][game_c][r][c]
        # change the label that was last selected to green
        self.lastlabel.config(fg="green")

        # check if that specific game has now finished or not
        self.win_message(game_r, game_c, r, c)

        # check if the game in grid position r, c is finished
        if self.games[r][c].complete:
            # if it is, then allow the next player to play any move
            self.nextrow = -1
            self.nextcolumn = -1
        else:
            # if not, then restrict them to play in the game in r, c
            self.nextrow = r
            self.nextcolumn = c

        # check for win of main game
        if not self.win_game(game_r, game_c):
            # if player not won, then change the player number
            self.main_game.current_player = (
                self.main_game.current_player
            ) % 2 + 1

            # update the board
            if self.nextrow == -1:
                # if they are allowed to play anywhere, then let them know
                self.update_board(
                    game_r,
                    game_c,
                    r,
                    c,
                    "Player {0}: Play anywhere!".format(
                        self.main_game.counters[self.main_game.current_player]
                    ),
                )
                # indicate that they could play in the whole grid
                self.nextboard = self.main_gameboard
                # change the background to red of the entire gameboard
                self.nextboard.config(bg="red")
            else:
                # let them know where they need to play
                self.update_board(
                    game_r,
                    game_c,
                    r,
                    c,
                    "Player {0}: Play in square {1}, {2}".format(
                        self.main_game.counters[self.main_game.current_player],
                        self.nextrow + 1,
                        self.nextcolumn + 1,
                    ),
                )
                # indicate which game they have to play
                self.nextboard = self.gameboards[self.nextrow][self.nextcolumn]
                # change the background to red of that game
                self.nextboard.config(bg="red")

    def player_turn(self, game_r: int, game_c: int, r: int, c: int):
        """player turn

        game_r: the row of the mini game currently being played
        game_c: the column of the mini game currently being played
        r: the row within the mini game to play the move in
        c: the column within the mini game to play the move in
        """

        # place the player's counter on grid r, c of game in game_r, game_c
        self.games[game_r][game_c].place(self.main_game.current_player, r, c)

    def win_message(self, game_r: int, game_c: int, r: int, c: int) -> bool:
        """check for a win of a small game, and display appropriate message

        game_r: the row of the mini game currently being played
        game_c: the column of the mini game currently being played
        r: the row within the mini game to play the move in
        c: the column within the mini game to play the move in
        returns: True if the mini game played in game_r, game_c has been
        completed, False otherwise
        """

        # check if the game is in a finished position
        win_state = self.games[game_r][game_c].check_for_win()
        if win_state:
            # check for a draw
            if win_state == -1:
                # update message and board
                self.update_board(game_r, game_c, r, c, "That was a draw...")
                # reset the current board to be empty
                self.games[game_r][game_c] = Game()
                for r in range(3):
                    for c in range(3):
                        self.update_board(
                            game_r, game_c, r, c, "That was a draw..."
                        )

            # otherwise it is a win
            else:
                # update game to show complete
                self.games[game_r][game_c].complete = True
                # update the main game
                self.main_game.board[game_r][
                    game_c
                ] = self.main_game.current_player
                if self.games[self.nextrow][self.nextcolumn].complete:
                    self.nextrow = -1
                    self.nextcolumn = -1
                    self.update_main(game_r, game_c, "Play anywhere")
                else:
                    self.update_main(
                        game_r,
                        game_c,
                        "Play in square {0}, {1}".format(
                            self.nextrow + 1, self.nextcolumn + 1
                        ),
                    )
            return True
        return False

    def win_game(self, game_r: int, game_c: int) -> bool:
        """checks for win of large game following an update in game
        in game_r, game_c

        game_r: the row of the mini-game just finished
        game_c: the column of the mini-game just finished
        returns: True if the main game has completed, False otherwise
        """

        # check if game in finished position
        win_state = self.main_game.check_for_win()
        if win_state:
            # mark game as completed
            self.main_game.complete = True
            # check for draw
            if win_state == -1:
                # update display and display message saying a draw
                self.update_main(game_r, game_c, "It's a draw...")
            # otherwise its a win
            else:
                # update display and display message saying a win
                self.update_main(
                    game_r,
                    game_c,
                    "Player "
                    + str(
                        self.main_game.counters[self.main_game.current_player]
                    )
                    + " won the game!",
                )
            return True
        return False
