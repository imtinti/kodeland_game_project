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
GREEN = (17, 255, 129)
BLUE = (0, 0, 255)

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


def draw_text_two(text, font, color, surface, center_x, center_y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(center_x, center_y))
    surface.blit(textobj, textrect)
    

def main_menu():


    screen.fill(WHITE)

    draw_text_two('Main Menu', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
    draw_text_two('Press ENTER to Start', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
    draw_text_two('Press Q to Quit', small_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 40)


    # Setting caption screen
    pygame.display.set_caption(HOME_SCREEN)

    pygame.display.update()

def pause_menu():

    screen.fill(WHITE)


    draw_text_two('Pause Menu', font, BLACK, screen, WIDTH_GAME // 2, ((HEIGHT_GAME // 8) + 40))
    draw_text_two('Press ESC to Resume', small_font, BLACK, screen, WIDTH_GAME // 2, HEIGHT_GAME // 2)
    draw_text_two('Press M to Main Menu', small_font, BLACK, screen, WIDTH_GAME // 2, HEIGHT_GAME // 2 + 20)

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


        draw_text_two('Press ENTER to PAUSE', small_font, BLACK, screen, WIDTH_GAME // 2, 20)
        draw_text_two('Use arrows to control the red block', small_font, BLACK, screen, WIDTH_GAME // 2, 40)
        draw_text_two('Don not touch the black blocks!', small_font, BLACK, screen, WIDTH_GAME // 2, 60)


        draw_text_two(f'Tries number: {tries_number}' , small_font, BLACK, screen, WIDTH_GAME // 6, HEIGHT_GAME//2)

        # Draw start line
        pygame.draw.line(screen, GREEN, (0, 100), (WIDTH_GAME, 100), 5)
        draw_text('FINISH', small_font, GREEN, screen, 10, 80)

        # Draw finish line
        pygame.draw.line(screen, BLUE, (0, HEIGHT_GAME - 100), (WIDTH_GAME, HEIGHT_GAME - 100), 5)
        draw_text('START', small_font, BLUE, screen, 10, HEIGHT_GAME - 95)

        

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

                    if event.key == pygame.K_m: #user choose to goback to initial menu
                        #set screen size
                        pygame.display.set_mode((WIDTH, HEIGHT))
                        #reset player positions
                        player, enemies, tries_number = init_new_game()
                        
                        #goback to main menu
                        game_state = MAIN_MENU

run_game()
