
import pygame
from pygame.locals import *

import copy
import math
import random

import src.TileLogic as TL
import src.settings as sett
import src.character_sprite as character_sprite
import src.character as Char
import src.pathfinder as pf

pygame.init()
pygame.mixer.init()



sett.init()

def logic_tile_init():
    logic_tiles = []
    for i in range(sett.nb_tiles_h):
        logic_tiles.append([])
        for j in range(sett.nb_tiles_w):
            logic_tiles[i].append(TL.TileLogic((i, j)))
    prev_cursor_pos = [0, 0]
    cursor_pos = [0, 0]
    logic_tiles[cursor_pos[0]][cursor_pos[1]].is_cursor = True

    for i in range(int(sett.nb_tiles_h*sett.nb_tiles_w*0.5)):
        rh = random.randint(0, sett.nb_tiles_h-1)
        rw = random.randint(0, sett.nb_tiles_w-1)
        logic_tiles[rh][rw].cost += 1

    for ent in sett.all_entities_list:
        logic_tiles[ent.x][ent.y].is_free = False
        logic_tiles[ent.x][ent.y].is_entity = True
        logic_tiles[ent.x][ent.y].entity = ent

    return logic_tiles, prev_cursor_pos, cursor_pos

def rect_tiles_init(tw, th):
    rect_tiles = []
    for i in range(sett.nb_tiles_h):
        rect_tiles.append([])
        for j in range(sett.nb_tiles_w):
            r = pygame.Rect((j*tw, i*th), (tw, th))
            rect_tiles[i].append(r)
    return rect_tiles

def updateTL():
    for i in range(len(sett.logic_tiles)):
        for j in range(len(sett.logic_tiles[i])):
            sett.logic_tiles[i][j].is_free = True
            sett.logic_tiles[i][j].is_entity = False
    for ent in sett.all_entities_list:
        sett.logic_tiles[ent.x][ent.y].is_free = False
        sett.logic_tiles[ent.x][ent.y].is_entity = True
        sett.logic_tiles[ent.x][ent.y].entity = ent

def clear_path():
    for i in range(len(sett.logic_tiles)):
        for j in range(len(sett.logic_tiles[i])):
            sett.logic_tiles[i][j].is_path_test = False
            sett.logic_tiles[i][j].is_visited = False

