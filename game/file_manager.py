import csv
import re
from pathlib import Path
from .game_board import Game_board
from .stat_values import ROW, COL, BLACK, WHITE


class File_manager:
    """Reads and Writes to .csv files"""

    @staticmethod
    def read_file(filename):
        base_path = Path(__file__).parent
        file_path = (base_path / f"../{filename}.csv").resolve()

        board = []
        occupied_tiles = []

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                row = list(map(File_manager._remove_spaces, row))  # Remove all spaces
                row = list(map(lambda x: x.lower(), row))  # Make lowercase
                if File_manager.is_empty_row(row):  # Skip empty rows
                    continue
                else:
                    File_manager.check_format(row)  # Check if the correct format was used

                    if row[0] in occupied_tiles:  # tile is already occupied
                        raise FileManagerException(f"Multiple pieces on one tile: \"{row[0]}\"")

                    if not Game_board.is_black_tile(row[0]):  # Piece is on a white tile
                        raise FileManagerException(f"Invalid position: \"{row[0]}\"")

                    board.append(row)
                    occupied_tiles.append(row[0])
        return board

    @staticmethod
    def save_file(board, filename):
        save_string = ""

        for row in board:
            for stone in row:
                if stone == 0:  # Empty square
                    continue
                save_string += File_manager._format_output(stone.row, stone.col, stone.color, stone.queen) + "\n"

        base_path = Path(__file__).parent
        file_path = (base_path / f"../{filename}.csv").resolve()
        with open(file_path, 'w') as file:
            file.write(save_string)
        print(f"Saving to {file_path} as:\n{save_string}")

    @staticmethod
    def _format_output(row, col, color, queen):
        color_symbol = ""
        if color == BLACK:
            color_symbol = "b"
        elif color == WHITE:
            color_symbol = "w"
        return f"{Game_board.coordinates_to_notation(row, col)},{color_symbol if not queen else color_symbol * 2}"

    @staticmethod
    def check_format(row):
        # More than 2 fields
        if len(row) != 2:
            raise FileManagerException(f"Invalid number of fields in a row. (Expected 2, found {len(row)})")

        first_field = re.match("[a-h]{1}[1-8]{1}", row[0])
        second_field = (row[1] == 'b') or (row[1] == 'bb') or (row[1] == 'w') or (row[1] == 'ww')
        if first_field and second_field:
            return
        else:
            raise FileManagerException(f"Invalid format: \"{row}\"")

    @staticmethod
    def is_empty_row(row):  # Empty row or a row containing just an empty string
        return len(row) == 0 or (len(row) == 1 and row[0] == '')

    @staticmethod
    def _remove_spaces(txt):
        return txt.replace(' ', '')


class FileManagerException(Exception):
    pass
