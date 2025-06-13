import csv
import random
import sys
from copy import copy

from card import Card
from button import Button
import pygame
from pygame.locals import *

DIFFICULTY = 10
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
GRID_WIDTH, GRID_HEIGHT = 300, 400
LINE_WIDTH = 2
GRID_SIZE = 3
GRID_X = (WINDOWWIDTH - GRID_WIDTH) // 2
GRID_Y = (WINDOWHEIGHT - GRID_HEIGHT) // 2
CELL_WIDTH = GRID_WIDTH // GRID_SIZE
CELL_HEIGHT = GRID_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED         = (255, 0, 0)
GREEN       = (0, 255, 0)
BLUE        = (0, 0, 255)
YELLOW      = (255, 255, 0)
CYAN        = (0, 255, 255)
MAGENTA     = (255, 0, 255)
ORANGE      = (255, 165, 0)
PURPLE      = (128, 0, 128)
BROWN       = (139, 69, 19)
PINK        = (255, 192, 203)
DARK_GRAY   = (64, 64, 64)
LIGHT_GRAY  = (192, 192, 192)
NAVY_BLUE   = (0, 0, 128)
TEAL        = (0, 128, 128)
BACKGROUNDCOLOR = GRAY
FIELDSIZEX = 300
FIELDSIZEY = 400
CARD_WIDTH=CELL_WIDTH-LINE_WIDTH
CARD_HEIGHT=CELL_HEIGHT-LINE_WIDTH



def load_cards_from_csv():
    filename = "cards.csv"
    card_list=[]
    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            card_list.append(Card(row[0], row[1], row[2], row[3], row[4]))

    return card_list


# def drawField():
#     DISPLAYSURF.fill(BACKGROUNDCOLOR)
#     spaceRect = pygame.Rect(0, 0, 200, 200)
#     # pygame.draw.rect(pygame.display.get_surface(), BLACK, (100, 100, 200, 150))
#     # pygame.draw.line(pygame.display.get_surface(), BLACK, (100,100), (200,200), 5)
#
#     for i in range(1, GRID_SIZE):  # Vertical lines
#         x = GRID_X + i * CELL_WIDTH
#         pygame.draw.line(pygame.display.get_surface(), BLACK, (x, GRID_Y), (x, GRID_Y + GRID_HEIGHT), LINE_WIDTH)
#
#     for i in range(1, GRID_SIZE):  # Horizontal lines
#         y = GRID_Y + i * CELL_HEIGHT
#         pygame.draw.line(pygame.display.get_surface(), BLACK, (GRID_X, y), (GRID_X + GRID_WIDTH, y), LINE_WIDTH)
#
#     rect_x = GRID_X+CELL_WIDTH+LINE_WIDTH
#     rect_y = GRID_Y+LINE_WIDTH
#     rect_width = CELL_WIDTH-LINE_WIDTH
#     rect_height = CELL_HEIGHT-LINE_WIDTH
#     pygame.draw.rect(pygame.display.get_surface(), WHITE, (rect_x, rect_y, rect_width, rect_height))

