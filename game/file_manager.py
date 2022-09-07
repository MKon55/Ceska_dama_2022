import csv
import re
from pathlib import Path
from .game_board import GameBoard
from .game_movement import Gameing
from .stat_values import WHITE, BLACK, WHITE_CHAR, BLACK_CHAR, WHITE_QUEEN_CHAR, BLACK_QUEEN_CHAR, DEFAULT_COLOR_TURN, WHITE_TURN_CHAR, BLACK_TURN_CHAR
from .piece_queen import PieceQueen


class FileManager:
    """Reads and Writes to .csv files"""

    @staticmethod
    def ReadFile(path_to_file):
        file_path = path_to_file.resolve()

        board = []
        turn = DEFAULT_COLOR_TURN
        occupied_tiles = []

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            firstRow = True
            for row in csv_reader:
                # Check if the first row has info about who's turn it is. If not, assume WHITE turn
                if firstRow:
                    if FileManager.IsRowAboutPlayerTurn(row):  # First row has info about who's turn it is
                        turn = FileManager.GetTurnColorFromText(row[0])
                        continue
                    firstRow = False
                row = list(map(FileManager._RemoveSpaces, row))  # Remove all spaces
                row = list(map(lambda x: x.lower(), row))  # Make lowercase
                if FileManager.IsEmptyRow(row):  # Skip empty rows
                    continue
                else:
                    FileManager.CheckFormat(row)  # Check if the correct format was used

                    if row[0] in occupied_tiles:  # tile is already occupied
                        raise FileManagerException(f"Multiple pieces on one tile: \"{row[0]}\"")

                    if not GameBoard.IsBlackTile(row[0]):  # Piece is on a white tile
                        raise FileManagerException(f"Invalid position: \"{row[0]}\"")

                    board.append(row)
                    occupied_tiles.append(row[0])
        return board, turn

    @staticmethod
    def SaveFile(board, filename):
        save_string = ""

        # Who's turn is it
        save_string += WHITE_CHAR if Gameing.turn == WHITE else BLACK_CHAR
        save_string += "\n"

        for row in board:
            for stone in row:
                if stone == 0:  # Empty square
                    continue
                isQueen = isinstance(stone, PieceQueen)
                save_string += FileManager._FormatOutput(stone.row, stone.col, stone.color, isQueen) + "\n"

        base_path = Path(__file__).parent
        file_path = (base_path / f"../saves/{filename}.csv").resolve()
        # Check if the saves folder exists
        if not file_path.exists():
            folder_path = (base_path / "../saves").resolve()
            folder_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(save_string)
        # print(f"Saving to {file_path}")

    @staticmethod
    def _FormatOutput(row, col, color, queen):
        color_symbol = ""
        if color == BLACK:
            color_symbol = BLACK_CHAR
        elif color == WHITE:
            color_symbol = WHITE_CHAR
        return f"{GameBoard.CoordinatesToNotation(row, col)},{color_symbol if not queen else color_symbol * 2}"

    @staticmethod
    def CheckFormat(row):
        # More than 2 fields
        if len(row) != 2:
            raise FileManagerException(f"Invalid number of fields in a row. (Expected 2, found {len(row)})")

        first_field = re.match("[a-h]{1}[1-8]{1}", row[0])
        second_field = (row[1] == WHITE_CHAR) or (row[1] == WHITE_QUEEN_CHAR) or (row[1] == BLACK_CHAR) or (row[1] == BLACK_QUEEN_CHAR)
        if first_field and second_field:
            return
        else:
            raise FileManagerException(f"Invalid format: \"{row}\"")

    @staticmethod
    def IsRowAboutPlayerTurn(row):
        # Check if the row is about who's turn it is
        if len(row) == 1:
            return row[0] == WHITE_TURN_CHAR or row[0] == BLACK_TURN_CHAR

    @staticmethod
    def GetTurnColorFromText(text):
        if text == WHITE_TURN_CHAR:
            return WHITE
        if text == BLACK_TURN_CHAR:
            return BLACK
        else:
            return DEFAULT_COLOR_TURN

    @staticmethod
    def IsEmptyRow(row):  # Empty row or a row containing just an empty string
        return len(row) == 0 or (len(row) == 1 and row[0] == '')

    @staticmethod
    def _RemoveSpaces(txt):
        return txt.replace(' ', '')


class FileManagerException(Exception):
    pass
