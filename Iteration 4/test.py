import pygame

def test_init():
    global win
    win = pygame.display.get_surface()


def test_loop(events):
    pygame.draw.rect(win, (30, 50, 30), pygame.Rect(290, 280, 290, 250))
