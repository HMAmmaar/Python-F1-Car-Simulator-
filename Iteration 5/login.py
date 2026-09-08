import pygame
from utils import ORBITRON_FONT, ORBITRON_FONT_INFO, blit_title_center, create_button, TextBox
from password_logic import validate_credentials
import pygame
import re

def create_notification_login(win, text,duration=2000):
    
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
    password.draw(win)

    pygame.display.update()
    pygame.time.delay(duration)

def is_secure_password(password):
    """
    Check if password contains:
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one special character
    - Minimum length (optional, commonly 8)
    """
    if len(password) < 8:
        return False
    
    patterns = [
        r'\d',           # digit
        r'[A-Z]',        # uppercase
        r'[a-z]',        # lowercase
        r'[!@#$%^&*(),.?":{}|<>_]'  # special characters
    ]
    
    return all(re.search(pattern, password) for pattern in patterns)

def username_length(username):
    if len(username) > 8:
        return "too long"
    elif len(username) < 3:
        return "too short"
    else:
        return True

def login_init():
    global win, username,password,email
    win = pygame.display.get_surface()
    win.fill((20, 20, 20))
    pygame.display.set_caption("Login Menu")

    username = TextBox(195, 190, ORBITRON_FONT, is_password=False)
    password = TextBox(195, 300, ORBITRON_FONT, is_password=True)



def login_loop(events_list):
    win.fill((20, 20, 20))   # clear screen

    blit_title_center(win,"Login Page")

    username_surf = ORBITRON_FONT.render("Username:", True, (200, 200, 200))
    password_surf = ORBITRON_FONT.render("Password:", True, (200, 200, 200))

    center_x = win.get_width() // 2

    username_rect = username_surf.get_rect(center=(center_x, 160))
    password_rect = password_surf.get_rect(center=(center_x, 270))

    pygame.draw.rect(win, (20, 20, 50), pygame.Rect(165, 120, 300, 300), border_radius=15)

    win.blit(username_surf, username_rect)
    win.blit(password_surf, password_rect)

    SUBMIT_surface, SUBMIT_rect= create_button("Submit", 320, 370)
    win.blit(SUBMIT_surface, (SUBMIT_rect.x, SUBMIT_rect.y))

    SIGNUP_surface, SIGNUP_rect= create_button("Signup", 195, 370)
    win.blit(SIGNUP_surface, (SIGNUP_rect.x, SIGNUP_rect.y))

    EXIT_button_surface, EXIT_button_rect = create_button("Exit Game", 450, 580, (0, 0, 180))
    win.blit(EXIT_button_surface, (EXIT_button_rect.x, EXIT_button_rect.y))

    FORGOTPASS_button_surface, FORGOTPASS_button_rect = create_button("Forgot Password", 30, 580, (220, 220, 220))
    win.blit(FORGOTPASS_button_surface, (FORGOTPASS_button_rect.x, FORGOTPASS_button_rect.y))

    for event in events_list:       
        if event.type == pygame.MOUSEBUTTONDOWN:
            CURRENT_USER = username.text
            CURRENT_PASSWORD = password.text
            mouse_x, mouse_y = event.pos
            if SIGNUP_rect.collidepoint(mouse_x, mouse_y):
                print("Signup button pressed")
                if username.text == "" or password.text == "":
                    create_notification_login(win,'Create username and password for signup')
                else:
                    if validate_credentials(username.text, password.text) == True:
                        create_notification_login(win,"User already exists")
                    else:
                        if is_secure_password(password.text) == False:
                            create_notification_login(win, "Password aint secure enough")
                        else:
                            x = username_length(username.text)
                            if x == "too long":
                                create_notification_login(win, "Username is too long")
                            elif x == "too short":
                                create_notification_login(win, "Username too short")
                            elif x == True:
                                return "SIGN_UP"
                            else:
                                print("SIGN UP ERROR: username_length()")
                
            if SUBMIT_rect.collidepoint(mouse_x, mouse_y):
                print("Submit button pressed")
                if validate_credentials(username.text, password.text) == True:
                    print(f"{username.text} logged in")
                    create_notification_login(win, f"{username.text} logged in")
                    return "INTRO_MENU"
                else:
                    create_notification_login(win,"Login Failed")
                    print("Login Failed")
            if FORGOTPASS_button_rect.collidepoint(mouse_x, mouse_y):
                if username.text == "":
                    create_notification_login(win,'Enter username then click forgot password')
                else:
                    if validate_credentials(username.text, "placeholder") == "no such user":
                        create_notification_login(win,'Username does not exist')
                    else:
                        print("Forgot Password")
                        return "FORGOT_PASSWORD"
            if EXIT_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                exit()

        username.handle_event(event)
        password.handle_event(event)

    username.draw(win)
    password.draw(win)
