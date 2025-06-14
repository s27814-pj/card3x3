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
TURN_TIME_LIMIT=15.0
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
    pygame.time.wait(2500)
    DISPLAYSURF.fill(BACKGROUNDCOLOR)

def print_text(text_in,x,y,back_colour):
    font = pygame.font.SysFont(None, 32)
    text = font.render(str(text_in), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    DISPLAYSURF.fill(back_colour, text_rect)
    DISPLAYSURF.blit(text, text_rect)


if __name__ == '__main__':
    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    pygame.mixer.music.load("song18.mp3")
    pygame.mixer.music.play(-1)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('card 3x3')
    DISPLAYSURF.fill(BACKGROUNDCOLOR)
    welcome_screen()
    game_state="menu"

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    game_state="menu"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    pygame.mixer.music.stop() if pygame.mixer.music.get_busy() else pygame.mixer.music.play(-1)
        if game_state=="menu":
            DISPLAYSURF.fill(BACKGROUNDCOLOR)
            card_list = load_cards_from_csv()
            random.shuffle(card_list)
            left_hand = []
            right_hand = []
            cards_on_field = [None] * 9
            for i in range(5):
                left_hand.append(card_list[i])
            for i in range(5, 10):
                right_hand.append(card_list[i])
            selected_card = 0
            selected_spot = 0
            previous_human_move = True
            score = 0
            remaining_time = TURN_TIME_LIMIT
            rule_plus=False

            left_buttons = []
            right_buttons = []
            field_buttons = []
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
                y = GRID_Y + LINE_WIDTH + int(i / 3) * CELL_HEIGHT
                field_buttons.append(Button(x, y, CELL_WIDTH - LINE_WIDTH, CELL_HEIGHT - LINE_WIDTH))

            start_button=Button(WINDOWWIDTH//3,WINDOWHEIGHT //10, WINDOWWIDTH//3,WINDOWHEIGHT //10)
            start_plus_button=Button(WINDOWWIDTH//3,(WINDOWHEIGHT //10)*3, WINDOWWIDTH//3,WINDOWHEIGHT //10)
            guide_button=Button(WINDOWWIDTH//3,(WINDOWHEIGHT //10)*5, WINDOWWIDTH//3,WINDOWHEIGHT //10)
            exit_button=Button(WINDOWWIDTH//3,(WINDOWHEIGHT //10)*8, WINDOWWIDTH//3,WINDOWHEIGHT //10)
            if start_button.draw_text(DISPLAYSURF, "START", TEAL): game_state= "left_select_card"
            elif start_plus_button.draw_text(DISPLAYSURF,"START PLUS", TEAL):
                rule_plus=True
                game_state="left_select_card"
            elif guide_button.draw_text(DISPLAYSURF, "INSTRUCTIONS", TEAL): game_state= "instructions"
            elif exit_button.draw_text(DISPLAYSURF, "EXIT", TEAL):
                pygame.quit()
                sys.exit()
            else:game_state = "menu"



        if game_state!="menu" and game_state!="instructions":
            if game_state!="results":
                for i in range(1, GRID_SIZE):
                     x = GRID_X + i * CELL_WIDTH
                     pygame.draw.line(DISPLAYSURF, BLACK, (x, GRID_Y), (x, GRID_Y + GRID_HEIGHT), LINE_WIDTH)

                for i in range(1, GRID_SIZE):
                    y = GRID_Y + i * CELL_HEIGHT
                    pygame.draw.line(DISPLAYSURF, BLACK, (GRID_X, y), (GRID_X + GRID_WIDTH, y), LINE_WIDTH)


                font = pygame.font.SysFont(None, 48)
                text = font.render("SCORE: "+ str(score), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.topleft = (10, 5)
                DISPLAYSURF.fill(BACKGROUNDCOLOR, text_rect)
                DISPLAYSURF.blit(text, text_rect)
                pygame.display.update(text_rect)
                font = pygame.font.SysFont(None, 18)
                text = font.render("time left: "+ str(int(remaining_time)), True, (0, 0, 0))
                text_rect.topleft = (10, 40)
                DISPLAYSURF.fill(BACKGROUNDCOLOR, text_rect)
                DISPLAYSURF.blit(text, text_rect)
                pygame.display.update(text_rect)

            if game_state == "left_select_card":
                previous_human_move = True
                for i, btn in enumerate(left_buttons):
                    if btn.draw_card(DISPLAYSURF, left_hand[i]):
                        selected_card=i
                        left_hand[i].colour=TEAL
                        game_state="left_place_card"
            else:
                for i, btn in enumerate(left_buttons):
                    btn.draw_card(DISPLAYSURF, left_hand[i])

            if game_state == "left_place_card":
                for i, btn in enumerate(field_buttons):
                    if cards_on_field[i] is None:
                        if btn.draw_empty(DISPLAYSURF, BACKGROUNDCOLOR):
                            selected_spot = i
                            game_state = "move_card"
                    else:
                        btn.draw_card(DISPLAYSURF, cards_on_field[i])
            if game_state == "move_card":
                cards_on_field[selected_spot] = copy(left_hand[selected_card])
                left_hand[selected_card].is_hidden=True
                cards_on_field[selected_spot].colour=GREEN
                remaining_time=TURN_TIME_LIMIT
                game_state="check_move_results"

            if game_state == "right_comp_move":
                previous_human_move = False
                available_cards = [i for i, card in enumerate(right_hand) if not card.is_hidden]
                available_spots = [i for i, spot in enumerate(cards_on_field) if spot is None]
                if available_spots==[] or available_cards==[]:
                    pygame.time.wait(200)
                    game_state="results"
                else:
                    selected_card = random.choice(available_cards)
                    selected_spot = random.choice(available_spots)
                    cards_on_field[selected_spot]=copy(right_hand[selected_card])
                    cards_on_field[selected_spot].colour=RED
                    right_hand[selected_card].is_hidden=True
                    game_state="check_move_results"

            if game_state == "check_move_results":
                if previous_human_move:
                    colour=GREEN
                else:
                    colour=RED
                sum_plus =[None] *4
                if selected_spot>2: #check north
                    if cards_on_field[selected_spot-3] is not None:
                        if cards_on_field[selected_spot].N > cards_on_field[selected_spot-3].S:
                            cards_on_field[selected_spot-3].colour=colour
                        sum_plus[0]=int(cards_on_field[selected_spot].N)+int(cards_on_field[selected_spot-3].S)
                if selected_spot<6: #south
                    if cards_on_field[selected_spot+3] is not None:
                        if cards_on_field[selected_spot].S > cards_on_field[selected_spot+3].N:
                            cards_on_field[selected_spot+3].colour=colour
                        sum_plus[1] = int(cards_on_field[selected_spot].S) + int(cards_on_field[selected_spot+3].N)
                if selected_spot % 3 !=0: #west
                    if cards_on_field[selected_spot-1] is not None:
                        if cards_on_field[selected_spot].W > cards_on_field[selected_spot-1].E:
                            cards_on_field[selected_spot-1].colour=colour
                        sum_plus[2] = int(cards_on_field[selected_spot].W) + int(cards_on_field[selected_spot-1].E)
                if selected_spot %3 !=2:
                    if cards_on_field[selected_spot+1] is not None:
                        if cards_on_field[selected_spot].E > cards_on_field[selected_spot+1].W:
                            cards_on_field[selected_spot+1].colour=colour
                        sum_plus[3] = int(cards_on_field[selected_spot].E) + int(cards_on_field[selected_spot+1].W)
                if rule_plus:
                    indices=[]
                    for i in range(4):
                        for j in range(i+1, 4):
                            if sum_plus[i] is not None and sum_plus[i]==sum_plus[j]:
                                indices.append(j)
                                indices.append(i)
                                print("PLUS")
                    if 0 in indices:
                        cards_on_field[selected_spot - 3].colour = colour
                    if 1 in indices:
                        cards_on_field[selected_spot + 3].colour = colour
                    if 2 in indices:
                        cards_on_field[selected_spot - 1].colour = colour
                    if 3 in indices:
                        cards_on_field[selected_spot + 1].colour = colour



                score = sum(
                    1 for card in cards_on_field
                    if card is not None and card.colour == GREEN
                )
                if previous_human_move:
                    game_state="right_comp_move"
                else:
                    game_state="left_select_card"


            for i, btn in enumerate(right_buttons):
                btn.draw_card(DISPLAYSURF, right_hand[i])

            for i, btn in enumerate(field_buttons):
                if cards_on_field[i] is None:
                    btn.draw_empty(DISPLAYSURF, BACKGROUNDCOLOR)
                else:
                    btn.draw_card(DISPLAYSURF, cards_on_field[i])

            if game_state=="results":

                DISPLAYSURF.fill(BACKGROUNDCOLOR)
                if score >5 and not None in cards_on_field:
                    print("You won")

                    font = pygame.font.SysFont(None, 96)
                    text = font.render("SCORE: " + str(score), True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (WINDOWWIDTH //2, WINDOWHEIGHT //2)
                    DISPLAYSURF.fill(BACKGROUNDCOLOR, text_rect)
                    DISPLAYSURF.blit(text, text_rect)
                    text = font.render("You won", True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (WINDOWWIDTH //2, WINDOWHEIGHT //4)
                    DISPLAYSURF.fill(BACKGROUNDCOLOR, text_rect)
                    DISPLAYSURF.blit(text, text_rect)


                else:
                    font = pygame.font.SysFont(None, 96)
                    text = font.render("SCORE: " + str(score), True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (WINDOWWIDTH //2, WINDOWHEIGHT //2)
                    pygame.display.get_surface().fill(BACKGROUNDCOLOR, text_rect)
                    pygame.display.get_surface().blit(text, text_rect)
                    text = font.render("You lost", True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (WINDOWWIDTH //2, WINDOWHEIGHT //4)
                    pygame.display.get_surface().fill(BACKGROUNDCOLOR, text_rect)
                    pygame.display.get_surface().blit(text, text_rect)
                remaining_time=TURN_TIME_LIMIT

            if remaining_time<0: game_state="results"

        if game_state=="instructions":

            DISPLAYSURF.fill(TEAL)
            print_text("get score >5, act before end of time for turn",WINDOWWIDTH//2, WINDOWHEIGHT//10, TEAL)
            print_text("press M to mute music", WINDOWWIDTH // 2, (WINDOWHEIGHT // 10)*2, TEAL)
            print_text("press R to restart", WINDOWWIDTH // 2, (WINDOWHEIGHT // 10) * 3, TEAL)
            print_text("press R to return to menu", WINDOWWIDTH // 2, (WINDOWHEIGHT // 10) * 4, TEAL)


        pygame.display.update()
        dt= FPSCLOCK.tick(FPS)
        remaining_time -= dt/1000

