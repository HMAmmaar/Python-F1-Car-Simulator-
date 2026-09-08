import pygame
import time
import math
import random

import file_handling

from utils import ORBITRON_FONT_INFO,ORBITRON_FONT, ORBITRON_FONT_TINY, scale_image, blit_rotate_center, blit_info_box, blit_text_center
from track_selection_menu import track_manager
from leaderbord_handler import update_best_lap
from password_logic import load_user_cars


DEBUG = False

GRASS = track_manager.get_current_track().grass

TRACK = track_manager.get_current_track().track

TRACK_BORDER = track_manager.get_current_track().track_border
TRACK_BORDER_MASK = track_manager.get_current_track().track_border_mask
FINISH = track_manager.get_current_track().finish
FINISH_MASK = track_manager.get_current_track().finish_mask

FINISH_POS = track_manager.get_current_track().finish_pos

PLAYER_CAR_START_POS = track_manager.get_current_track().player_start_pos
COMPUTER_CAR_START_POS = track_manager.get_current_track().comp_start_pos

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

WIDTH, HEIGHT = 630,630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WORLD_WIDTH, WORLD_HEIGHT = 1200, 1200  # Big enough for largest track
WORLD = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))

pygame.display.set_caption("Racing Game!")

FPS = 120
PATH = track_manager.get_current_track().path

class Results:
    def __init__(self, track_name, winner):
        from login import username
        self.track_name = track_name
        self.winner = winner
        self.winner_name = username.text if winner == player_car else "Computer"
        self.winner_img = winner.img
        self.player_car_cp_times = player_car.cp_times
        self.computer_car_cp_times = computer_car.cp_times
        self.player_time = round(player_car.finish_time, 3)
        if computer_car.finish_time is not None:
            self.computer_time = round(computer_car.finish_time, 3)
        else:
            self.computer_time = None

def results_handler():

    from login import username

    if player_car.finished:
        if computer_car.finished is not None:
            player_finish_time = player_car.finish_time
            computer_finish_time = computer_car.finish_time
            
            if player_finish_time < computer_finish_time:
                winner = player_car
            elif player_finish_time > computer_finish_time:
                winner = computer_car
            else:
                winner = player_car
        else:
            winner = player_car
    
    print("Winner:", "Player" if winner == player_car else "Computer" if winner == computer_car else "Unknown")

    results_screen_name = str(track_manager.get_current_track().name)+"_results_screen"
    globals()[results_screen_name] = Results(track_manager.get_current_track().name, winner)
    print(f"created results screen instance: {results_screen_name}")
    print(f"Created results screen for track: {track_manager.get_current_track().name}")

    update_best_lap(track_manager.get_current_track().name, username.text, player_finish_time)
    update_best_lap(track_manager.get_current_track().name, "Computer", computer_finish_time)
    

def update_assets():
    global GRASS, TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK, FINISH_POS, PLAYER_CAR_START_POS, COMPUTER_CAR_START_POS, WIDTH, HEIGHT, WIN, WORLD, FPS, PATH, player_car, computer_car, images
    global Game
    # try:
    #     global Game
    #     if sum(player_car.cp_times) > 0:
    #         results_handler()  # Handle results for the completed track
    # except NameError:
    #     pass  # Game not started yet
    # Update track assets
    GRASS = track_manager.get_current_track().grass
    TRACK = track_manager.get_current_track().track
    TRACK_BORDER = track_manager.get_current_track().track_border
    TRACK_BORDER_MASK = track_manager.get_current_track().track_border_mask
    FINISH = track_manager.get_current_track().finish
    FINISH_MASK = track_manager.get_current_track().finish_mask
    FINISH_POS = track_manager.get_current_track().finish_pos
    PLAYER_CAR_START_POS = track_manager.get_current_track().player_start_pos
    COMPUTER_CAR_START_POS = track_manager.get_current_track().comp_start_pos
    PATH = track_manager.get_current_track().path

    print("")

    print(track_manager.get_current_track().name)

    print("Player Start Pos:", PLAYER_CAR_START_POS)
    print("Computer Start Pos:", COMPUTER_CAR_START_POS)

    # Delete old instances
    del player_car, computer_car

    # Create new instances
    player_car = PlayerCar(3, 3.5)
    computer_car = ComputerCar(2.5, 3.5, PATH)
    Game = GameInfo()
    
    # Update images list
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER,(0,0))]
    
    # Clear and redraw world
    WORLD.fill((0, 0, 0))

    from login import username
    PLAYER_CAR_IMG , COMP_CAR_IMG = load_user_cars(username.text)

    player_car.img = PLAYER_CAR_IMG
    computer_car.img = COMP_CAR_IMG

    draw(WORLD, images, player_car, computer_car) # draw the images and the player car and computer car
    zoom(WIN)
    draw_HUD(WIN)
    draw_minimap(WIN)

    pygame.display.update()

    draw_f1_start_lights(WIN)  # draw the F1 start lights




