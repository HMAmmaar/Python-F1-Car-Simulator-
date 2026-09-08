import pygame
import time
import math

import file_handling

from utlis import scale_image, blit_rotate_center, blit_info_box

DEBUG = True

GRASS = scale_image(pygame.image.load("Iteration 2/imgs/grass.jpg"), 2)
TRACK = scale_image(pygame.image.load("Iteration 2/imgs/track-1/track.png"), 0.7)

TRACK_BORDER = scale_image(pygame.image.load("Iteration 2/imgs/track-1/track-border.png"), 0.7)
TRACK_BORDER_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("Iteration 2/imgs/track-1/track-1 border mask.png"), 0.7)) # create the track border mask
FINISH = scale_image(pygame.image.load("Iteration 2/imgs/finish.png"),0.75)
FINISH_MASK = pygame.mask.from_surface(FINISH) # create the finish mask

FINISH_POS = (100,135)

RED_CAR = scale_image(pygame.image.load("Iteration 2/imgs/cars/red-car.png"), 0.45)
GREEN_CAR = scale_image(pygame.image.load("Iteration 2/imgs/cars/green-car.png"), 0.45)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 14000000
PATH = [(134, 92), (96, 61), (51, 90), (46, 346), (56, 368), (224, 552), (269, 571), (309, 554), (319, 426), (358, 382), (434, 385), (461, 432), (473, 542), (524, 568), (571, 545), (570, 322), (540, 290), (352, 290), (318, 244), (350, 207), (529, 204), (576, 172), (574, 88), (536, 61), (248, 66), (218, 100), (220, 276), (182, 322), (134, 272), (133, 91)]


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
        self.x, self.y = self.START_POS
        self.acceleration = 0.05 # value constraint for how quickly car can accelerate
        self.current_point = 0 # index of the current point in the path the car is moving towards
        self.cp_times = []  # list to store checkpoint times
        self.finished = False  # flag to indicate if the car has finished


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
        rect = pygame.Rect(self.x-20, self.y-20, self.img.get_width()+40, self.img.get_height()+40) # create a rect for the car
        if DEBUG:
            pygame.draw.rect(WIN, (0,0,255), rect, width=1) # draw the rect for debugging
            pygame.draw.circle(WIN, (0,255,0), PATH[self.current_point] , 10, width=1) 
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
    IMG = RED_CAR
    START_POS = (117,160)
    
    def bounce(self):
        self.vel = -self.vel/2 #change velcotiy to other direction and half speed
        self.move() # car will continue to move at new velocity
    

class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (142, 160)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel) # call the init method of the AbstractCar class
        self.path = path # list of points the computer car will follow
        self.vel = max_vel # computer car always moves at max velocity
    
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
        rect = pygame.Rect(self.x-20, self.y-20, self.img.get_width()+40, self.img.get_height()+40) # create a rect for the car
        if DEBUG:
            pygame.draw.rect(WIN, (0,0,255), rect, width=1) # draw the rect for debugging
            pygame.draw.circle(WIN, (0,255,0), self.path[self.current_point] , 10, width=1) 
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

Game = GameInfo() # instantiating the GameInfo class


while run:
    clock.tick(FPS)

    pygame.display.update() # update the display

    draw(WIN, images, player_car, computer_car) # draw the images and the player car and computer car
    draw_HUD(WIN)  # draw the HUD
    Game.started = True  # mark the game as started

    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT: # check if user clicks the X button
            run = False # break the main loop
            break # exit the game
        if DEBUG:
            if event.type == pygame.MOUSEBUTTONDOWN: # on mouse click
                pos = pygame.mouse.get_pos() # get mouse position
                computer_car.path.append(pos) # add position to computer car path
    
    move_player(player_car) # move the player car based on key presses
    computer_car.move() # move the computer car along its path

    if player_car.collide(TRACK_BORDER_MASK)!= None: # check if car collides with track border
        player_car.bounce() # if it does, bounce the car back
    
    if computer_car.collide(FINISH_MASK, *FINISH_POS) != None: # check if car collides with finish line
        if computer_car.current_point >= len(PATH)-1: # check if car has passed all checkpoints
            if computer_car.finished == False: # check if car has passed all checkpoints
                computer_car.cp_times.append(Game.get_level_time())  # record finish time
                print("Computer Finished in", Game.get_level_time(), "seconds!") # print finish time
                computer_car.finished = True # mark car as finished
            computer_car.reduce_speed() # reduce speed when finished

    if player_car.collide(FINISH_MASK, *FINISH_POS) != None: # check if car collides with finish line
        if player_car.current_point >= len(PATH)-1: # check if car has passed all checkpoints
            if player_car.finished == False: # check if car has already finished
                player_car.cp_times.append(Game.get_level_time())  # record finish time
                print("Player Car finished in", Game.get_level_time(), "seconds!") # print finish time
                player_car.finished = True # mark car as finished
            player_car.reduce_speed() # reduce speed when finished
        else: 
            print("Pls go through all points") # prompt player to go through all checkpoints
    
    if player_car.finished: # if both cars have finished
        if Game.get_level_time() > player_car.cp_times[-1] + 3:
            file_handling.create_csv(player_car.cp_times, computer_car.cp_times)
            run = False # end the main loop

if DEBUG:
    print(computer_car.path)   
    print("Player Checkpoint times", player_car.cp_times)  # print the checkpoint times
    print("Computer Checkpoint times:", computer_car.cp_times)  # print the checkpoint times


pygame.quit()