import pygame

def init():
    global version
    version = "0.1a"

    global width
    width = 800

    global height 
    height = 600

    global nb_tiles_w    
    nb_tiles_w = 25

    global nb_tiles_h
    nb_tiles_h = 25

    global all_entities_list
    all_entities_list = []

    global all_sprites_list
    all_sprites_list = pygame.sprite.Group()

    global logic_tiles
    logic_tiles = []

    global BGcolor
    BGcolor = (34,139,34)

    global tile_color
    tile_color = (0, 0, 0)

    global cursor_color
    cursor_color = (255, 255, 255)

    global mvt_color
    mvt_color = (0, 0, 255)

    global busy_color
    busy_color = (255, 0, 0)

    global it_max_astar
    it_max_astar = 0

    global main_theme_file
    main_theme_file = "./res/musics/main_theme_FE.mp3"

    global im_dict
    im_dict = {}
    im_dict["man1_base"] = []
    im_dict["man1_base"].append(pygame.image.load("./res/man1_base/man1_1.png"))
    im_dict["man1_base"].append(pygame.image.load("./res/man1_base/man1_2.png"))
    im_dict["man1_base"].append(pygame.image.load("./res/man1_base/man1_3.png"))
    im_dict["man1_base"].append(pygame.image.load("./res/man1_base/man1_2.png"))
    
    im_dict["man1_select"] = []
    im_dict["man1_select"].append(pygame.image.load("./res/man1_select/man1_1.png"))
    im_dict["man1_select"].append(pygame.image.load("./res/man1_select/man1_2.png"))
    im_dict["man1_select"].append(pygame.image.load("./res/man1_select/man1_1.png"))
    im_dict["man1_select"].append(pygame.image.load("./res/man1_select/man1_3.png"))

    im_dict["man1_attack"] = []
    im_dict["man1_attack"].append(pygame.image.load("./res/man1_attack/man1_1.png"))
    im_dict["man1_attack"].append(pygame.image.load("./res/man1_attack/man1_2.png"))
    im_dict["man1_attack"].append(pygame.image.load("./res/man1_attack/man1_3.png"))
    im_dict["man1_attack"].append(pygame.image.load("./res/man1_attack/man1_2.png"))
    im_dict["man1_attack"].append(pygame.image.load("./res/man1_attack/man1_4.png"))