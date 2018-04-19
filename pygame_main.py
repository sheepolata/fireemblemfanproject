
import pygame
from pygame.locals import *

import copy

import TileLogic
import settings

pygame.init()
settings.init()

def main():

    mainscreen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("FEFP " + settings.version)

    run = True

    #tiles logic init
    logic_tiles = []
    for i in range(settings.nb_tiles_h):
        logic_tiles.append([])
        for j in range(settings.nb_tiles_w):
            logic_tiles[i].append(TileLogic.TileLogic((i, j)))
    prev_cursor_pos = [0, 0]
    cursor_pos = [0, 0]
    logic_tiles[cursor_pos[0]][cursor_pos[1]].is_cursor = True

    #tiles rect init
    rect_tiles = []
    tw, th = int(float(settings.width)/float(settings.nb_tiles_w)), int(float(settings.height)/float(settings.nb_tiles_h))
    for i in range(settings.nb_tiles_h):
        rect_tiles.append([])
        for j in range(settings.nb_tiles_w):
            r = pygame.Rect((j*tw, i*th), (tw, th))
            rect_tiles[i].append(r)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Quit Game")
                    run = not run
                elif event.key == K_UP:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[0] = (cursor_pos[0] - 1) % settings.nb_tiles_h
                elif event.key == K_DOWN:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[0] = (cursor_pos[0] + 1) % settings.nb_tiles_h
                elif event.key == K_LEFT:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[1] = (cursor_pos[1] - 1) % settings.nb_tiles_w
                elif event.key == K_RIGHT:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[1] = (cursor_pos[1] + 1) % settings.nb_tiles_w
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #lmb
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for i in range(len(rect_tiles)):
                        for j in range(len(rect_tiles[i])):
                            if rect_tiles[i][j].collidepoint(pos):
                                logic_tiles[i][j].is_selected = not logic_tiles[i][j].is_selected


        logic_tiles[prev_cursor_pos[0]][prev_cursor_pos[1]].is_cursor = False
        logic_tiles[cursor_pos[0]][cursor_pos[1]].is_cursor = True

        mainscreen.fill(settings.BGcolor)
        for i in range(len(rect_tiles)):
            for j in range(len(rect_tiles[i])):
                if logic_tiles[i][j].is_cursor:
                    pygame.draw.rect(mainscreen, settings.cursor_color, rect_tiles[i][j], 1)
                else:
                    pygame.draw.rect(mainscreen, settings.tile_color, rect_tiles[i][j], 1)

        pygame.display.flip()


if __name__ == '__main__':
    main()