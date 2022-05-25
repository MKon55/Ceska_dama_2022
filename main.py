# Hlavní část programu
# Pro pygame => pip install pygame

import sys
import pygame
import pygame_menu
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame.rect import Rect

#Importování modulu ze game
from game.stat_values import WIDTH, HEIGHT
from game.game_board import Game_board
from game.file_manager import File_manager

FPS = 60

pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dáma")  # Název hry


def start_players():
    main()


def start_ai():
    main()


def load_game():
    path_to_file = file_picker()
    if path_to_file is None:
        return
    loaded_game = File_manager().read_file(path_to_file)
    main(loaded_game)


def main_menu():  # Main menu (opens first)
    mytheme = pygame_menu.Theme(background_color=(204, 255, 224),
                                title_background_color=(25, 200, 25),
                                title_font_shadow=False,
                                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                                title_font_size=150,
                                title_font_color=(14, 14, 14),
                                title_offset=(WIDTH / 2 - 200, 50),
                                widget_padding=25,
                                title_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
                                widget_font=pygame_menu.font.FONT_OPEN_SANS_LIGHT,
                                selection_color=(15, 200, 15)
                                )

    menu = pygame_menu.Menu('Dáma', WIDTH, HEIGHT, theme=mytheme)

    menu.add.button('Hrát ve dvou', start_players)
    menu.add.button('Hrát proti AI', start_ai)
    menu.add.button('Nahrát hru', load_game)
    menu.add.button('Ukončit', pygame_menu.events.EXIT)

    menu.mainloop(WINDOW)


def file_picker():
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(pygame.Color('#ccffe0'))

    manager = pygame_gui.UIManager((HEIGHT, HEIGHT), "Ceska_dama_2022\\gui_theme.json")
    clock = pygame.time.Clock()

    file_selection = open_ui_file_dialog(manager)

    while 1:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == file_selection.ok_button:
                        return file_selection.current_file_path

                    if event.ui_element == file_selection.cancel_button:
                        return None
            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


def open_ui_file_dialog(manager):
    file_selection = UIFileDialog(rect=Rect(0, 0, WIDTH, HEIGHT), manager=manager, allow_picking_directories=False, window_title="Vybrat uloženou hru")
    file_selection.cancel_button.set_text("Zpět")
    file_selection.home_button.tool_tip_text = "Domů"
    file_selection.delete_button.tool_tip_text = "Odstranit"
    file_selection.refresh_button.tool_tip_text = "Aktualizovat"
    file_selection.parent_directory_button.tool_tip_text = "O složku výš"
    return file_selection


def main(loaded_game=None):  # Main game loop
    game = True
    gaming_time = pygame.time.Clock()  # Ať máme stálou rychlost hry, nemusí být
    board = Game_board()

    if loaded_game is not None:
        board.load_board(loaded_game)

    #File_manager().save_file(board.game_board, "savegame2")

    while game:
        gaming_time.tick(FPS)

        for event in pygame.event.get():
            # Event pro pygame => ukončení hry (button)
            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.MOUSEBUTTONUP:  # Pro klikání myší, zjišťuje na co jsme klikly a co můžeme dělat
                pass

        board.draw(WINDOW)
        pygame.display.update()  # Pro update hracího pole když hrajeme hru

    pygame.quit()  # ukončení window pro hru
    sys.exit()


main_menu()

#vytvoření "předgui" pro načtení ze souboru .csv nebo začátek nové partie
#   Něco jako main menu ve hře
#   Vedle hracího pole ještě počet herních kamenů, počet dám a jaký hráč je na tahu (převděpodobně na pravé straně okna pygame)
#       Viz Fišerova práce na přednášce
#Potřeba tedy vytvořit načtení pozic do hracího pole ze .csv souboru (pokusím se implementovat ale mám problém s pochopením)
#   Zároveň uložit kdykoliv partii do .csv souboru (cyklus který vezmu nynější pozici hracích kamenu a toho kdo je na tahu)
#   Specifické pojmenování a rozložení dat musí být spleněno jinak exception!!
#Začátek nové partie již můžeme začít pomocí již daného kodu
