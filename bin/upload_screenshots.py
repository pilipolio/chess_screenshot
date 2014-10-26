import os
from chess_screenshot.pieces import Board
screen_shots_path = r'D:\chessboards\boards'

file_path = [os.path.join(screen_shots_path, file_path) for file_path in os.listdir(screen_shots_path) if file_path.endswith('.png')][0]

board = Board.from_filename(file_path)
pgn_game = board.to_pgn_game()