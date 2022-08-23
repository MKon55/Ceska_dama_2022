import pygame
import pygame_gui
import json

from game.screen_manager import WINDOW_WIDTH, WINDOW_HEIGHT
from game.stat_values import BACKGROUND, UI_LIGHT, UI_NORMAL, UI_DARK, UI_DARKER, UI_DARKEST
from config.localconfig import PATH
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame.rect import Rect
from pathlib import Path


# Window for picking a file to load
def FilePicker():
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill(BACKGROUND)

    # Run this function if you change any UI colors
    # UpdateJSON()

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), PATH + "gui_theme.json")
    clock = pygame.time.Clock()

    file_selection = OpenUiFileDialog(manager)

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
            try:
                manager.process_events(event)
            except IndexError:  # Fixes game crash related to pygame_gui
                continue

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


# Helping function for FilePicker()
def OpenUiFileDialog(manager):
    base_path = Path(__file__).parent
    save_path = (base_path / "../saves/").resolve()
    file_selection = UIFileDialog(rect=Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), manager=manager, allow_picking_directories=False, window_title="Vybrat uloženou hru", initial_file_path=save_path)
    file_selection.cancel_button.set_text("Zpět")
    file_selection.home_button.tool_tip_text = "Domů"
    file_selection.delete_button.tool_tip_text = "Odstranit"
    file_selection.refresh_button.tool_tip_text = "Aktualizovat"
    file_selection.parent_directory_button.tool_tip_text = "O složku výš"
    return file_selection


def UpdateJSON():
    with open(PATH + "gui_theme.json", "r") as jsonFile:
        data = json.load(jsonFile)

    HEX_UI_LIGHT = "#" + '%02x%02x%02x' % UI_LIGHT
    HEX_UI_NORMAL = "#" + '%02x%02x%02x' % UI_NORMAL
    HEX_UI_DARK = "#" + '%02x%02x%02x' % UI_DARK
    HEX_UI_DARKER = "#" + '%02x%02x%02x' % UI_DARKER
    HEX_UI_DARKEST = "#" + '%02x%02x%02x' % UI_DARKEST

    data["defaults"]["colours"]["normal_bg"] = HEX_UI_DARK
    data["defaults"]["colours"]["hovered_bg"] = HEX_UI_DARKER
    data["defaults"]["colours"]["disabled_bg"] = HEX_UI_DARKER
    data["defaults"]["colours"]["selected_bg"] = HEX_UI_DARKER
    data["defaults"]["colours"]["dark_bg"] = HEX_UI_NORMAL
    data["defaults"]["colours"]["active_bg"] = HEX_UI_DARKER
    data["defaults"]["colours"]["normal_text"] = HEX_UI_DARKER
    data["defaults"]["colours"]["hovered_text"] = HEX_UI_LIGHT
    data["defaults"]["colours"]["selected_text"] = HEX_UI_LIGHT
    data["defaults"]["colours"]["disabled_text"] = HEX_UI_DARKEST
    data["defaults"]["colours"]["active_text"] = HEX_UI_LIGHT
    data["defaults"]["colours"]["normal_border"] = HEX_UI_DARK
    data["defaults"]["colours"]["hovered_border"] = HEX_UI_DARK
    data["defaults"]["colours"]["disabled_border"] = HEX_UI_DARK
    data["defaults"]["colours"]["selected_border"] = HEX_UI_DARK
    data["defaults"]["colours"]["active_border"] = HEX_UI_DARK

    data["#file_dialog.#file_display_list"]["colours"]["normal_bg"] = HEX_UI_DARK
    data["#file_dialog.#file_display_list"]["colours"]["hovered_bg"] = HEX_UI_DARKER
    data["#file_dialog.#file_display_list"]["colours"]["disabled_bg"] = HEX_UI_DARKER
    data["#file_dialog.#file_display_list"]["colours"]["selected_bg"] = HEX_UI_DARKER
    data["#file_dialog.#file_display_list"]["colours"]["dark_bg"] = HEX_UI_NORMAL

    data["selection_list.@selection_list_item"]["colours"]["normal_bg"] = "#323232"  # "#323D45"  # "#21282d"
    data["selection_list.@selection_list_item"]["colours"]["hovered_bg"] = HEX_UI_DARK
    data["selection_list.@selection_list_item"]["colours"]["disabled_bg"] = HEX_UI_DARKER
    data["selection_list.@selection_list_item"]["colours"]["selected_bg"] = HEX_UI_DARK
    data["selection_list.@selection_list_item"]["colours"]["dark_bg"] = HEX_UI_NORMAL
    data["selection_list.@selection_list_item"]["colours"]["active_bg"] = HEX_UI_DARKER
    data["selection_list.@selection_list_item"]["colours"]["normal_text"] = HEX_UI_LIGHT

    with open(PATH + "gui_theme.json", "w") as jsonFile:
        json.dump(data, jsonFile)
