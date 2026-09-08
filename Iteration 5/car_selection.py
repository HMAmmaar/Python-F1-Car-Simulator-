import pygame
from utils import scale_image, create_button, blit_title_center, ORBITRON_FONT_INFO

player_car_pointer = 0
computer_car_pointer = 0

PREVIEW_SCALE = 2

def car_selection_init():
    global win, cars, PREVIEW_SCALE, player_car_pointer, computer_car_pointer
    win = pygame.display.get_surface()

    RED_CAR = scale_image(pygame.image.load("imgs/cars/red-car.png"), 0.45)
    GREEN_CAR = scale_image(pygame.image.load("imgs/cars/green-car.png"), 0.45)
    GREY_CAR = scale_image(pygame.image.load("imgs/cars/grey-car.png"), 0.45)
    PURPLE_CAR = scale_image(pygame.image.load("imgs/cars/purple-car.png"), 0.45)
    WHITE_CAR = scale_image(pygame.image.load("imgs/cars/white-car.png"), 0.45)
    RED_F1_CAR = scale_image(pygame.image.load("imgs/cars/RED_F1_CAR.png"), 0.06)
    ORANGE_F1_CAR = scale_image(pygame.image.load("imgs/cars/ORANGE_F1_CAR.png"), 0.06)
    CYAN_F1_CAR = scale_image(pygame.image.load("imgs/cars/CYAN_F1_CAR.png"), 0.06)
    DARK_RED_F1_CAR = scale_image(pygame.image.load("imgs/cars/DARK_RED_F1_CAR.png"), 0.06)
    DARK_BLUE_F1_CAR = scale_image(pygame.image.load("imgs/cars/DARK_BLUE_F1_CAR.png"), 0.06)
    YELLOW_F1_CAR = scale_image(pygame.image.load("imgs/cars/YELLOW_F1_CAR.png"), 0.06)
    PINK_F1_CAR = scale_image(pygame.image.load("imgs/cars/PINK_F1_CAR.png"), 0.06)
    GREY_F1_CAR = scale_image(pygame.image.load("imgs/cars/GREY_F1_CAR.png"), 0.06)

    cars = [
        ("Red F1", RED_F1_CAR), ("Orange F1", ORANGE_F1_CAR),
        ("Cyan F1", CYAN_F1_CAR), ("Dark Red F1", DARK_RED_F1_CAR),
        ("Dark Blue F1", DARK_BLUE_F1_CAR), ("Yellow F1", YELLOW_F1_CAR),
        ("Pink F1", PINK_F1_CAR), ("Grey F1", GREY_F1_CAR),
        ("Classic Red", RED_CAR), ("Classic Green", GREEN_CAR),
        ("Classic Grey", GREY_CAR), ("Classic Purple", PURPLE_CAR),
        ("Classic White", WHITE_CAR)
    ]

def car_selection_loop(events_list):
    global player_car_pointer, computer_car_pointer
    win.fill((20,20,20))

    blit_title_center(win,"Car Selection Menu")

    car_image = cars[player_car_pointer][1]
    win.blit(scale_image(car_image, 9), (95,120))

    
    render = ORBITRON_FONT_INFO.render("Player Car", 1, (200, 200, 200))
    win.blit(render, (120,520))

    LEFT_ARROW_PLAYER_surface, LEFT_ARROW_PLAYER_rect = create_button("<", 40, 315, (150, 150, 150))
    win.blit(LEFT_ARROW_PLAYER_surface, (LEFT_ARROW_PLAYER_rect.x, LEFT_ARROW_PLAYER_rect.y))
    
    RIGHT_ARROW_PLAYER_surface, RIGHT_ARROW_PLAYER_rect = create_button(">", 260, 315, (150, 150, 150))
    win.blit(RIGHT_ARROW_PLAYER_surface, (RIGHT_ARROW_PLAYER_rect.x, RIGHT_ARROW_PLAYER_rect.y))

    LEFT_ARROW_COMP_surface, LEFT_ARROW_COMP_rect = create_button("<", 330, 315, (150, 150, 150))
    win.blit(LEFT_ARROW_COMP_surface, (LEFT_ARROW_COMP_rect.x, LEFT_ARROW_COMP_rect.y))
    
    RIGHT_ARROW_COMP_surface, RIGHT_ARROW_COMP_rect = create_button(">", 540, 315, (150, 150, 150))
    win.blit(RIGHT_ARROW_COMP_surface, (RIGHT_ARROW_COMP_rect.x, RIGHT_ARROW_COMP_rect.y))


    for event in events_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if LEFT_ARROW_PLAYER_rect.collidepoint(mouse_x, mouse_y):
                print("LEFT_ARROW_PLAYER clicked")
                player_car_pointer -= 1
            elif RIGHT_ARROW_PLAYER_rect.collidepoint(mouse_x, mouse_y):
                print("RIGHT_ARROW_PLAYER clicked")
                player_car_pointer += 1
            elif LEFT_ARROW_COMP_rect.collidepoint(mouse_x, mouse_y):
                print("LEFT_ARROW_COMP clicked")
            elif RIGHT_ARROW_COMP_rect.collidepoint(mouse_x, mouse_y):
                print("RIGHT_ARROW_COMP clicked")