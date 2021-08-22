import pygame
import pygame_menu
from pivit.constants import WINWIDTH, WINHEIGHT, GameConfig
from pivit.game import Game

FPS = 60
CONFIG = GameConfig()
GAME = None

pygame.init()
WIN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Pivit')

# def starting_menu(win):
#     menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
#     menu.add.text_input('Name :', default='John Doe')
#     menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
#     menu.add.button('Play', main)
#     menu.add.button('Quit', pygame_menu.events.EXIT)    
#     menu.mainloop(win)

def make_starting_menu():
    menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :', default='John Doe')
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_game, menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)    
    return menu

def start_game(menu):
    global GAME
    GAME = Game(WIN, CONFIG)
    menu.disable()

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
                menu.draw(WIN)
                pygame.display.update()
            
            elif GAME is not None:
                if GAME.winner() != None:
                    print(GAME.winner())
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
# starting_menu(WIN)