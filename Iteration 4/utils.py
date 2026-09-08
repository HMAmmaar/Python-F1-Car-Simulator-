import pygame

# ========== FONTS ==========
pygame.font.init()
font_path_orbitron = "fonts\Orbitron\static\Orbitron-ExtraBold.ttf"
ORBITRON_FONT = pygame.font.Font(font_path_orbitron, 30)
try:
    ORBITRON_FONT_INFO = pygame.font.Font(font_path_orbitron, 20)
except:
    ORBITRON_FONT_INFO = pygame.font.SysFont("Arial", 20)

ORBITRON_FONT_TINY = pygame.font.Font(font_path_orbitron, 12)



def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle) # rotates image around top-left hand corner. X and Y coordinates change based on angle
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center) # removes offset by making rectangle with center same as original image
    win.blit(rotated_image, new_rect.topleft) # draws rotated image on window at new top-left coordinates

def blit_info_box(win, area, text, x, y, padding=5, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    if area == "HUD":
        font = ORBITRON_FONT_INFO
    render = font.render(text, True, text_color)
    box = pygame.Rect(x - padding, y - padding, render.get_width() + 2*padding, render.get_height() + 2*padding)
    pygame.draw.rect(win, bg_color, box)
    win.blit(render, (x, y))

def blit_title_center(win, text):
    font = ORBITRON_FONT
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                      40))  # fixed y-coordinate for title

def blit_text_center(win, text):
    font = ORBITRON_FONT
    render = font.render(text, 1, (200, 200, 200))
    
    # 📦 Background box
    box_width = render.get_width() + 20
    box_height = render.get_height() + 20
    box_x = win.get_width() / 2 - box_width / 2
    box_y = win.get_height() / 2 - box_height / 2
    
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height))  # black box
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                      win.get_height()/2 - render.get_height()/2))


def create_button(text, x, y, color=(0, 180, 0), hover_color=None):
    """
    Create a button.
    Returns: (surface, rect) tuple
    """
    if hover_color is None:
        hover_color = tuple(min(c + 40, 255) for c in color)
    
    font = ORBITRON_FONT_INFO
    text_surface = font.render(text, True, (0, 0, 0))
    
    padding = 20
    width = text_surface.get_width() + padding * 2
    height = 30
    
    # Create button surface
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw button background
    pygame.draw.rect(button_surface, color, (0, 0, width, height), border_radius=5)
    
    # Center text
    text_x = (width - text_surface.get_width()) // 2
    text_y = (height - text_surface.get_height()) // 2
    button_surface.blit(text_surface, (text_x, text_y))
    
    # Create rect
    button_rect = pygame.Rect(x, y, width, height)
    
    return button_surface, button_rect

def create_notification(win, text,duration=2000):
    
    colour = (255,255,0)

    font = ORBITRON_FONT_INFO
    render = font.render(text, 1, colour)
    
    # Background box
    box_width = render.get_width() + 20
    box_height = render.get_height() + 20
    box_x = win.get_width() / 2 - box_width / 2
    box_y = 10  # Top of the window
    
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height))  # black box
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                      box_y + 10))
    
    pygame.display.update()
    pygame.time.delay(duration)