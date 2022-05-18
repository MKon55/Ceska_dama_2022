# Hlavní část programu
# Pro pygame => pip install pygame

import pygame

#Importování modulu ze hra
from hra.hodnoty import WIDTH, HEIGHT
from hra.hraci_plocha import Hraci_plocha
from hra.file_manager import File_manager

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry


def main():
    hra = True
    cas_hry = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    plocha = Hraci_plocha()

    print(File_manager().read_file("savegame1"))

    while hra:
        cas_hry.tick(FPS)

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                hra = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pass

        plocha.draw(WINDOW)
        pygame.display.update()  # Pro update hracího pole když hrajeme hru

    pygame.quit()  # ukončení window pro hru


main()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie
#   Něco jako main menu ve hře
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu (převděpodobně na pravé straně okna pygame)
#       Viz Fišerova práce na přednášce
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru (pokusím se implementovat ale mám problém s pochopením)
#   Zároveň uložit kdykoliv partii do .csv souboru (cyklus který vezmu nynější pozici hracích kamenu a toho kdo je na tahu)
#   Specifické pojmenování a rozložení dat musí být spleněno jinak exception!!
#Začátek nové partie již můžeme začít pomocí již daného kodu
