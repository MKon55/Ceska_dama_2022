# Informace pro hrací kámen ktety bude improtován do hracího plochy

from abc import ABC, abstractmethod
from .stat_values import SQUARE_SIZE


class GamePiece(ABC):
    PADDING = 20  # určení velikosti hracího kamene ve prostoru

    # Constructor
    @abstractmethod
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.pos = (row, col)
        self.color = color
        self.selected = False
        self.x = 0  # x pro col
        self.y = 0  # y pro row
        self.CalcPos()

    # Create an instance from an existing piece (Used for queen promotion)
    @classmethod
    def fromPiece(cls, piece):
        return cls(piece.row, piece.col, piece.color)

    # Metoda co určí pozici ve hracím čtverci pro vytvoření hracího kamene
    #   Prostředek našeho místa pro hrací kámen, pro jeho správné vykreslení (Prostředek čtverce)
    def CalcPos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # Metoda pro pohyb hracího kamene
    def Move(self, row, col):
        self.row = row
        self.col = col
        self.pos = (row, col)
        self.CalcPos()  # Přepočítání aby byl kámen přesunut na prostředek čtverce

    # Metoda vykreslí hrací kámen
    @abstractmethod
    def Draw(self, win):
        pass


#Potřeba stále implementovat pohyb hracího kamene (White hráč vždycky začíná jako první pokud není načteno ze partie v .csv)
#   (Done) Implementace buď ve hrací_kamenu nebo hraci_plocha nebo vlastí specifcký soubor na pohyb
#   Jak pro hráče tak pro AI
#   Binární strom pro rozhodávání správného pohybu
#   (Done) Po stisknutí hracího kamene se zobrazí body na hrací ploše zelené barvy kam se můžeme přesunout
#       Jinou možnost nám to nedá
