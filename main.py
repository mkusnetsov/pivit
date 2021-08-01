import pygame
import pygame_menu
from pivit.constants import WINWIDTH, WINHEIGHT, GameConfig
from pivit.game import Game

FPS = 60
CONFIG = GameConfig()

pygame.init()
WIN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Pivit')

def starting_menu(win):
    menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Name :', default='John Doe')
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', main)
    menu.add.button('Quit', pygame_menu.events.EXIT)    
    menu.mainloop(win)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN, CONFIG)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.process_mouse_click(pos)

        game.update()
    
    pygame.quit()

def set_difficulty(value, difficulty):
    if difficulty==1:
        CONFIG.set_board_size(8)
    elif difficulty==2:
        CONFIG.set_board_size(6)
    else:
        raise ValueError

starting_menu(WIN)