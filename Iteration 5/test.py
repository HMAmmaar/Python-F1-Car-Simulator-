import pygame
from leaderbord_handler import draw_leaderboard_panel, get_player_best_lap
from utils import ORBITRON_FONT_INFO, ORBITRON_FONT

def test_init():
    global PLAYER_TIME, COMPUTER_TIME
    win = pygame.display.get_surface()

    PLAYER_TIME = 23.567
    COMPUTER_TIME = 55.78



def test_loop(events):
    win = pygame.display.get_surface()
    win.fill((20,20,20))
    # pygame.draw.rect(win, (30, 50, 30), pygame.Rect(290, 280, 290, 250))


    win.blit(ORBITRON_FONT.render("You Won!", 1, (200, 200, 200)), (290, 100))

    win.blit(ORBITRON_FONT_INFO.render( "Player" + " Time: " + str(PLAYER_TIME), 1, (200, 200, 200)), (290, 140))
    win.blit(ORBITRON_FONT_INFO.render("Computer Time: " + (str(COMPUTER_TIME) if COMPUTER_TIME is not None else "DNF"), 1, (200, 200, 200)), (290, 165))
    
    TRACK_PB = get_player_best_lap("Track 1", "A")

    win.blit(ORBITRON_FONT_INFO.render("Track PB: "+ str(TRACK_PB), 1, (200, 200, 200)), (290, 190))

    draw_leaderboard_panel(
        win=win,
        panel_rect=pygame.Rect(290, 280, 290, 250),
        track_id=None,
        track_name="Track 1",  # Use the track name directly
        font=ORBITRON_FONT_INFO,
        highlight_username="A",
        limit=10
    )
