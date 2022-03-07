# Use pytest to check if move is valid

# Import main.py from above directory
import sys

sys.path.append('')

# Import main.py from above directory
from main import ChessLaTeX


# Test if move is valid
def test_valid_move():
    # Read in games/current_game.csv (which contains one column of moves)
    with open('games/current_game.csv', 'r') as f:
        moves = f.read().splitlines()
    # Create ChessLaTeX object
    chess_latex = ChessLaTeX(moves)
    assert chess_latex.is_valid
