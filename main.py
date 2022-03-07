import pylatex
from pylatex import NoEscape


class Chess:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position

    def draw_chessboard(self):
        # Create document and use package chessboard
        doc = pylatex.Document()
        doc.packages.append(pylatex.Package('skak'))
        doc.packages.append(pylatex.Package('chessboard'))
        doc.append(pylatex.Command('setchessboard', NoEscape(r'showmover=false')))
        doc.append(pylatex.Command('newgame'))
        doc.append(pylatex.Command('chessboard'))

        doc.generate_pdf('chessboard_display', compiler='pdflatex')



if __name__ == "__main__":
    chess = Chess("test", "black", "a1")
    chess.draw_chessboard()


