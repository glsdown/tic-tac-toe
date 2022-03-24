import tkinter as tk

from helpers import Game, check_for_win


class selectionWindow(tk.Tk):
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
        win_state = check_for_win(self.game.board)
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


def main():
    """main code to create main_game window"""

    window = selectionWindow()
    window.mainloop()


if __name__ == "__main__":
    main()
