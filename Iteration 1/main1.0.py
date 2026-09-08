import pygame
import time
import math

from utlis import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2)
TRACK = scale_image(pygame.image.load("imgs/track-1/track.png"), 0.7)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-1/track-border.png"), 0.7)
TRACK_BORDER_MASK = pygame.mask.from_surface(scale_image(pygame.image.load("imgs/track-1/track-1 border mask.png"), 0.7)) # create the track border mask
FINISH = scale_image(pygame.image.load("imgs/finish.png"),0.75)
FINISH_MASK = pygame.mask.from_surface(FINISH) # create the finish mask

FINISH_POS = (100,135)

RED_CAR = scale_image(pygame.image.load("imgs/cars/red-car.png"), 0.45)
GREEN_CAR = scale_image(pygame.image.load("imgs/cars/green-car.png"), 0.45)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")


class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel 
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05 # value constraint for how quickly car can accelerate


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
    
    def collide(self,mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img) # creates a car mask
        offset = (int(self.x - x), int(self.y - y)) # need integer values fo the offset
        poi = mask.overlap(car_mask, offset)  # overlaps masks to see if thery are collding
        return poi  # return the point of intersection if there is 1


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (117,160)

    def reduce_speed(self): # function to reduce speed when no keys are pressed
        if self.vel >= 0: # if car is moving forward
             self.vel = max(self.vel - self.acceleration/2, 0) # reduce speed by half the acceleration value until it reaches 0
        else: # if car is moving backwards
            self.vel = min(self.vel + self.acceleration/2, 0) # increase speed by half the acceleration value until it reaches 0
        self.move() # car will continue to move at new velocity
    
    def bounce(self):
        self.vel = -self.vel/2 #change velcotiy to other direction and half speed
        self.move() # car will continue to move at new velocity


def draw(win, images, player_car): # now also receives player car
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win) # draws the player car

def move_player(player_car):
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
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (TRACK_BORDER,(0,0))] # list of images to be drawn on the screen
player_car = PlayerCar(3, 3.5) # instantiating the player car passing in max velocity and rotation velocity

while run:
    pygame.display.update() # update the display

    draw(WIN, images, player_car) # draw the images and the player car

    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT: # check if user clicks the X button
            run = False # break the main loop
            break # exit the game
    
    move_player(player_car) # move the player car based on key presses

    if player_car.collide(TRACK_BORDER_MASK)!= None: # check if car collides with track border
        player_car.bounce() # if it does, bounce the car back

    if player_car.collide(FINISH_MASK, *FINISH_POS) != None: # check if car collides with finish line
        print("Finish") # for now just print finish
            
pygame.quit()