ZOOM = 1.5

def get_camera_position():
    """Calculate camera position with clamping (same as zoom function)"""
    cam_w, cam_h = WIDTH//ZOOM, HEIGHT//ZOOM
    cx = int(player_car.x - cam_w//2)
    cy = int(player_car.y - cam_h//2)

    # Get current track
    current_track = track_manager.get_current_track()
    track_rect = current_track.track.get_rect()
    
    # Clamp camera to track bounds (SAME AS ZOOM FUNCTION)
    cx = max(track_rect.left, min(cx, track_rect.right - cam_w))
    cy = max(track_rect.top, min(cy, track_rect.bottom - cam_h))
    
    return cx, cy, cam_w, cam_h

def zoom(win):
    """Use the shared camera calculation"""
    cx, cy, cam_w, cam_h = get_camera_position()
    
    camera_rect = pygame.Rect(cx, cy, cam_w, cam_h)
    camera_rect.clamp_ip(WORLD.get_rect())
    sub = WORLD.subsurface(camera_rect)
    zoomed = pygame.transform.scale(sub, (WIDTH, HEIGHT))
    win.blit(zoomed, (0,0))

def screen_to_world(screen_x, screen_y):
    """Use the EXACT SAME camera position as zoom function"""
    cx, cy, cam_w, cam_h = get_camera_position()
    
    # Convert screen to world using the clamped camera position
    camera_x = screen_x / ZOOM
    camera_y = screen_y / ZOOM
    world_x = camera_x + cx
    world_y = camera_y + cy
    
    return int(world_x), int(world_y)

class GameInfo:
    def __init__(self, level=1):
        self.level_start_time = time.time()
        self.started = False

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time, 3)

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel 
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = 0.05 # value constraint for how quickly car can accelerate
        self.current_point = 0 # index of the current point in the path the car is moving towards
        self.cp_times = []  # list to store checkpoint times
        self.finished = False  # flag to indicate if the car has finished
        self.finish_time = None  # time when the car finished

    def rotate(self, left=False, right=False):
        if self.vel == 0:
            return  # No turning when stationary

        # Tune these values:
        TURN_EXPONENT = 0.5       # lower = faster increase at low speeds (try 0.5–1)
        MAX_TURN_RATIO = 1        # cap turning to 100% of rotation_vel

        # Non-linear scaling of turn speed
        speed_factor = (abs(self.vel) / self.max_vel) ** TURN_EXPONENT
        speed_factor = min(speed_factor, MAX_TURN_RATIO)

        scaled_rotation = self.rotation_vel * speed_factor

        # Reverse turning logic: flip direction if moving backward
        if self.vel < 0:
            if left:
                self.angle -= scaled_rotation
            elif right:
                self.angle += scaled_rotation
        else:
            if left:
                self.angle += scaled_rotation
            elif right:
                self.angle -= scaled_rotation

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle) # here we then use that image to draw the car
        if DEBUG:
            self.draw_checkpoints(win) # draw checkpoints for debugging

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) # increases velocity by acceleration value until it reaches max velocity
        self.move() # calling self.move() to move the car

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2) # decreases the velocity by acceration value. Speed of car is halved beacuse cars generally travel slower backwards
        self.move() # calling self.move() to move the car

    def move(self):
        radians = math.radians(self.angle) # degree -> radians
        vertical = math.cos(radians) * self.vel # Calulates how much car should mover veritcally
        horizontal = math.sin(radians) * self.vel # Calculates how much car should move horizontally

        self.y -= vertical
        self.x -= horizontal

        try:
            self.update_checkpoint()  # update checkpoint status
        except IndexError:
            pass  # no more checkpoints to update
    
    def collide(self,mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img) # creates a car mask
        offset = (int(self.x - x), int(self.y - y)) # need integer values fo the offset
        poi = mask.overlap(car_mask, offset)  # overlaps masks to see if thery are collding
        return poi  # return the point of intersection if there is 1

    def draw_checkpoints(self, win):
        if DEBUG:
            for point in PATH:
                pygame.draw.circle(win, (255,0,0), point , 5) # draw red circle at each point in path

    def update_checkpoint(self):
        target = PATH[self.current_point] # get the current target point
        rect = pygame.Rect(self.x-60, self.y-20, self.img.get_width()+120, self.img.get_height()+60) # create a rect for the car
        if DEBUG:
            pygame.draw.rect(WORLD, (0,0,255), rect, width=1) # draw the rect for debugging
            pygame.draw.circle(WORLD, (0,255,0), PATH[self.current_point] , 10, width=1) 
        if rect.collidepoint(*target): # if the car is close enough to the target point
            self.current_point += 1 # move to the next point in the path
            self.cp_times.append(Game.get_level_time())  # record the time when the checkpoint is reached
    
    def reduce_speed(self): # function to reduce speed when no keys are pressed
        if self.vel >= 0: # if car is moving forward
             self.vel = max(self.vel - self.acceleration/2, 0) # reduce speed by half the acceleration value until it reaches 0
        else: # if car is moving backwards
            self.vel = min(self.vel + self.acceleration/2, 0) # increase speed by half the acceleration value until it reaches 0
        self.move() # car will continue to move at new velocity

