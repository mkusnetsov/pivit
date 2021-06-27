import pygame
from pivit.constants import WINWIDTH, WINHEIGHT
from pivit.game import Game

FPS = 60

pygame.init()
WIN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
pygame.display.set_caption('Pivit')

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

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

main()