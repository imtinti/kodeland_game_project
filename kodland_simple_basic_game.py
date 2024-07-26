import pygame
import sys
import os 

# Set to centralize on window screen where pygame create windows
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 17, 17)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Game states
MAIN_MENU = 'main_menu'
GAME_RUNNING = 'game_running'
PAUSE_MENU = 'pause_menu'
COLISION_DETECTED = 'colision_detected'


game_state = MAIN_MENU
global tries_number

# State captions options
HOME_SCREEN = 'HOME'
GAME_SCREEN = 'GAME'
PAUSE_SCREEN = 'PAUSE'

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WIDTH_GAME, HEIGHT_GAME = 600, 700



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    screen.fill(WHITE)
    draw_text('Main Menu', font, BLACK, screen, 20, 20)
    draw_text('Press ENTER to Start', small_font, BLACK, screen, 20, 100)
    draw_text('Press Q to Quit', small_font, BLACK, screen, 20, 140)

    # Setting caption screen
    pygame.display.set_caption(HOME_SCREEN)

    pygame.display.update()

def pause_menu():
    screen.fill(WHITE)
    draw_text('Pause Menu', font, BLACK, screen, 20, 20)
    draw_text('Press ESC to Resume', small_font, BLACK, screen, 20, 100)
    draw_text('Press M to Main Menu', small_font, BLACK, screen, 20, 140)

    # Setting caption screen
    pygame.display.set_caption(PAUSE_SCREEN)

    pygame.display.update()

def game_loop(player, enemies, tries_number):
    # Screen dimensions
    WIDTH_GAME, HEIGHT_GAME = 600, 700
    screen = pygame.display.set_mode((WIDTH_GAME, HEIGHT_GAME))

    # Setting caption screen
    pygame.display.set_caption(GAME_SCREEN)

    while game_state == GAME_RUNNING:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return PAUSE_MENU

        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        screen.fill(WHITE)

        pygame.draw.rect(screen, RED, player)
        
        for enemy in enemies:
            pygame.draw.rect(screen, BLACK, enemy)
            # Check collision
            if player.colliderect(enemy):
                #player, enemies = init_new_game()
                return COLISION_DETECTED  # Go back to main menu on collision

        # Draw text on the game screen
        draw_text('Press ENTER to PAUSE', small_font, BLACK, screen, 20, 20)
        draw_text('Use arrows to control the red block', small_font, BLACK, screen, 20, 40)
        draw_text(f'Tries number: {tries_number}' , small_font, BLACK, screen, 20, 60)
        

        pygame.display.update()
        clock.tick(60)

    return MAIN_MENU

#WIDTH, HEIGHT = 800, 600
#WIDTH_GAME, HEIGHT_GAME = 600, 700

default_player_position_init =[((WIDTH_GAME/2)-45), HEIGHT_GAME-55, 50, 50]

default_enemie_position_init_one = [200, 150, 50, 50]
default_enemie_position_init_two = [400, 300, 50, 50]

def init_new_game():

    # Initialize player and enemies outside of game_loop to keep their state
    player = pygame.Rect(default_player_position_init)

    enemies = [pygame.Rect(default_enemie_position_init_one), pygame.Rect(default_enemie_position_init_two)]

    tries_number = 0

    return player, enemies, tries_number

def reset_start_position():

    # Initialize player and enemies outside of game_loop to keep their state
    return pygame.Rect(default_player_position_init)


def run_game():

    global game_state


    # Screen home setup
    pygame.display.set_caption(HOME_SCREEN)

    player, enemies, tries_number = init_new_game()

    while True:

        #MAIN MENU
        if game_state == MAIN_MENU:
            main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = GAME_RUNNING
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        #GAME RUNNING
        elif game_state == GAME_RUNNING:
            game_state = game_loop(player, enemies, tries_number)

            if game_state == COLISION_DETECTED: #MEANS THAT HAS OCURRED AN COLLISION
                tries_number = tries_number + 1
                player = reset_start_position() # RESET GAME
                #increase score, decrease life, etc
                

                game_state = GAME_RUNNING # GO BACK TO MAIN MENU STATE
                

        #GAME PAUSED
        elif game_state == PAUSE_MENU:
            pause_menu()
            for event in pygame.event.get():

                #handle button quit click event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #handle enter keydown
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        game_state = GAME_RUNNING

                    if event.key == pygame.K_m:
                        #reset player positions

                        player, enemies, tries_number = init_new_game()
                        
                        #goback to main menu
                        game_state = MAIN_MENU

run_game()