class PlayerCar(AbstractCar):
    IMG = DARK_BLUE_F1_CAR

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel) # call the init method of the AbstractCar class
        self.x, self.y = PLAYER_CAR_START_POS
    
    def bounce(self):
        self.vel = -self.vel/2 #change velcotiy to other direction and half speed
        self.move() # car will continue to move at new velocity
    

class ComputerCar(AbstractCar):
    IMG = DARK_RED_F1_CAR

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel) # call the init method of the AbstractCar class
        self.path = path # list of points the computer car will follow
        self.vel = max_vel # computer car always moves at max velocity
        self.x, self.y = COMPUTER_CAR_START_POS
    
    def draw_points(self, win):
        if DEBUG:
            for point in self.path:
                pygame.draw.circle(win, (255,0,0), point , 5) # draw red circle at each point in path
    
    def draw(self, win):
        super().draw(win) # call the draw method of the AbstractCar class
        if DEBUG:
            self.draw_points(win) # draw the path points
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point] # get the current target point
        x_diff = target_x - self.x # difference in x coordinates
        y_diff = target_y - self.y # difference in y coordinates

        if y_diff == 0: # to avoid division by 0 error
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff) # calculate the angle to the target point

        if target_y > self.y: # if the target point is below the car
            desired_radian_angle += math.pi # adjust the angle

        difference_in_angle = self.angle - math.degrees(desired_radian_angle) # difference between current angle and desired angle

        if difference_in_angle >= 180: # adjust the difference to be within -180 to 180 degrees
            difference_in_angle -= 360
        elif difference_in_angle <= -180:
            difference_in_angle += 360

        if difference_in_angle > 0: # if the car needs to turn right
            self.angle -= min(self.rotation_vel, abs(difference_in_angle)) # turn right by rotation velocity or the remaining angle
        else: # if the car needs to turn left
            self.angle += min(self.rotation_vel, abs(difference_in_angle)) # turn left by rotation velocity or the remaining angle
    
    def update_path_point(self):
        target= self.path[self.current_point] # get the current target point
        rect = pygame.Rect(self.x-60, self.y-20, self.img.get_width()+120, self.img.get_height()+60) # create a rect for the car
        if DEBUG:
            pygame.draw.rect(WORLD, (0,0,255), rect, width=1) # draw the rect for debugging
            pygame.draw.circle(WORLD, (0,255,0), self.path[self.current_point] , 10, width=1) 
        if rect.collidepoint(*target): # if the car is close enough to the target point
            self.current_point += 1 # move to the next point in the path
        
    def adaptive_speed(self):
        gap = get_gap(player_car.cp_times, computer_car.cp_times)[0] # get the current gap

        if gap < -2: # if player is ahead
            self.vel = self.max_vel * 1.5  # speed up to 110% of max velocity
            if DEBUG:
                print(f"Speeding up by 1.5 * self.max_vel, gap: {gap}")
        elif gap > 2: # if player is behind
            self.vel = self.max_vel * 0.5  # slow down to 80% of max velocity
            if DEBUG:
                print(f"Slowing down by 0.5 * self.max_vel, gap: {gap}")
        else:
            self.vel = self.max_vel  # maintain max velocity


    def move(self):
        if self.current_point >= len(self.path): # if car has reached the end of the path
            return
        
        self.calculate_angle() # calculate the angle to the next point
        self.update_path_point() # update the current point if close enough
        self.adaptive_speed() # adjust speed based on gap
        super().move() # call the move method of the AbstractCar class

        if self.current_point == 0:
            self.vel = min(Game.get_level_time()*self.max_vel, self.max_vel) # gradually increase speed after starting

