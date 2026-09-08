import pygame
from utils import blit_title_center, scale_image, create_notification,create_button, ORBITRON_FONT_INFO

# Load your images at the module level
try:
    CAR_SELECTION_IMAGE = scale_image(pygame.image.load("imgs/cars/ORANGE_F1_CAR.png").convert_alpha(), 0.4)
except:
    print("Could not load car selection image")
    CAR_SELECTION_IMAGE = pygame.Surface((200, 350))  # Fallback surface
    CAR_SELECTION_IMAGE.fill((100, 100, 200))

try:
    GAME_IMAGE = scale_image(pygame.image.load("imgs/finish_flag.png").convert_alpha(), 0.4)
except:
    print("Could not load game image")
    GAME_IMAGE = pygame.Surface((200, 350))  # Fallback surface
    GAME_IMAGE.fill((200, 100, 100))

def intro_menu_init():
    # Nothing to do here since images are already loaded
    pass

def intro_menu_loop(event_list):
    win = pygame.display.get_surface()
    win.fill((20, 20, 20))
    blit_title_center(win, "Welcome to the Car Racing Game!")
    
    left_button = pygame.Rect(330, 120, 260, 450)
    right_button = pygame.Rect(40, 120, 260, 450)
    
    # Draw button backgrounds directly on window
    pygame.draw.rect(win, (40, 20, 60), left_button, border_radius=10)
    pygame.draw.rect(win, (200, 100, 50), right_button, border_radius=10)
    
    # Add images to buttons (position them inside button rectangles)
    if CAR_SELECTION_IMAGE:
        # Center image horizontally, position near top of button
        img_x = left_button.centerx - CAR_SELECTION_IMAGE.get_width() // 2
        img_y = left_button.y + 60  # 50px from top
        win.blit(CAR_SELECTION_IMAGE, (img_x, img_y))
    
    if GAME_IMAGE:
        img_x = right_button.centerx - GAME_IMAGE.get_width() // 2
        img_y = right_button.y + 135  # 120px from top
        win.blit(GAME_IMAGE, (img_x, img_y))
    
    # Add text to buttons
    font = ORBITRON_FONT_INFO
    left_text = font.render("Car Selection Menu", True, (255, 255, 255))
    # Position text near bottom of button
    left_text_rect = left_text.get_rect(centerx=left_button.centerx, bottom=left_button.bottom - 20)
    win.blit(left_text, left_text_rect)
    
    right_text = font.render("Main Game", True, (255, 255, 255))
    right_text_rect = right_text.get_rect(centerx=right_button.centerx, bottom=right_button.bottom - 20)
    win.blit(right_text, right_text_rect)

    EXIT_button_surface, EXIT_button_rect = create_button("Exit Game", 450, 580, (0, 0, 180))
    win.blit(EXIT_button_surface, (EXIT_button_rect.x, EXIT_button_rect.y))

    LOGOUT_button_surface, LOGOUT_button_rect = create_button("Log out", 30, 580, (220, 220, 220))
    win.blit(LOGOUT_button_surface, (LOGOUT_button_rect.x, LOGOUT_button_rect.y))
    

    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_x, mouse_y = event.pos

            if left_button.collidepoint(mouse_x,mouse_y):
                create_notification(win,"Feature will be added soon!")
                # return "CAR_SELECTION"  # Move to car selection menu
            elif right_button.collidepoint(mouse_x,mouse_y):
                return "TRACK_SELECTION"  # Start the game
            elif LOGOUT_button_rect.collidepoint(mouse_x, mouse_y):
                return "LOGIN"
            elif EXIT_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                exit()