from screeninfo import get_monitors

WIDTH, HEIGHT = 0, 0


# Tato metoda nastaví dynamickou velikost plochy
def GetAndSetScreenSize():
    global HEIGHT
    global WIDTH
    for m in get_monitors():
        if(m.is_primary == True):
            WIDTH = m.width//2
            HEIGHT = WIDTH


GetAndSetScreenSize()