def draw(win, images, player_car,computer_car): # now also receives computer_car
    for img, pos in images:
        win.blit(img, pos)

    
    computer_car.draw(win) # draws the computer car
    player_car.draw(win) # draws the player car

def sector_times():
    total_path_length = len(PATH)
    sector_length = (total_path_length-1) // 3
    try:
        player_sector1_time = player_car.cp_times[sector_length]
    except IndexError:
        player_sector1_time = None
    try:
        player_sector2_time = player_car.cp_times[2 * sector_length] - player_car.cp_times[sector_length]
    except IndexError:
        player_sector2_time = None
    try:
        player_sector3_time = player_car.cp_times[total_path_length-1] - player_car.cp_times[2 * sector_length]
    except IndexError:
        player_sector3_time = None
    
    try:
        computer_sector1_time = computer_car.cp_times[sector_length]
    except IndexError:
        computer_sector1_time = None
    try:
        computer_sector2_time = computer_car.cp_times[2 * sector_length] - computer_car.cp_times[sector_length]
    except IndexError:
        computer_sector2_time = None
    try:
        computer_sector3_time = computer_car.cp_times[total_path_length-1] - computer_car.cp_times[2 * sector_length]
    except IndexError:
        computer_sector3_time = None
    
    if player_sector1_time is not None or computer_sector1_time is not None:
        if player_sector1_time is not None and computer_sector1_time is None:
            sector1_color = (0, 255, 0)  # Green
        elif player_sector1_time is None and computer_sector1_time is not None:
            sector1_color = (255, 0, 0)  # Red
        elif player_sector1_time < computer_sector1_time:
            sector1_color = (0, 255, 0)  # Green
        elif player_sector1_time > computer_sector1_time:
            sector1_color = (255, 0, 0)  # Red
        else:
            sector1_color = (0, 0, 0)  # White for tie
    else:
        sector1_color = (0, 0, 0)  # White

    if player_sector2_time is not None or computer_sector2_time is not None:
        if player_sector2_time is not None and computer_sector2_time is None:
            sector2_color = (0, 255, 0)  # Green
        elif player_sector2_time is None and computer_sector2_time is not None:
            sector2_color = (255, 0, 0)  # Red
        elif player_sector2_time < computer_sector2_time:
            sector2_color = (0, 255, 0)  # Green
        elif player_sector2_time > computer_sector2_time:
            sector2_color = (255, 0, 0)  # Red
        else:
            sector2_color = (0, 0, 0)  # White for tie
    else:
        sector2_color = (0, 0, 0)  # White
    
    if player_sector3_time is not None or computer_sector3_time is not None:
        if player_sector3_time is not None and computer_sector3_time is None:
            sector3_color = (0, 255, 0)  # Green
        elif player_sector3_time is None and computer_sector3_time is not None:
            sector3_color = (255, 0, 0)  # Red
        elif player_sector3_time < computer_sector3_time:
            sector3_color = (0, 255, 0)  # Green
        elif player_sector3_time > computer_sector3_time:
            sector3_color = (255, 0, 0)  # Red
        else:
            sector3_color = (0, 0, 0)  # White for tie
    else:
        sector3_color = (0, 0, 0)  # White
    
    return sector1_color, sector2_color, sector3_color

