#!/usr/bin/python
# Program: Tic-Tac-Toe Game
# Author: Cherol Phoshoko
import pygame, sys
import numpy as np
import time


# Initializing pygame and Setting up display screen
pygame.init()
screen_width = 600
screen_height = 600
pygame.display.set_caption("Tic-Tac-Toe by Cherol Phoshoko")
screen = pygame.display.set_mode((screen_width, screen_height))

# Constant variables
tokenX_color = (228, 50, 2)
tokenO_color = (22, 70, 2)
background_col = (23, 23, 23)
gridlines_col = (49, 49, 49)  # lines drawing grid layout of game board
gridlines_width = 12

# numpy array used to create 3x3 game board,
rows = 3
cols = 3
board = np.zeros((rows, cols))

# these represent the width and size of the X and O tokens
radius = 60
o_width = 15
x_width = 20
space = 55  # will be used to create space between tokens and gridlines

# variables used to create introductory game image when program runs
# image will be displayed for 5 seconds before game starts.

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render("Tic-Tac-Toe", True, (23, 23, 23), (49, 49, 49))
textRect = text.get_rect()
textRect.center = (screen_width // 2, screen_height // 2)
screen.fill((23, 23, 23))
t = 5

while t > 0:
    pygame.display.update()
    mins, secs = divmod(t, 60)
    time.sleep(1)
    t -= 1
    screen.blit(text, textRect)


#  draws grid lines
def grid():
    pygame.draw.line(screen, gridlines_col, (0, 200), (600, 200), gridlines_width)
    pygame.draw.line(screen, gridlines_col, (0, 400), (600, 400), gridlines_width)
    pygame.draw.line(screen, gridlines_col, (200, 0), (200, 600), gridlines_width)
    pygame.draw.line(screen, gridlines_col, (400, 0), (400, 600), gridlines_width)


# draws tokens
def draw_token():
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                pygame.draw.line(screen, tokenX_color, (int(col*200 + space), int(row*200 + 200 - space)),
                                 (int(col*200 + 200 - space), int(row*200 + space)), x_width)
                pygame.draw.line(screen, tokenX_color, (int(col*200 + space), int(row*200 + space)),
                                 (int(col*200 + 200 - space), int(row*200 + 200 - space)), x_width)
            if board[row][col] == 2:
                pygame.draw.circle(screen, tokenO_color, (int(col*200 + 100), int(row*200 + 100)), radius, o_width)

            
# marks selected grid square with player token
def mark_grid(row, col, token):
    board[row][col] = token


# determines if grid is empty
def empty_grid(row, col):
    return board[row][col] == 0


# determines if all grids are filled or 'marked'
def grids_filled():
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                return False
            
    return True


# Determines how a player wins, if 3 horizontal, vertical or diagonal grids match
def winner(token):
    for col in range(cols):
        if board[0][col] == token and board[1][col] == token and board[2][col] == token:
            vertical_win(col, token)
            return True
        
    for row in range(rows):
        if board[row][0] == token and board[row][1] == token and board[row][2] == token:
            horizontal_win(row, token)
            return True
        
    if board[0][0] == token and board[1][1] == token and board[2][2] == token:
        diagonal_desc(token)
        return True
    elif board[2][0] == token and board[1][1] == token and board[0][2] == token:
        diagonal_asc(token)
        return True


# Displays who wins the game
def display_winner(token):
    x = 5
    font = pygame.font.Font('freesansbold.ttf', 70)
    if token == 1:
        winning_token = "X WINS!"
        text = font.render(winning_token, True, (228, 50, 2), (23, 23, 23))
    elif token == 2:
        winning_token = "O WINS!"
        text = font.render(winning_token, True, (22, 70, 2), (23, 23, 23))
        
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height // 2)
    screen.set_colorkey((23, 23, 23))
    
    while x > 0:
        pygame.display.update()
        mins, secs = divmod(x, 60)
        time.sleep(1)
        screen.blit(text, textRect)
        x -= 1
        

# these last for functions are used to draw the line crossing matching winner grids
def vertical_win(col, token):
    posX = col * 200 + 100
    if token == 1:
        color = tokenX_color
    elif token == 2:
        color = tokenO_color
    pygame.draw.line(screen, color, (posX, 15), (posX, screen_height - 15), 15)


def horizontal_win(row, token):
    posY = row * 200 + 100
    if token == 1:
        color = tokenX_color
    elif token == 2:
        color = tokenO_color
    pygame.draw.line(screen, color, (15, posY), (screen_width - 15, posY), 15)
    

def diagonal_asc(token):
    if token == 1:
        color = tokenX_color
    elif token == 2:
        color = tokenO_color
    pygame.draw.line(screen, color, (15, screen_height - 15), (screen_width - 15, 15), 15)


def diagonal_desc(token):
    if token == 1:
        color = tokenX_color
    elif token == 2:
        color = tokenO_color
    pygame.draw.line(screen, color, (15, 15), (screen_width - 15, screen_height - 15), 15)


# let's players play as often as they want
def restart_game():
    screen.fill(background_col)
    grid()
    
    for row in range(rows):
        for col in range(cols):
            board[row][col] = 0

    
screen.fill(background_col)
grid()
game_over = False
token = 1  # represents current player's token X or O

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # these determine the mouse position within each grid
            # so that user can click a grid by clicking anywhere within a it.
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            pick_row = int(mouse_y // 200)
            pick_col = int(mouse_x // 200)

            # this let's a player pick a grid if it's not marked yet and draws the current
            # player token in the grid, switching between players til game ends.
            if empty_grid(pick_row, pick_col):
                if token == 1:  # x
                    mark_grid(pick_row, pick_col, 1)
                    if winner(token):
                        game_over = True
                    token = 2

                elif token == 2:  # o
                    mark_grid(pick_row, pick_col, 2)
                    if winner(token):
                        game_over = True
                    token = 1

                draw_token()   # will draw token X/O token on whichever block they chose
                if game_over and token == 1:
                    token = 2
                    display_winner(token)
                    break
                if game_over and token == 2:
                    token = 1
                    display_winner(token)
                    break

        # Player can restart by pressing r key when game is over or grids are filled
        if (event.type == pygame.KEYDOWN and game_over) or (event.type == pygame.KEYDOWN and grids_filled):
            if event.key == pygame.K_r:
                restart_game()
                token = 1
                game_over = False

    pygame.display.update()
