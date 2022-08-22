from screeninfo import get_monitors

WIDTH, HEIGHT = 0, 0
WINDOW_WIDTH, WINDOW_HEIGHT = 0, 0


# Tato metoda nastaví dynamickou velikost plochy
def GetAndSetScreenSize():
    global WIDTH
    global HEIGHT
    global WINDOW_HEIGHT
    global WINDOW_WIDTH
    for m in get_monitors():
        if(m.is_primary is True):
            WIDTH = m.width//2
            HEIGHT = m.width//2
            WINDOW_WIDTH = m.width//2 + m.width//4
            WINDOW_HEIGHT = m.width//2


GetAndSetScreenSize()
