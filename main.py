import pylatex
from pylatex import NoEscape
import chess

class ChessLaTeX:
    def __init__(self, moves):
        self.moves = moves
        self.fen = self.generate_fen()
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
    def generate_fen(self):
        # Create a new game and play moves
        game = chess.Board()
        for move in self.moves:
            try:
                game.push_san(move)
            except ValueError:
                return False
        # Return FEN notation
        return game.fen()

if __name__ == "__main__":
    # Read in games/current_game.csv (which contains one column of moves)
    with open('games/current_game.csv', 'r') as f:
        moves = f.read().splitlines()
    # Create ChessLaTeX object
    chess_latex = ChessLaTeX(moves)
    chess_latex.draw_chessboard()


