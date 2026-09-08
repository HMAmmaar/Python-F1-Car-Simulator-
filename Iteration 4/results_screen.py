import pygame
import main_game

from utils import ORBITRON_FONT, blit_text_center, blit_title_center, scale_image, create_button, create_notification
from main_game import track_manager, player_car, computer_car, ORBITRON_FONT_INFO, Results
from file_handling import create_csv

# Declare these as module-level variables
result_instance_arr = []
result_instance_pointer = 0
current_track = None

def results_screen_init():
    global result_instance_arr, result_instance_pointer, current_track

    result_instance_arr = []
    result_instance_pointer = 0

    for track in track_manager.tracks:
        results_screen_name = str(track.name) + "_results_screen"

        if hasattr(main_game, results_screen_name):
            result_instance = getattr(main_game, results_screen_name)
            print(f"Found results for {track.name}: Winner = {str(result_instance.winner_name)}, Player Time = {result_instance.player_time}, Computer Time = {result_instance.computer_time}")
            result_instance_arr.append(result_instance)
        else:
            print(f"No results found for {track.name}")
    
    # Since there will always be results, just set current_track to the first one
    current_track = result_instance_arr[result_instance_pointer]
    
    print(f"result_instance_arr: {result_instance_arr}")
    print(f"current_track: {current_track}")

def results_screen_loop(event_list):
    global current_track, result_instance_pointer, result_instance_arr
    
    win = pygame.display.get_surface()
    win.fill((20, 20, 20))  # Dark background for results screen
    
    PLAYER_TIME = current_track.player_time
    COMPUTER_TIME = current_track.computer_time
    CAR_IMAGE = scale_image(current_track.winner_img, 10)

    title = current_track.track_name + " Results"
    blit_title_center(win, title)

    # Arrow navigation buttons at y=40 (same level as title)
    arrow_y = 45
    left_arrow_visible = result_instance_pointer > 0
    right_arrow_visible = result_instance_pointer < len(result_instance_arr) - 1
    
    # Store arrow rects for click detection
    LEFT_ARROW_rect = None
    RIGHT_ARROW_rect = None
    
    # Left arrow (only show if there's a track to the left)
    if left_arrow_visible:
        LEFT_ARROW_surface, LEFT_ARROW_rect = create_button("<", 70, arrow_y, (150, 150, 150))
        win.blit(LEFT_ARROW_surface, (LEFT_ARROW_rect.x, LEFT_ARROW_rect.y))
    
    # Right arrow (only show if there's a track to the right)
    if right_arrow_visible:
        RIGHT_ARROW_surface, RIGHT_ARROW_rect = create_button(">", 500, arrow_y, (150, 150, 150))
        win.blit(RIGHT_ARROW_surface, (RIGHT_ARROW_rect.x, RIGHT_ARROW_rect.y))
    
    # Track counter display
    track_counter_text = f"{result_instance_pointer + 1}/{len(result_instance_arr)}"
    counter_surface = ORBITRON_FONT_INFO.render(track_counter_text, 1, (200, 200, 200))
    win.blit(counter_surface, (win.get_width()/2 - counter_surface.get_width()/2,
                      20))  # fixed y-coordinate for title

    if current_track.winner_name == "Player":
        win.blit(ORBITRON_FONT.render("You Won!", 1, (200, 200, 200)), (290, 100))
    elif current_track.winner_name == "Computer":
        win.blit(ORBITRON_FONT.render("You Lost!", 1, (200, 200, 200)), (290, 100))

    win.blit(ORBITRON_FONT_INFO.render("Player Time: " + str(PLAYER_TIME), 1, (200, 200, 200)), (290, 140))
    win.blit(ORBITRON_FONT_INFO.render("Computer Time: " + (str(COMPUTER_TIME) if COMPUTER_TIME is not None else "DNF"), 1, (200, 200, 200)), (290, 165))
    win.blit(CAR_IMAGE, (40, 100))
    
    pygame.draw.rect(win, (30, 50, 30), pygame.Rect(290, 280, 290, 250))

    CSV_button_surface, CSV_button_rect = create_button("Create CSV", 290, 200, (180, 180, 0))
    win.blit(CSV_button_surface, (CSV_button_rect.x, CSV_button_rect.y))

    REPLAY_button_surface, REPLAY_button_rect = create_button("Create Replay", 290, 240, (180, 180, 0))
    win.blit(REPLAY_button_surface, (REPLAY_button_rect.x, REPLAY_button_rect.y))

    MENU_button_surface, MENU_button_rect = create_button("Back to Menu", 30, 580, (220, 220, 220))
    win.blit(MENU_button_surface, (MENU_button_rect.x, MENU_button_rect.y))

    EXIT_button_surface, EXIT_button_rect = create_button("Exit Game", 450, 580, (0, 0, 180))
    win.blit(EXIT_button_surface, (EXIT_button_rect.x, EXIT_button_rect.y))

    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if Done button was clicked
            if MENU_button_rect.collidepoint(mouse_x, mouse_y):
                for track in track_manager.tracks:
                    results_screen_name = str(track.name) + "_results_screen"
                    if hasattr(main_game, results_screen_name):
                        delattr(main_game, results_screen_name)
                return "TRACK_SELECTION"
            
            if CSV_button_rect.collidepoint(mouse_x, mouse_y):
                create_csv(current_track.track_name, current_track.player_car_cp_times, current_track.computer_car_cp_times)
                create_notification(win,f"{current_track.track_name} CSV File Created")
            
            if EXIT_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                exit()
            
            if REPLAY_button_rect.collidepoint(mouse_x, mouse_y):
                create_notification(win,"Feature will be added soon!")
                pass
            
            # Arrow navigation
            if left_arrow_visible and LEFT_ARROW_rect and LEFT_ARROW_rect.collidepoint(mouse_x, mouse_y):
                result_instance_pointer -= 1
                current_track = result_instance_arr[result_instance_pointer]
            
            if right_arrow_visible and RIGHT_ARROW_rect and RIGHT_ARROW_rect.collidepoint(mouse_x, mouse_y):
                result_instance_pointer += 1
                current_track = result_instance_arr[result_instance_pointer]
    
    return None