def welcome_screen():
    font = pygame.font.SysFont(None, 72)
    surf = font.render("welcome screen", True, WHITE)
    rect = surf.get_rect()
    rect.topleft = (WINDOWWIDTH //4 , 5)
    DISPLAYSURF.blit(surf, rect)
    surf = font.render("Card game 3x3", True, WHITE)
    rect = surf.get_rect()
    rect.topleft = (WINDOWWIDTH //4 , 155)
    DISPLAYSURF.blit(surf, rect)
    pygame.display.update()
    pygame.time.wait(500)
    DISPLAYSURF.fill(BACKGROUNDCOLOR)

def drawCard(card):
    print(1)


if __name__ == '__main__':
    global FPSCLOCK, DISPLAYSURF
    card_list=load_cards_from_csv()
    random.shuffle(card_list)
    left_hand=[]
    right_hand=[]
    cards_on_field=[None] * 9
    for i in range (5):
        left_hand.append(card_list[i])
    for i in range (5,10):
        right_hand.append(card_list[i])
    selected_card = 0
    selected_spot = 0


    pygame.init()
    pygame.mixer.music.load("song18.mp3")
    pygame.mixer.music.play(-1)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('card 3x3')
    DISPLAYSURF.fill(BACKGROUNDCOLOR)
    welcome_screen()
    game_state="left_select_card"

    # card1 = Button(50,75,50,65)
    # card2 = Button(50, 150, 50, 65)
    # card3 = Button(50, 225, 50, 65)
    # card4 = Button(50, 300, 50, 65)
    # card5 = Button(50, 375, 50, 65)
    # card1r = Button(WINDOWWIDTH-65-50,75,50,65)
    # card2r = Button(WINDOWWIDTH-65-50, 150, 50, 65)
    # card3r = Button(WINDOWWIDTH-65-50, 225, 50, 65)
    # card4r = Button(WINDOWWIDTH-65-50, 300, 50, 65)
    # card5r = Button(WINDOWWIDTH-65-50, 375, 50, 65)

    # Create buttons
    left_buttons = []
    right_buttons = []
    field_buttons =[]

    # Position constants
    x_left = 50
    x_right = WINDOWWIDTH - 65 - 50
    y_start = 75
    spacing = 75
    width = 50
    height = 65

    for i in range(5):
        y = y_start + i * spacing
        left_buttons.append(Button(x_left, y, width, height))
        right_buttons.append(Button(x_right, y, width, height))

    for i in range(len(cards_on_field)):
        x = i % 3 * CELL_WIDTH + GRID_X + LINE_WIDTH
        y = GRID_Y+LINE_WIDTH + int(i/3) * CELL_HEIGHT
        field_buttons.append(Button(x, y, CELL_WIDTH-LINE_WIDTH, CELL_HEIGHT-LINE_WIDTH))

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if game_state=="menu":
            DISPLAYSURF.fill(TEAL)


        for i in range(1, GRID_SIZE):
             x = GRID_X + i * CELL_WIDTH
             pygame.draw.line(pygame.display.get_surface(), BLACK, (x, GRID_Y), (x, GRID_Y + GRID_HEIGHT), LINE_WIDTH)

        for i in range(1, GRID_SIZE):
            y = GRID_Y + i * CELL_HEIGHT
            pygame.draw.line(pygame.display.get_surface(), BLACK, (GRID_X, y), (GRID_X + GRID_WIDTH, y), LINE_WIDTH)





        if game_state == "left_select_card":
            for i, btn in enumerate(left_buttons):
                if btn.draw(DISPLAYSURF, left_hand[i]):
                    selected_card=i
                    print(selected_card)
                    game_state="left_place_card"
        else:
            for i, btn in enumerate(left_buttons):
                btn.draw(DISPLAYSURF, left_hand[i])

        if game_state == "left_place_card":
            for i, btn in enumerate(field_buttons):
                if cards_on_field[i] is None:
                    if btn.colour_show(DISPLAYSURF, BACKGROUNDCOLOR):
                        selected_spot = i
                        print(selected_spot)
                        game_state = "move_card"
                else:
                    btn.draw(DISPLAYSURF, cards_on_field[i])
        if game_state == "move_card":
            cards_on_field[selected_spot] = copy(left_hand[selected_card])
            # print(left_hand[selected_card].N)
            left_hand[selected_card].is_hidden=True
            cards_on_field[selected_spot].colour=GREEN
            game_state="check_move_results"

        # if game_state == "check_move_results":
        #     if

        for i, btn in enumerate(right_buttons):
            btn.draw(DISPLAYSURF, right_hand[i])

        for i, btn in enumerate(field_buttons):
            if cards_on_field[i] is None:
                btn.colour_show(DISPLAYSURF, BACKGROUNDCOLOR)
            else:
                btn.draw(DISPLAYSURF, cards_on_field[i])


        pygame.display.update()
        FPSCLOCK.tick()

