# this code is a video game where the user is represented by a white square. The white square is given a limited amount of time to go around the surface and catch other randomly appearing colored squares. The user keeps doing this until they run out of time.

# VERY IMPORTANT: THE MOVING SQUARE THROUGHOUT THIS CODE WILL BE REFERRED TO AS THE "CHAMELEON" AND THE RANDOMLY APPEARING COLORED SQUARES WILL BE REFERRED TO AS THE "FRUIT".(COMMENTS INCLUDED)



import math
import pygame
import random

# pygame RGB(Red,Green,blue) color combinations
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (225, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (254, 226, 62)



pygame.init() # initializing pygame

# setting the amount of space the game window takes up (measured in pixels)
GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT = 900, 500
GAME_SCREEN = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
pygame.display.set_caption("Quick Chameleon")
clock = pygame.time.Clock()

# basic game details
SPEED = 4
FPS = 60
score = 0
time = ((GAME_SCREEN_WIDTH / 2) / (SPEED*FPS)) + 2 # approximately the amount of time needed to get to a possible fruit spawn point depending on the screen width
time_change_rate = 1/FPS   # the amount of time that passes per frame change which eventually adds up to one second

# chameleon details, drawing, and on screen placement
chameleon_color = WHITE
CHAMELEON_WIDTH, CHAMELEON_HEIGHT = 20, 20
CHAMELEON = pygame.Rect(0, 0, CHAMELEON_WIDTH, CHAMELEON_HEIGHT)
CHAMELEON.center = GAME_SCREEN.get_rect().center

# fruit details and on screen placement
fruit_spawn_x = random.randint(0, (GAME_SCREEN_WIDTH - CHAMELEON_WIDTH)) # accounting for the width of the fruit so it isn't printed off the screen
fruit_spawn_y = random.randint(0, (GAME_SCREEN_HEIGHT - CHAMELEON_HEIGHT)) # accounting for the height of the fruit it isn't printed off the screen
FRUIT_WIDTH, FRUIT_HEIGHT = 20, 20



# text details (placement, score, and time)
ALL_FONT = 'gadugi.ttf'

TEXT_SIZE = 32
FONT = pygame.font.SysFont(ALL_FONT, TEXT_SIZE)



#score placement details
SCORE_X, SCORE_Y = 20, 20  # x and y coordinates (assuming it doesn't move)
SCORE_TEXT_COLOR = WHITE
# game time details
TIMER_X, TIMER_Y = (GAME_SCREEN_WIDTH - 50), 20  # x and y coordinates (assuming it doesn't move)
TIMER_TEXT_COLOR = WHITE

# game introduction details
introduction = "Use the arrow keys to move the chameleon. Press the space bar to start the game."

INTRODUCTION_TEXT_SIZE = 25
INTRO_FONT = pygame.font.SysFont(ALL_FONT, INTRODUCTION_TEXT_SIZE)

# game description details
description = "You'll be given some time. When the game starts, quickly find the flickering box and touch it. The faster you do this, the more time you gain."
description_2 = "Try to get as many colored boxes as you can before you run out of time. Good luck!"

DESCRIPTION_TEXT_SIZE = 18
DESC_FONT = pygame.font.SysFont(ALL_FONT, DESCRIPTION_TEXT_SIZE)

# game over text details
GAME_OVER_TEXT_SIZE = round(GAME_SCREEN_WIDTH / 6)
GAME_OVER_FONT = pygame.font.SysFont(ALL_FONT, GAME_OVER_TEXT_SIZE)




# printing the introduction and description of the game before the game starts
not_ready = True
while not_ready:
    ready = pygame.key.get_pressed()
    clock.tick(FPS)
    for event in pygame.event.get():
        if ready[pygame.K_SPACE]:
            not_ready = False



        text_i = INTRO_FONT.render(introduction, True, RED)
        GAME_SCREEN.blit(text_i,  ((GAME_SCREEN_WIDTH / 10), (GAME_SCREEN_HEIGHT / 5)))

        text_d = DESC_FONT.render(description, True, BLUE)
        GAME_SCREEN.blit(text_d,  ((GAME_SCREEN_WIDTH / 17), ((GAME_SCREEN_HEIGHT*4) / 5)))

        text_d_2 = DESC_FONT.render(description_2, True, YELLOW)
        GAME_SCREEN.blit(text_d_2, ((GAME_SCREEN_WIDTH / 5), ((GAME_SCREEN_HEIGHT * 4) / 5) + 15))
        pygame.display.update()






# main body of the game code
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()


    CHAMELEON.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    CHAMELEON.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * SPEED


    # making sure the player doesn't go past the boundary(the given game screen)
    if CHAMELEON.x > GAME_SCREEN_WIDTH:
        CHAMELEON.x -= GAME_SCREEN_WIDTH
    if CHAMELEON.y > GAME_SCREEN_HEIGHT:
        CHAMELEON.y -= GAME_SCREEN_HEIGHT
    if CHAMELEON.x < 0:
        CHAMELEON.x += GAME_SCREEN_WIDTH
    if CHAMELEON.y < 0:
        CHAMELEON.y += GAME_SCREEN_HEIGHT


    time -= time_change_rate

    alternating_fruit_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



    FRUIT = pygame.Rect(fruit_spawn_x, fruit_spawn_y, FRUIT_WIDTH, FRUIT_HEIGHT)


    if time > 0 and CHAMELEON.colliderect(FRUIT):
        fruit_spawn_x = random.randint(0, (GAME_SCREEN_WIDTH - CHAMELEON_WIDTH)) # changing the x axis placement of the fruit after the collision
        fruit_spawn_y = random.randint(0, (GAME_SCREEN_HEIGHT - CHAMELEON_HEIGHT)) # changing the y axis placement of the fruit after the collision

        chameleon_color = alternating_fruit_color # changing the color of the chameleon to the color of the fruit during the time of the collision

        score += 1

        # applying the pythagorean theorem and the physics formula for velocity to determine the minimum amount of time the chameleon needs to get to the next fruit
        a = fruit_spawn_x - CHAMELEON.x
        b = fruit_spawn_y - CHAMELEON.y
        hypotenuse_squared = (a**2) + (b**2)
        c = math.sqrt(hypotenuse_squared)
        time_needed = c / (SPEED*FPS)


        time += ((time_needed * time_change_rate * FPS) + 0.25) # 0.25 seconds added to account for human response time

    elif time < 0:
        TIMER_TEXT_COLOR = BLACK  # timer becomes negative so this line makes it merge with the background

        text_g_o = GAME_OVER_FONT.render("GAME OVER", True, alternating_fruit_color)
        GAME_SCREEN.blit(text_g_o, ((GAME_SCREEN_WIDTH / 5), (GAME_SCREEN_HEIGHT / 3)))


        pygame.display.flip()



    #drawing parts of the game on the game screen
    GAME_SCREEN.fill(BLACK)

    pygame.draw.rect(GAME_SCREEN, alternating_fruit_color, FRUIT)
    pygame.draw.rect(GAME_SCREEN, chameleon_color, CHAMELEON)

    text_s = FONT.render(str(score), True, SCORE_TEXT_COLOR)
    GAME_SCREEN.blit(text_s, (SCORE_X, SCORE_Y))

    text_t = FONT.render(str(round(time)), True, TIMER_TEXT_COLOR)
    GAME_SCREEN.blit(text_t, (TIMER_X, TIMER_Y))

    pygame.display.update()




pygame.quit()

