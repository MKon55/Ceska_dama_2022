# Hlavní část programu 
# Pro pygame => pip install pygame 

import pygame 

#Importování modulu ze hra
from hra.hodnoty import WIDTH, HEIGHT 
from hra.hraci_plocha import Hraci_plocha

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma") #Název hry

def main():
    hra = True
    cas_hry = pygame.time.Clock() #Ať máme stálou rychlost hry, nemusí být
    plocha = Hraci_plocha()
    
    while hra:
        cas_hry.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Event pro pygame => ukončení hry (button)
                hra = False
                
            if event.type == pygame.MOUSEBUTTONUP: #Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat 
                pass
            
        plocha.draw(WINDOW)        
        pygame.display.update() #Pro update hracího pole když hrajeme hru 
    
    pygame.quit() #ukončení window pro hru
    
main()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie 
#   Něco jako main menu ve hře 
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu 
#       Viz Fišerova práce na přednášce 
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru
#   Zároveň uložit kdykoliv partii do .csv souboru
#Začátek nové partie již můžeme začít pomocí již daného kodu 