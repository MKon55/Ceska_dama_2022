import pygame
import pygame_gui

from game.screen_manager import WIDTH, HEIGHT
from config.localconfig import PATH
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame.rect import Rect


# Window for picking a file to load
def FilePicker():
    window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(pygame.Color('#ccffe0'))

    manager = pygame_gui.UIManager((HEIGHT, HEIGHT), PATH + "gui_theme.json")
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
            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()


# Helping function for FilePicker()
def OpenUiFileDialog(manager):
    file_selection = UIFileDialog(rect=Rect(0, 0, WIDTH, HEIGHT), manager=manager, allow_picking_directories=False, window_title="Vybrat uloženou hru")
    file_selection.cancel_button.set_text("Zpět")
    file_selection.home_button.tool_tip_text = "Domů"
    file_selection.delete_button.tool_tip_text = "Odstranit"
    file_selection.refresh_button.tool_tip_text = "Aktualizovat"
    file_selection.parent_directory_button.tool_tip_text = "O složku výš"
    return file_selection
