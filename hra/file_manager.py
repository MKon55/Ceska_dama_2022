import csv
import re
from pathlib import Path
from .hraci_plocha import Hraci_plocha


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

                    if not Hraci_plocha.is_black_tile(row[0]):  # Piece is on a white tile
                        raise FileManagerException(f"Invalid position: \"{row[0]}\"")

                    board.append(row)
                    occupied_tiles.append(row[0])
        return board

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
