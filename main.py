import os
import random

import pylatex
from pylatex import NoEscape
from pdf2image import convert_from_path
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
        # Convert pdf to png and add to README.md specify output name as chessboard.png
        images = convert_from_path('chessboard_display.pdf')
        for image in images:
            # Crop the image to just show the chessboard
            image = image.crop(box=(467, 400, 912, 847))
            image.save('chessboard.png', 'PNG')


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
            # if game is empty, just write the move otherwise add newline
            if os.stat('games/current_game.csv').st_size == 0:
                f.write(f"{move}")
            else:
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
        if chess_latex.game.is_game_over():
            # Move current_game.csv to game{number}.csv
            # Create new current_game.csv
            # Generate a new game
            # Save the new game to current_game.csv
            src = 'games/current_game.csv'
            # Seach games/ for the most recent number
            # If there are no games, then number = 1
            # If there are games, then number = the most recent number + 1
            number = 1
            for file in os.listdir('games/'):
                if file.startswith('game'):
                    number = int(file[4:]) + 1
            dst = f'games/game{number}.csv'
            os.rename(src, dst)
            with open('games/current_game.csv', 'w') as f:
                f.write('')
            chess_latex = ChessLaTeX([])
        chess_latex.make_random_move()
    else:
        chess_latex.draw_chessboard()


