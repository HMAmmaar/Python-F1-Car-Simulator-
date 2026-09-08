import pygame

# ========== FONTS ==========
pygame.font.init()
font_path_orbitron = "fonts\Orbitron\static\Orbitron-ExtraBold.ttf"
ORBITRON_FONT = pygame.font.Font(font_path_orbitron, 30)
try:
    ORBITRON_FONT_INFO = pygame.font.Font(font_path_orbitron, 20)
except:
    ORBITRON_FONT_INFO = pygame.font.SysFont("Arial", 20)



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