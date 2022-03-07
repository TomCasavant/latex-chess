import pylatex
from pylatex import NoEscape
import chess

class ChessLaTeX:
    def __init__(self, moves):
        self.moves = moves
        self.fen = self.generate_fen()

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
            game.push_san(move)
        # Return FEN notation
        return game.fen()


if __name__ == "__main__":
    # Example moves 1.e4 c5 2.Nf3
    chess_latex = ChessLaTeX(["e4", "c5", "Nf3"])
    # First move is 1.e4
    chess_latex.draw_chessboard()


