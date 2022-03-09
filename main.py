import random

import pylatex
from pylatex import NoEscape
import chess
import sys

class ChessLaTeX:
    def __init__(self, moves):
        self.moves = moves
        self.game = self.get_game()
        self.fen = self.game.fen()
        self.is_valid = self.fen is not False

    def draw_chessboard(self):
        # Create document and use package chessboard
        doc = pylatex.Document()
        doc.packages.append(pylatex.Package('skak'))
        doc.packages.append(pylatex.Package('chessboard'))
        doc.append(pylatex.Command('setchessboard', NoEscape(r'showmover=false')))
        doc.append(pylatex.Command('newgame'))
        # Place chess pieces
        doc.append(pylatex.Command('fenboard', NoEscape(self.fen)))
        doc.append(pylatex.Command('chessboard'))
        # Save tex file
        doc.generate_tex()
        doc.generate_pdf('chessboard_display', compiler='pdflatex')

    # Generate FEN notation from list of moves
    def get_game(self):
        # Create a new game and play moves
        game = chess.Board()
        for move in self.moves:
            try:
                game.push_san(move)
            except ValueError:
                return False
        # Return FEN notation
        return game

    # Get list of valid moves, and choose a random one, save to the csv file
    def make_random_move(self):
        # Get the list of valid moves from this game
        # Convert generator to list
        legal_moves = self.game.legal_moves
        # Choose a random move from the list
        move = random.choice(list(legal_moves))
        # Save the move to the csv file
        with open('games/current_game.csv', 'a') as f:
            f.write(f"\n{move}")


if __name__ == "__main__":
    # Read in games/current_game.csv (which contains one column of moves)
    # Get argument from command line
    # If argument is 'move' then generate a random move
    # If argument is 'generate' then draw the chessboard
    with open('games/current_game.csv', 'r') as f:
        moves = f.read().splitlines()
    chess_latex = ChessLaTeX(moves)
    choice = sys.argv[1]
    if choice == 'move':
        chess_latex.make_random_move()
    else:
        chess_latex.draw_chessboard()


