# Hlavní část programu 
# Pro pygame => pip install pygame (docker to má automaticky)

import pygame 

#Importování modulu ze hodnot
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