def get_gap(player_cp_times, computer_cp_times):
    if len(player_cp_times) == 0 and len(computer_cp_times) == 0:
        return 0.0, (255, 255, 255)  # No gap if no checkpoints reached
    
    if len(player_cp_times) == 0:
        gap = computer_cp_times[-1]
        return round(gap,3), (255,0,0)
    
    last_cp_common = min(len(player_cp_times), len(computer_cp_times)) - 1
    gap = player_cp_times[last_cp_common] - computer_cp_times[last_cp_common]

    if len(player_cp_times) > len(computer_cp_times):
        gap =  -(player_cp_times[-1] - player_cp_times[last_cp_common])
    elif len(computer_cp_times) > len(player_cp_times):
        gap = computer_cp_times[-1] - computer_cp_times[last_cp_common]
    
    if gap < 0:
        colour = (0, 255, 0)  # Green for ahead
    elif gap == 0:
        colour = (0, 0, 0)  # White for tied
    else:
        colour = (255, 0, 0)  # Red for behind

    return round(gap, 3), colour

def draw_HUD(win):
    level_time = Game.get_level_time()
    blit_info_box(win, "HUD", f"Time: {level_time} s", 10, win.get_height()-45)
    gap, colour = get_gap(player_car.cp_times, computer_car.cp_times)
    if gap >= 0:
        gap = str("+" + str(gap))
    blit_info_box(win, "HUD", f"Gap: {gap} s", 10, win.get_height()-85, text_color= colour)
    sector1_colour, sector2_colour, sector3_colour = sector_times()
    pygame.draw.rect(win, sector1_colour, (0, win.get_height()-10, win.get_width()//3, 10))
    pygame.draw.rect(win, sector2_colour, (win.get_width()//3, win.get_height()-10, win.get_width()//3, 10))
    pygame.draw.rect(win, sector3_colour, ((win.get_width()//3)*2, win.get_height()-10, win.get_width()//3, 10))

def draw_f1_start_lights(win):
    LIGHT_RADIUS = 20
    SPACING = 15
    TOTAL = 5
    PAD = 10
    BG_COLOR = (20, 20, 20)

    total_w = TOTAL * (2*LIGHT_RADIUS + SPACING) - SPACING
    box_w = total_w + PAD*2
    box_h = 2*LIGHT_RADIUS + PAD*2
    box_x = WIDTH//2 - box_w//2
    box_y = HEIGHT - 80 - PAD - LIGHT_RADIUS
    lights_box = pygame.Rect(box_x, box_y, box_w, box_h)

    pygame.draw.rect(win, BG_COLOR, lights_box, border_radius=12)
    pygame.display.update(lights_box)

    centers = [
        (box_x + PAD + LIGHT_RADIUS + i*(2*LIGHT_RADIUS + SPACING),
         box_y + PAD + LIGHT_RADIUS)
        for i in range(TOTAL)
    ]

    for i in range(TOTAL):
        pygame.draw.circle(win, (255,0,0), centers[i], LIGHT_RADIUS)
        pygame.display.update(lights_box)
        pygame.time.delay(600)


    pygame.time.delay(random.randint(500,1200))


    pygame.draw.rect(win, BG_COLOR, lights_box, border_radius=12)
    go_surf = ORBITRON_FONT.render("GO!", True, (0,255,0))
    go_rect = go_surf.get_rect(center=(WIDTH//2, box_y + box_h//2))
    win.blit(go_surf, go_rect)
    pygame.display.update(lights_box)
    pygame.time.delay(500)

def draw_minimap(win):
    key_height = 30
    
    # Get current track dimensions - CRITICAL: Use track dimensions, not world dimensions
    current_track = track_manager.get_current_track()
    track_width = current_track.track.get_width()
    track_height = current_track.track.get_height()
    
    # Calculate scale factors based on track dimensions
    minimap_scale_x = MINIMAP_WIDTH / track_width
    minimap_scale_y = MINIMAP_HEIGHT / track_height
    
    # Use the smaller scale to maintain aspect ratio
    minimap_scale = min(minimap_scale_x, minimap_scale_y)

    # 1. Semi-transparent background for mini-map
    mini_rect = pygame.Rect(MINIMAP_POS[0], MINIMAP_POS[1], MINIMAP_WIDTH, MINIMAP_HEIGHT)
    transparent_surf = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT), pygame.SRCALPHA)
    transparent_surf.fill((30, 30, 30, 150))  # dark translucent
    win.blit(transparent_surf, MINIMAP_POS)

    # 2. Scaled track image
    # Scale the track to fit in minimap while maintaining aspect ratio
    track_img = current_track.track
    track_aspect = track_width / track_height
    if track_aspect > (MINIMAP_WIDTH / MINIMAP_HEIGHT):
        # Width is limiting factor
        scaled_width = MINIMAP_WIDTH
        scaled_height = int(MINIMAP_WIDTH / track_aspect)
    else:
        # Height is limiting factor
        scaled_height = MINIMAP_HEIGHT
        scaled_width = int(MINIMAP_HEIGHT * track_aspect)
    
    # Center the scaled track in the minimap
    offset_x = (MINIMAP_WIDTH - scaled_width) // 2
    offset_y = (MINIMAP_HEIGHT - scaled_height) // 2
    
    scaled_track = pygame.transform.smoothscale(track_img, (scaled_width, scaled_height))
    win.blit(scaled_track, (MINIMAP_POS[0] + offset_x, MINIMAP_POS[1] + offset_y))

    # 3. Finish line marker - adjust scale for aspect ratio
    fx = MINIMAP_POS[0] + offset_x + (FINISH_POS[0] * minimap_scale)
    fy = MINIMAP_POS[1] + offset_y + (FINISH_POS[1] * minimap_scale)
    finish_rect = pygame.Rect(int(fx), int(fy), int(20 * minimap_scale), int(7 * minimap_scale))
    pygame.draw.rect(win, (255, 255, 255), finish_rect)
    pygame.draw.rect(win, (0, 0, 0), finish_rect, 1)  # Black border

    # 4. Player & computer car dots - use the same scale calculation
    px = MINIMAP_POS[0] + offset_x + (player_car.x * minimap_scale)
    py = MINIMAP_POS[1] + offset_y + (player_car.y * minimap_scale)
    # Check if point is within minimap bounds
    if (MINIMAP_POS[0] <= px <= MINIMAP_POS[0] + MINIMAP_WIDTH and 
        MINIMAP_POS[1] <= py <= MINIMAP_POS[1] + MINIMAP_HEIGHT):
        pygame.draw.circle(win, (0, 0, 255), (int(px), int(py)), 4)  # blue for player

    cx = MINIMAP_POS[0] + offset_x + (computer_car.x * minimap_scale)
    cy = MINIMAP_POS[1] + offset_y + (computer_car.y * minimap_scale)
    if (MINIMAP_POS[0] <= cx <= MINIMAP_POS[0] + MINIMAP_WIDTH and 
        MINIMAP_POS[1] <= cy <= MINIMAP_POS[1] + MINIMAP_HEIGHT):
        pygame.draw.circle(win, (255, 0, 0), (int(cx), int(cy)), 4)  # red for computer

    # 5. Legend/key box below minimap
    key_rect_pos = (MINIMAP_POS[0], MINIMAP_POS[1] + MINIMAP_HEIGHT)
    key_surf = pygame.Surface((MINIMAP_WIDTH, key_height), pygame.SRCALPHA)
    key_surf.fill((30, 30, 30, 150))
    win.blit(key_surf, key_rect_pos)
    pygame.draw.rect(win, (200, 200, 200), (key_rect_pos[0], key_rect_pos[1], MINIMAP_WIDTH, key_height), 1)

    font = ORBITRON_FONT_TINY

    # Player dot + label
    pygame.draw.circle(win, (0, 0, 255), (key_rect_pos[0] + 25, key_rect_pos[1] + key_height // 2), 4)
    player_label = font.render("Player", True, (255, 255, 255))
    win.blit(player_label, (key_rect_pos[0] + 35, key_rect_pos[1] + (key_height // 2) - 8))

    # Computer dot + label
    pygame.draw.circle(win, (255, 0, 0), (key_rect_pos[0] + 90, key_rect_pos[1] + key_height // 2), 4)
    comp_label = font.render("Computer", True, (255, 255, 255))
    win.blit(comp_label, (key_rect_pos[0] + 100, key_rect_pos[1] + (key_height // 2) - 8))

def move_player(player_car):

    if not player_car.finished:
        keys = pygame.key.get_pressed()
        moved = False

        # --- WASD CONTROL SCHEME ---
        if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
            if keys[pygame.K_a]:
                player_car.rotate(left=True)
            if keys[pygame.K_d]:
                player_car.rotate(right=True)
            if keys[pygame.K_w]:
                moved = True
                player_car.move_forward()
            if keys[pygame.K_s]:
                moved = True
                player_car.move_backward()

        # --- ARROW CONTROL SCHEME (only if WASD not used) ---
        elif keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                player_car.rotate(left=True)
            if keys[pygame.K_RIGHT]:
                player_car.rotate(right=True)
            if keys[pygame.K_UP]:
                moved = True
                player_car.move_forward()
            if keys[pygame.K_DOWN]:
                moved = True
                player_car.move_backward()

        # --- NO MOVEMENT ---
        if not moved:
            player_car.reduce_speed()




run = True # main loop
clock = pygame.time.Clock()

images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER,(0,0))] # list of images to be drawn on the screen
player_car = PlayerCar(3, 3.5) # instantiating the player car passing in max velocity and rotation velocity
computer_car = ComputerCar(2.5, 3.5, PATH) # instantiating the computer car

# Game = GameInfo() # instantiating the GameInfo class

def main_game_init():
    
    from login import username
    print(track_manager.get_current_track().name)
    print(track_manager.tracks)

    global ZOOM, MINIMAP_WIDTH, MINIMAP_HEIGHT, MINIMAP_POS
    ZOOM = 1.5
    MINIMAP_WIDTH, MINIMAP_HEIGHT = 200, 150
    MINIMAP_POS = (WIDTH - MINIMAP_WIDTH - 10, 10)

    update_assets()  # update assets for the current track

    PLAYER_CAR_IMG , COMP_CAR_IMG = load_user_cars(username.text)

    player_car.img = PLAYER_CAR_IMG
    computer_car.img = COMP_CAR_IMG

    pygame.display.update()
    
    draw(WORLD, images, player_car, computer_car) # draw the images and the player car and computer car
    zoom(WIN)
    draw_HUD(WIN)
    draw_minimap(WIN)

    pygame.display.update()




def main_game_loop(event_list):
    global images, player_car, computer_car, Game, run, ZOOM
    clock.tick(FPS)

    pygame.display.update() # update the display

    zoom(WIN)
    draw(WORLD, images, player_car, computer_car) # draw the images and the player car and computer car
    draw_HUD(WIN)  # draw the HUD
    draw_minimap(WIN)
    
    Game.started = True  # mark the game as started

    for event in event_list: # event loop
        if DEBUG:
            if event.type == pygame.MOUSEBUTTONDOWN: # on mouse click
                pos = pygame.mouse.get_pos() # get mouse position
                computer_car.path.append(pos) # add position to computer car pathx
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Also check for equals key
                ZOOM = min(3.0, ZOOM + 0.1)  # Use a larger step for visible effect
            elif event.key == pygame.K_MINUS:
                ZOOM = max(0.5, ZOOM - 0.1)  # Use a larger step for visible effect

    move_player(player_car) # move the player car based on key presses
    computer_car.move() # move the computer car along its path

    if player_car.collide(TRACK_BORDER_MASK)!= None: # check if car collides with track border
        player_car.bounce() # if it does, bounce the car back
    
    if computer_car.collide(FINISH_MASK, *FINISH_POS) != None: # check if car collides with finish line
        if computer_car.current_point >= len(PATH)-1: # check if car has passed all checkpoints
            if computer_car.finished == False: # check if car has passed all checkpoints
                computer_car.finish_time = Game.get_level_time()  # record finish time
                computer_car.cp_times.append(Game.get_level_time())  # record finish time
                print("Computer Finished in", Game.get_level_time(), "seconds!") # print finish time
                computer_car.finished = True # mark car as finished
            computer_car.reduce_speed() # reduce speed when finished

    if player_car.collide(FINISH_MASK, *FINISH_POS) != None: # check if car collides with finish line
        if player_car.current_point >= len(PATH)-1: # check if car has passed all checkpoints
            if player_car.finished == False: # check if car has already finished
                player_car.finish_time = Game.get_level_time()  # record finish time
                player_car.cp_times.append(Game.get_level_time())  # record finish time
                print("Player Car finished in", Game.get_level_time(), "seconds!") # print finish time
                player_car.finished = True # mark car as finished
            player_car.reduce_speed() # reduce speed when finished
        else: 
            print("Pls go through all points") # prompt player to go through all checkpoints
            pass

    if player_car.finished:
        if computer_car.finish_time is not None:
            player_finish_time = player_car.finish_time
            computer_finish_time = computer_car.finish_time
            
            if player_finish_time < computer_finish_time:
                blit_text_center(WIN, "Player Wins!")
            elif player_finish_time > computer_finish_time:
                blit_text_center(WIN, "Computer Wins!")
            else:
                blit_text_center(WIN, "Tie!")
        else:
            blit_text_center(WIN, "Player Wins!")
        
        if Game.get_level_time() > player_car.finish_time + 3:
            # file_handling.create_csv("test", player_car.cp_times, computer_car.cp_times)

            if DEBUG:
                print(computer_car.path)   
                print("Player Checkpoint times", player_car.cp_times)  # print the checkpoint times
                print("Computer Checkpoint times:", computer_car.cp_times)  # print the checkpoint times
            
            results_handler()  # Handle results for the completed track

            if track_manager.next_track() is not None:
                update_assets()  # update assets for the new track
                draw(WORLD, images, player_car, computer_car)  # redraw the world with new assets
                images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER,(0,0))] # update images list
                pygame.display.update()
            else:
                results_handler()  # Handle results for the completed track
                print("All tracks completed!")
                return "RESULTS_SCREEN"
