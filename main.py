import pygame
import pygame_menu
from pivit.constants import WINWIDTH, WINHEIGHT, GameConfig
from pivit.game import Game

FPS = 60
CONFIG = GameConfig()
GAME = None

pygame.init()
WINDOW = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Pivit')

def make_starting_menu():
    menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :', default='John Doe')
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_game, menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)    
    return menu

def start_game(menu):
    global GAME
    menu.disable()
    WINDOW.fill((0,0,0))
    GAME = Game(WINDOW, CONFIG)
    GAME.update()

def main():
    run = True
    clock = pygame.time.Clock()
    menu = make_starting_menu()

    while run:
        clock.tick(FPS)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if menu.is_enabled():
                menu.update(events)
                if menu.is_enabled(): # The menu is still active, i.e. the game has not started
                    menu.draw(WINDOW)
                    pygame.display.update()
                continue
        
            # menu is not enabled
            if GAME is not None:
                if GAME.game_is_over():
                    print(GAME.game_status_message())
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    GAME.process_mouse_click(pos)
                    GAME.update()
    
    pygame.quit()

def set_difficulty(value, difficulty):
    if difficulty==1:
        CONFIG.set_board_size(8)
    elif difficulty==2:
        CONFIG.set_board_size(6)
    else:
        raise ValueError

main()