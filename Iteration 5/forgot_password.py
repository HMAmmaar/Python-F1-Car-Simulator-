import pygame
from utils import ORBITRON_FONT, ORBITRON_FONT_INFO, blit_title_center, create_button, TextBox
from password_logic import reset_password

def create_notification_forgot_password(win, text,duration=2000):
    
    colour = (255,255,0)

    font = ORBITRON_FONT_INFO
    render = font.render(text, 1, colour)
    
    # Background box
    box_width = render.get_width() + 20
    box_height = render.get_height() + 20
    box_x = win.get_width() / 2 - box_width / 2
    box_y = 450  # Top of the window
    
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height))  # black box
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                      box_y + 10))
    
    username.draw(win)
    password_new.draw(win)

    pygame.display.update()
    pygame.time.delay(duration)

def forgot_password_init():
    global win, username, password_new
    win = pygame.display.get_surface()
    win.fill((20, 20, 20))
    pygame.display.set_caption("Login Menu")

    from login import username
    print(f"Obtained Username '{username.text}' from login.py")

    # SECURITY_Q = obtain_security_question(username.text)
    print(f"Obtained Security Question for user {username.text}")


    username = TextBox(195, 190, ORBITRON_FONT, is_password=False)
    password_new = TextBox(195, 300, ORBITRON_FONT, is_password=True)
    

def forgot_password_loop(events_list):
    win.fill((20,20,20))



    blit_title_center(win, "Forgot Password")

    username_surf = ORBITRON_FONT.render("Username:", True, (200, 200, 200))
    password_new_surf = ORBITRON_FONT.render("Password:", True, (200, 200, 200))

    center_x = win.get_width() // 2

    username_rect = username_surf.get_rect(center=(center_x, 160))
    password_new_rect = password_new_surf.get_rect(center=(center_x, 270))

    pygame.draw.rect(win, (20, 20, 50), pygame.Rect(165, 120, 300, 300), border_radius=15)

    win.blit(username_surf, username_rect)
    win.blit(password_new_surf, password_new_rect)


    SUBMIT_surface, SUBMIT_rect= create_button("Submit", 250, 470)
    win.blit(SUBMIT_surface, (SUBMIT_rect.x, SUBMIT_rect.y))

    BACK_button_surface, BACK_button_rect = create_button("Back to Login", 30, 580, (220, 220, 220))
    win.blit(BACK_button_surface, (BACK_button_rect.x, BACK_button_rect.y))

    EXIT_button_surface, EXIT_button_rect = create_button("Exit Game", 450, 580, (0, 0, 180))
    win.blit(EXIT_button_surface, (EXIT_button_rect.x, EXIT_button_rect.y))

    for event in events_list:       
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if SUBMIT_rect.collidepoint(mouse_x, mouse_y):
                print("Submit button pressed")
                x = reset_password(username.text, password_new.text)
                if x == "password reset successful":
                    create_notification_forgot_password(win, "Password Resest Successful")
                elif x == "no such user":
                    create_notification_forgot_password(win, "Password Reset")
                    return "INTRO_MENU"

            if BACK_button_rect.collidepoint(mouse_x, mouse_y):
                return "LOGIN"
            
            if EXIT_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                exit()

        username.handle_event(event)
        password_new.handle_event(event)

    password_new.draw(win)
    username.draw(win)