def main():

    # cling_effect = pygame.mixer.Sound("./res/sounds/cling1.wav")
    # cling_effect.play()

    pygame.mixer.music.load(sett.main_theme_file)
    pygame.mixer.music.play(-1)


    mainscreen = pygame.display.set_mode((sett.width, sett.height))
    pygame.display.set_caption("FEFP " + sett.version)
    clock = pygame.time.Clock()

    tw, th = int(float(sett.width)/float(sett.nb_tiles_w)), int(float(sett.height)/float(sett.nb_tiles_h))

    main_char_sprite = character_sprite.Character_sprite(sett.im_dict["man1_base"], sett.im_dict["man1_select"], sett.im_dict["man1_attack"], tw, th)
    second_char_sprite = character_sprite.Character_sprite(sett.im_dict["man1_base"], sett.im_dict["man1_select"], sett.im_dict["man1_attack"], tw, th)

    # main_char = Char.Character("Jean", main_char_sprite, 6, 6, True, "Ally")
    # second_char = Char.Character("Marc", second_char_sprite, 10, 10, True, "Ally")

    selected_entity = None

    font_size = int((tw + th) / 4.5)
    font = pygame.font.SysFont('Sans', font_size)
    

    run = True

    #tiles logic init
    prev_cursor_pos = None
    cursor_pos = None
    sett.logic_tiles, prev_cursor_pos, cursor_pos = logic_tile_init()


    #tiles rect init
    rect_tiles = rect_tiles_init(tw, th)

    path = pf.astar([0, 0], [10, 10])

    for i in range(len(path)):
        sett.logic_tiles[path[i].x][path[i].y].is_path_test = True
        col = int(255- i * (255/len(path)))
        sett.logic_tiles[path[i].x][path[i].y].path_color_test = (col, col, col)


    CAN_MOVE = False
    IN_ATTACK_RANGE = False

    while run:
        clock.tick(60)


        if selected_entity != None:
            dist = abs(math.sqrt((selected_entity.x - cursor_pos[0])**2 + (selected_entity.y - cursor_pos[1])**2 ))

            CAN_MOVE = dist <= entity.mouvement and sett.logic_tiles[cursor_pos[0]][cursor_pos[1]].is_free
            IN_ATTACK_RANGE = dist <= 1 and sett.logic_tiles[cursor_pos[0]][cursor_pos[1]].is_entity and sett.logic_tiles[cursor_pos[0]][cursor_pos[1]].entity.name != selected_entity.name

        #USER INPUT
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if selected_entity != None:
                        selected_entity.sprite.animation = selected_entity.sprite.animation_base
                        selected_entity = None
                        for i in range(len(sett.logic_tiles)):
                            for j in range(len(sett.logic_tiles[i])):
                                sett.logic_tiles[i][j].in_range = False
                                sett.logic_tiles[i][j].in_range_but_busy = False
                    else:
                        print("Quit Game")
                        run = not run
                elif event.key == K_UP:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[0] = (cursor_pos[0] - 1) % sett.nb_tiles_h
                elif event.key == K_DOWN:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[0] = (cursor_pos[0] + 1) % sett.nb_tiles_h
                elif event.key == K_LEFT:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[1] = (cursor_pos[1] - 1) % sett.nb_tiles_w
                elif event.key == K_RIGHT:
                    prev_cursor_pos = copy.copy(cursor_pos)
                    cursor_pos[1] = (cursor_pos[1] + 1) % sett.nb_tiles_w
                elif event.key == K_SPACE:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #lmb
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for i in range(len(rect_tiles)):
                        for j in range(len(rect_tiles[i])):
                            if rect_tiles[i][j].collidepoint(pos):
                                prev_cursor_pos = copy.copy(cursor_pos)
                                cursor_pos = [i, j]
                    clear_path()
                    path = pf.astar([0, 0], cursor_pos)
                    for i in range(len(path)):
                        sett.logic_tiles[path[i].x][path[i].y].is_path_test = True
                        col = int(255- i * (255/len(path)))
                        sett.logic_tiles[path[i].x][path[i].y].path_color_test = (col, col, col)

                    if selected_entity == None:
                        foundone = False
                        xc, yc = cursor_pos[0], cursor_pos[1]
                        for entity in sett.all_entities_list:
                            if entity.x == xc and entity.y == yc and entity.selectable:
                                selected_entity = entity
                                foundone = True

                                for i in range(len(sett.logic_tiles)):
                                    for j in range(len(sett.logic_tiles[i])):
                                        d = abs(math.sqrt((selected_entity.x - sett.logic_tiles[i][j].logic_pos[0])**2 + (selected_entity.y - sett.logic_tiles[i][j].logic_pos[1])**2 ))
                                        if d <= selected_entity.mouvement:
                                            if sett.logic_tiles[i][j].is_free:
                                                sett.logic_tiles[i][j].in_range = True
                                            else:
                                                sett.logic_tiles[i][j].in_range_but_busy = True

                        if not foundone:
                            # selected_entity.sprite.animation = selected_entity.sprite.animation_base
                            selected_entity = None
                            for i in range(len(sett.logic_tiles)):
                                for j in range(len(sett.logic_tiles[i])):
                                    sett.logic_tiles[i][j].in_range = False
                                    sett.logic_tiles[i][j].in_range_but_busy = False
                    else:
                        if prev_cursor_pos == cursor_pos:
                            if CAN_MOVE:
                                selected_entity.x = cursor_pos[0]
                                selected_entity.y = cursor_pos[1]
                                selected_entity.sprite.animation = selected_entity.sprite.animation_base
                                selected_entity = None
                                for i in range(len(sett.logic_tiles)):
                                    for j in range(len(sett.logic_tiles[i])):
                                        sett.logic_tiles[i][j].in_range = False
                                        sett.logic_tiles[i][j].in_range_but_busy = False
                            if IN_ATTACK_RANGE:
                                otherEnt = sett.logic_tiles[cursor_pos[0]][cursor_pos[1]].entity
                                selected_entity.attackOther(otherEnt)
                                
                                selected_entity = None
                                for i in range(len(sett.logic_tiles)):
                                    for j in range(len(sett.logic_tiles[i])):
                                        sett.logic_tiles[i][j].in_range = False
                                        sett.logic_tiles[i][j].in_range_but_busy = False
                #lmb
                elif event.button == 3:
                    for i in range(len(rect_tiles)):
                        for j in range(len(rect_tiles[i])):
                            if rect_tiles[i][j].collidepoint(pos):
                                sett.logic_tiles[i][j].cost = float("inf") if sett.logic_tiles[i][j].cost != float("inf") else 1

                    if selected_entity != None:
                        selected_entity.sprite.animation = selected_entity.sprite.animation_base
                        selected_entity = None
                        for i in range(len(sett.logic_tiles)):
                            for j in range(len(sett.logic_tiles[i])):
                                sett.logic_tiles[i][j].in_range = False
                                sett.logic_tiles[i][j].in_range_but_busy = False

        if selected_entity != None:
            selected_entity.sprite.animation = selected_entity.sprite.animation_select

        updateTL()

        #Update cursor
        sett.logic_tiles[prev_cursor_pos[0]][prev_cursor_pos[1]].is_cursor = False
        sett.logic_tiles[cursor_pos[0]][cursor_pos[1]].is_cursor = True

        #Update Sprite
        to_rem = []
        for ent in sett.all_entities_list:
            if ent.is_dead():
                to_rem.append(ent)
        for rm in to_rem:
            rm.kill()
            sett.all_entities_list.remove(rm)

        #DRAWING
        mainscreen.fill(sett.BGcolor)
        
        to_draw_busy = []
        to_draw_range = []
        to_draw_other = []
        for i in range(len(rect_tiles)):
            for j in range(len(rect_tiles[i])):
                if sett.logic_tiles[i][j].is_path_test:
                    to_draw_other.append([rect_tiles[i][j], sett.logic_tiles[i][j].path_color_test, 0])
                if sett.logic_tiles[i][j].is_visited:
                    c = sett.logic_tiles[i][j].iteration_visit * (255/(sett.it_max_astar+1))
                    to_draw_other.append([rect_tiles[i][j], (0, 0, c), 0])
                if sett.logic_tiles[i][j].cost == float("inf"):
                    to_draw_other.append([rect_tiles[i][j], (139,69,19), 0])

                if sett.logic_tiles[i][j].in_range_but_busy:
                    to_draw_busy.append([rect_tiles[i][j], sett.busy_color, 3])
                elif sett.logic_tiles[i][j].in_range:
                    to_draw_range.append([rect_tiles[i][j], sett.mvt_color, 2])
                elif not sett.logic_tiles[i][j].is_cursor:
                    to_draw_other.append([rect_tiles[i][j], sett.tile_color, 1])
                else:
                    to_draw_other.append([rect_tiles[i][j], sett.cursor_color, 1])



        while to_draw_other:
            data = to_draw_other.pop()
            pygame.draw.rect(mainscreen, data[1], data[0], data[2])
        while to_draw_range:
            data = to_draw_range.pop()
            pygame.draw.rect(mainscreen, data[1], data[0], data[2])
        while to_draw_busy:
            data = to_draw_busy.pop()
            pygame.draw.rect(mainscreen, data[1], data[0], data[2])

        for i in range(len(rect_tiles)):
            for j in range(len(rect_tiles[i])):
                display = font.render(str(sett.logic_tiles[i][j].cost), True, (255, 0, 0))
                mainscreen.blit(display, rect_tiles[i][j].center)

        for ent in sett.all_entities_list:
            ent.update()
        sett.all_sprites_list.draw(mainscreen)
        for ent in sett.all_entities_list:
            display = font.render(str(ent.hitpoint), True, (0, 0, 0))
            mainscreen.blit(display, ent.sprite.rect.center)


        if (CAN_MOVE or IN_ATTACK_RANGE) and selected_entity != None:
            color_OK = (0, 255, 0)
            color_KO = (255, 0, 0)
            
            if CAN_MOVE:
                color = color_OK
            if IN_ATTACK_RANGE:
                color = color_KO


            pygame.draw.line(mainscreen, color, selected_entity.sprite.rect.center, rect_tiles[cursor_pos[0]][cursor_pos[1]].center)
                    
            if selected_entity.sprite.rect.center != rect_tiles[cursor_pos[0]][cursor_pos[1]].center:
                arrowsize = (sett.width/sett.nb_tiles_w + sett.height/sett.nb_tiles_h) / 2 / 4

                L1, L2, angle = math.sqrt((rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0] - selected_entity.sprite.rect.center[0])**2 + (rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1] - selected_entity.sprite.rect.center[1])**2), arrowsize, math.pi/6
                x1 = rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0] + (L2/L1) * ( (selected_entity.sprite.rect.center[0] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0])*math.cos(angle) + (selected_entity.sprite.rect.center[1] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1])*math.sin(angle))
                y1 = rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1] + (L2/L1) * ( (selected_entity.sprite.rect.center[1] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1])*math.cos(angle) - (selected_entity.sprite.rect.center[0] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0])*math.sin(angle))

                x2 = rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0] + (L2/L1) * ( (selected_entity.sprite.rect.center[0] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0])*math.cos(angle) - (selected_entity.sprite.rect.center[1] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1])*math.sin(angle))
                y2 = rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1] + (L2/L1) * ( (selected_entity.sprite.rect.center[1] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1])*math.cos(angle) + (selected_entity.sprite.rect.center[0] - rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0])*math.sin(angle))

                #Draw the arrow head
                pygame.draw.polygon(mainscreen, color, ((rect_tiles[cursor_pos[0]][cursor_pos[1]].center[0], rect_tiles[cursor_pos[0]][cursor_pos[1]].center[1]), (x1, y1), (x2, y2)))


        pygame.display.flip()


if __name__ == '__main__':
    main()