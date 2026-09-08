import pygame
from main_game import main_game_init, main_game_loop
from track_selection_menu import track_selection_init, track_selection_loop
from results_screen import results_screen_init, results_screen_loop
from intro_menu import intro_menu_init, intro_menu_loop



game_state = "INTRO_MENU"  # Example game state

run = True # main loop
clock = pygame.time.Clock()

init_dict = {
    "MAIN_GAME": False,
    "RESULTS_SCREEN": False,
    "TRACK_SELECTION": False,
    "INTRO_MENU": False
}

while run:

    for state in init_dict:
        if game_state != state:
            init_dict[state] = False

    event_list = pygame.event.get()
    for event in event_list: # event loop
        if event.type == pygame.QUIT: # check if user clicks the X button
            run = False # break the main loop
            break # exit the game
    
    if game_state == "MAIN_GAME":
        if init_dict["MAIN_GAME"] == False:
            main_game_init()
            init_dict["MAIN_GAME"] = True
        result = main_game_loop(event_list)
        if result != None:
            game_state = result
    
    if game_state == "TRACK_SELECTION":
        if init_dict["TRACK_SELECTION"] == False:
            track_selection_init()
            init_dict["TRACK_SELECTION"] = True
        result = track_selection_loop(event_list)
        if result != None:
            game_state = result
    
    if game_state == "RESULTS_SCREEN":
        if init_dict["RESULTS_SCREEN"] == False:
            results_screen_init()
            init_dict["RESULTS_SCREEN"] = True
        result = results_screen_loop(event_list)
        if result != None:
            game_state = result

    if game_state == "INTRO_MENU":
        if init_dict["INTRO_MENU"] == False:
            intro_menu_init()
            init_dict["INTRO_MENU"] = True
        result = intro_menu_loop(event_list)
        if result != None:
            game_state = result

    
    pygame.display.update()





pygame.quit()