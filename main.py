# libraries used
import pygame
import os


# environment python 3.9
# initializing the pygame
pygame.init()

# determining the height and width of the pygame window
WIN_HEIGHT = 500
WIN_WIDTH = 900
# width argument is passed first
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("KUNALs First Game!!")
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40


# FONT
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)


# color variable with rgb values
white = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT + 2


# framerate for the while loop to display the game
FPS = 60
VEL = 5  # velocity of the spaceship
# arguments passed here are X coordiante position , y coordinate position , width of the rect , height of the rectangle
BORDER = pygame.Rect(WIN_WIDTH/2 - 5, 0, 10, WIN_HEIGHT)
MAX_BULLETS = 3
BULLET_VELOCITY = 8

# loading the image of ship
# os.path.join = for every other os it will connect the path of the mentioned folders automatically like windows used frwrd slash and mac used bckwrd slash
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACE_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # here 90 is the degree of rotation
RED_SPACE_SHIP = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACE_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIN_WIDTH, WIN_HEIGHT))


# DRAW FUNCTION
# blit is used to import an outside image at custom location and fill is used to fill a colour
# function for drawing or creating stuffs on the pygame board
def draw_window(yellow, red, yellow_bullets, red_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE, (0, 0))  # arguemnts passed image with x,y coordinates
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    yellow_health_text = HEALTH_FONT.render(
        "Health:" + str(yellow_health), 1, white)
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, white)
    WINDOW.blit(yellow_health_text, (5, 10))
    WINDOW.blit(red_health_text, (WIN_WIDTH -
                red_health_text.get_width() - 10, 5))
    # error here faced filled the screen after drawing the border which overlapped
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullets in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullets)
    for bullets in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullets)

    pygame.display.update()


# winner function
def DeclareWinner(winner_text):
    declare = WINNER_FONT.render(winner_text, 1, white)
    WINDOW.blit(declare, (WIN_WIDTH/2 - declare.get_width() /
                2, WIN_HEIGHT/2 - declare.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# yellow_handling_function


def yellow_handling_func(key_pressed, yellow):

    # keypressed functionality

    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    # RIGHT  #yellow.width is a property
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width + 15 < BORDER.x:
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < WIN_HEIGHT:  # DOWN
        yellow.y += VEL


def red_handling_func(key_pressed, red):

    ####  BULLET AND SPACESHIP MOVEMENT LOGIC   ####

    # here the coordinates will only minus with -VEL when the required key is pressed just like the bullet_handling function it will also be continuosly be called
    # while the while loop is running but will not execute the -VEL until the required key is pressed whereas in the case of bundle_handling
    # no if condition is there hence -bulletvelocity continuosly changes the coordinates.

    # red moving functionality
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    # RIGHT +15 to move further to the right
    if key_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIN_WIDTH + 15:
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 15 < WIN_HEIGHT:  # DOWN
        red.y += VEL


def bullet_handling(yellow_bullets, red_bullets, yellow, red):

    # for loop here moves the bullet continously as while loop will keep running
    # and it will keep calling the bullet_handling function and which will keep subtracting the bullet.x coordinating for every
    # bullet present in the list thus will keep the bullet moving.
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
    
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIN_WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# MAIN FUNCTION

# function to run the main pygame window.
# clock used to determine framerate of the window similar to sleep in js


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    run = True
    clock = pygame.time.Clock()
    yellow_bullets = []  # empty list of the bullets
    red_bullets = []
    yellow_health = 10
    red_health = 10

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:

                    yellow_bullet = pygame.Rect(
                        yellow.x + yellow.width - 10, yellow.y + yellow.height/2 + 5, 10, 5)
                    yellow_bullets.append(yellow_bullet)

                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS:

                    red_bullet = pygame.Rect(
                        red.x - 18, red.y + red.height//2 + 5, 10, 5)
                    red_bullets.append(red_bullet)
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
            winner_text = ""
        if yellow_health == 0:
            winner_text = "Red Wins!"
        if red_health == 0:
            winner_text = "Yellow Wins!"

        if winner_text != "":
            DeclareWinner(winner_text)
            break  # now it will break the while loop and will exit the game

        draw_window(yellow, red, yellow_bullets,
                    red_bullets, red_health, yellow_health)
        key_pressed = pygame.key.get_pressed()
        yellow_handling_func(key_pressed, yellow)
        red_handling_func(key_pressed, red)
        bullet_handling(yellow_bullets, red_bullets,  yellow, red)

        # print(red_bullets , yellow_bullets)
    main()


# will only run the main function if the file name is main
if __name__ == "__main__":
    main()
