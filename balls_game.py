import pygame                   # importing game modules
import random                   # importing the randomizing module
from json import load, dump     # importing a module to handle json files


pygame.init() # initialization of game modules

# creating a window with a resolution of 800 by 600 pixels
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ball-Game") # name on the bar

# preparation of 3 fonts
txt1 = pygame.font.Font("freesansbold.ttf", 32)
txt2 = pygame.font.Font("freesansbold.ttf", 24)
txt3 = pygame.font.Font("freesansbold.ttf", 64)

# I set 7 colors in the dictionary
colors_balls = {1: (254, 254, 0), 2: (0, 128, 0), 3: (255, 128, 0), 4: (128, 0, 0), 5: (0, 0, 255), 6: (237, 19, 19), 7: (255, 0, 255)}

color_list = [] # I create an empty list in which the colors will be held

# variables to save results
score = 0
best_score = 0

mouseX = []
mouseY = []
value_xy = []
correct_field = 0

running = True
flag = False
draw = True


# the function draws the lines of the game board
def board_lines():
    # horizontal and vertical line
    vertical_line = pygame.Surface([1, 540])
    horizontal_line = pygame.Surface([540, 1])
    # color fill
    vertical_line.fill((255, 255, 255))
    horizontal_line.fill((255, 255, 255))
    # start coordinates
    x = 230
    y = 30
    
    xy_move = 60 # move by px
    
    # draw 10 horizontal lines (xy_move - distance)
    for _ in range(10):
        screen.blit(vertical_line, (x,y))
        x += xy_move    
    
    x = 230 # after the loop you need to reset x to the initial setting
    
    # draw 10 vertical lines (xy_move - distance)
    for _ in range(10):
        screen.blit(horizontal_line, (x,y))
        y += xy_move


# the function draws the lines for next 3 balls
def next_balls_lines():
    # horizontal and vertical line
    horizontal_line = pygame.Surface([180, 1])
    vertical_line = pygame.Surface([1, 60])
    # color fill
    vertical_line.fill((255, 255, 255))
    horizontal_line.fill((255, 255, 255))
    # start coordinates
    x= 10
    y=200

    # draw a lines
    screen.blit(horizontal_line, (x, y))
    screen.blit(horizontal_line, (x, y + 60))
    screen.blit(vertical_line, (x, y))
    screen.blit(vertical_line, (x + 60, y))
    screen.blit(vertical_line, (x + 120, y))
    screen.blit(vertical_line, (x + 180, y))


# function creating the reset button
def reset_box():
    # drawing a reset button in color
    box_reser = pygame.Surface([160, 55])
    box_reser.fill((165, 208, 232))
    screen.blit(box_reser, (20,350))
    # adding text to the button
    reset_txt = txt2.render("R - RESET", True, (59, 32, 212))
    screen.blit(reset_txt, (40, 365))


# function creating rectangle with result
def score_box():
    # drawing a rectangle with result
    box_score = pygame.Surface([160, 110])
    box_score.fill((165, 208, 232))
    screen.blit(box_score, (20, 30))
    # adding text and current score 
    score_txt_1 = txt1.render("SCORE", True, (59, 32, 212))
    screen.blit(score_txt_1, (42, 40))
    score_txt_2 = txt1.render(str(score), True, (59, 32, 212))
    screen.blit(score_txt_2, (30, 100))


# function creating rectangle with the best score
def the_best_score_box():
    # drawing a rectangle with the best score
    box_score = pygame.Surface([160, 110])
    box_score.fill((165, 208, 232))
    screen.blit(box_score, (20, 450))
    # adding text and the best score
    score_txt_1 = txt2.render("THE BEST", True, (59, 32, 212))
    screen.blit(score_txt_1, (40, 455))
    score_txt_2 = txt2.render("SCORE", True, (59, 32, 212))
    screen.blit(score_txt_2, (58, 480))
    score_txt_3 = txt1.render(str(best_score), True, (59, 32, 212))
    screen.blit(score_txt_3, (30, 520))


# function creates a rectangle with information about the end of the game
def game_over_box():
    # drawing a rectangle with game over information
    box_game_over = pygame.Surface([450, 150])
    box_game_over.fill((255, 255, 255))
    screen.blit(box_game_over, (275, 190))
    # adding text Game Over
    game_over_txt1 = txt3.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game_over_txt1, (300, 200))
    # adding text and score
    game_over_txt2 = txt1.render("SCORE " + str(score), True, (0, 0, 0))
    screen.blit(game_over_txt2, (410, 260))
    # adding text how to start a new game
    game_over_txt3 = txt2.render("TO RESTART PRESS R", True, (0, 0, 0))
    screen.blit(game_over_txt3, (370, 300))


# function drawing a line separating the game board from the results
def line_score():
    line_score = pygame.Surface([3, 600])
    screen.blit(line_score, (200, 0))


# function drawing board
def board():
    screen_game = pygame.Surface([540, 540])
    screen_game.fill((166, 193, 237))
    screen.blit(screen_game, (230, 30))


# creating a 9 x 9 matrix for start (filled with zeros)
def matrix_start():
    start_matrix = []
    matrX = []
    for _ in range(9):
        for _ in range(9):
            matrX.append(0)
        start_matrix.append(matrX)
        matrX = []
    return start_matrix


# a function that creates a matrix with the coordinates of the centers of each playing field
def center_matrix(i,j):
    middleX = 260
    middleY = 60
    line = []
    matrix_middle = []
    for w in range(9):
        for q in range(9):
            center_coordinates = (middleX, middleY)
            line.append(center_coordinates)
            middleX += 60
        matrix_middle.append(line)
        middleY += 60
        middleX = 260
        line = []
    return matrix_middle[i][j]


# game start function
def start():
    # takes a matrix of 9 x 9 zeros as the game state matrix
    matrix_state = matrix_start()
    # drawing 3 consecutive colors of balls
    for _ in range(3):
        color_list.append(random.randint(1,7))
        # drawing a place on the board when a redraw is already occupied
        run = True
        while run:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if matrix_state[x][y] == 0:
                # color draw for this item
                matrix_state[x][y] = random.randint(1, 7)
                run = False
    return matrix_state


# function checks whether it is possible to move the ball to the selected point
def path_check(startX, startY, endX, endY):
    to_check = [(startX, startY)]
    accessible = []
    end = (endX, endY)
    possible = False
    # checking every nearby point
    # if the conditions are met, adding to the list of points to be checked and the list of available points
    for i in to_check:
        if (i[1] - 1) >= 0 and matrix_state[i[0]][i[1] - 1] == 0:
            if (i[0], (i[1] - 1)) not in to_check:
                to_check.append((i[0], (i[1] - 1)))
            if (i[0], (i[1] - 1)) not in accessible:
                accessible.append((i[0], (i[1] - 1)))
        if (i[1] + 1) < 9 and matrix_state[i[0]][i[1] + 1] == 0:
            if (i[0], (i[1] + 1)) not in to_check:
                to_check.append((i[0], (i[1] + 1)))
            if (i[0], (i[1] + 1)) not in accessible:
                accessible.append((i[0], (i[1] + 1)))
        if (i[0] - 1) >= 0 and matrix_state[i[0] - 1][i[1]] == 0:
            if ((i[0] - 1), i[1]) not in to_check:
                to_check.append(((i[0] - 1), i[1]))
            if ((i[0] - 1), i[1]) not in accessible:
                accessible.append(((i[0] - 1), i[1]))
        if (i[0] + 1) < 9 and matrix_state[i[0] + 1][i[1]] == 0:
            if ((i[0] + 1), i[1]) not in to_check:
                to_check.append(((i[0] + 1), i[1]))
            if ((i[0] + 1), i[1]) not in accessible:
                accessible.append(((i[0] + 1), i[1]))
        if end in accessible:
            possible = True
            break
    return possible


# checking if at least five balls of the same color are placed next to each other vertically, horizontally or diagonally
def check_5(x):
    xy_coordinates = []
    or_next_x = []
    or_next_y = []
    or_next_xy = []
    or_next_xym = []
    deletion = []
    # saving the coordinates of balls of the same color to the list
    for i in range(9):
        for j in range(9):
            if matrix_state[i][j] == x:
                xy_coordinates.append((i, j))
    
    for i in xy_coordinates:
        x = 0
        y = 0
        # horizontally  
        for j in range(5):
            next = ((i[0] + x, i[1]))
            if next in xy_coordinates:
                or_next_x.append(next)
            else:
                or_next_x = []
                x = 0
                break
            x += 1
        # vertical
        for j in range(5):
            next = ((i[0], i[1] + y))
            if next in xy_coordinates:
                or_next_y.append(next)
            else:
                or_next_y = []
                y = 0
                break
            y += 1
        
        s = 0
        z = 0
        # "diagonally" 
        for j in range(5):
            next = ((i[0] + s, i[1] + z))
            if next in xy_coordinates:
                or_next_xy.append(next)
            else:
                or_next_xy = []
                s = 0
                z = 0
                break
            s += 1
            z += 1
        s = 0
        z = 0
        # "diagonally" 
        for j in range(5):
            next = ((i[0] - s, i[1] + z))
            if next in xy_coordinates:
                or_next_xym.append(next)
            else:
                or_next_xym = []
                s = 0
                z = 0
                break
            s += 1
            z += 1
        # coordinates to delate
        for i in or_next_x:
            if i not in deletion:
                deletion.append(i)
        for i in or_next_y:
            if i not in deletion:
                deletion.append(i)
        for i in or_next_xy:
            if i not in deletion:
                deletion.append(i)
        for i in or_next_xym:
            if i not in deletion:
                deletion.append(i)
    return deletion


# the function reads the best result from the json file
def read_best_score():
    with open('best_score.json') as data:
        score_save = load(data)
        return score_save["best_score"]


# clearing lists with mouse event data
def clear_mouse():
    mouseY.clear()
    mouseX.clear()
    value_xy.clear()


# setting the best_score value taken from the file
best_score = read_best_score()

# running the start function and saving the returned matrix as the state of the game
matrix_state = start()
# game loop 
while running:
    screen.fill((208, 236, 245)) # filling with color
    # calling drawing functions
    line_score()
    board()
    board_lines()
    next_balls_lines()
    reset_box()
    score_box()
    the_best_score_box()

    # changing the color of a given field after the first mouse click
    if flag:
        lin2 = pygame.Surface([60, 60])
        lin2.fill((82, 98, 161))
        screen.blit(lin2, (230 + mouseX[-1] * 60, 30 + mouseY[-1] * 60))


    # displaying the circles in the previously drawn color
    # next 3 balls
    xx = 40
    yy = 230
    for i in color_list:
        pygame.draw.circle(screen, colors_balls[i], (xx, yy), 20)
        xx += 60
    # game board
    for i in range(9):
        for j in range(9):
            if matrix_state[i][j] != 0:
                pygame.draw.circle(screen, colors_balls[matrix_state[i][j]], center_matrix(i,j), 20)
    
    # check if the game is over
    zero = 0
    for i in matrix_state:
        for j in i:
            if j == 0:
                zero += 1
    # if there are less than 3 empty fields on the board, call the function
    if zero < 3:
        game_over_box()
    # checking if the result is greater than the best result so far
    if score > best_score:
        # saving to json file
        with open('best_score.json', 'w') as data:
            score_save = {"best_score": score}
            dump (score_save, data)
        
        best_score = read_best_score()
           
    # display
    pygame.display.flip()

    # after pressing r reset the game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        color_list = []
        matrix_state = start()
        score = 0
        flag = False
    # click on reset box - reset the game
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if 20 <= pos[0] <= 180 and 350 <= pos[1] <= 405 and mouse[0] == True:
        color_list = []
        matrix_state = start()
        score = 0
        flag = False
    # event listening
    for event in pygame.event.get():
        # press exit game
        if event.type == pygame.QUIT:
            running = False
        # game algorithm - mouse clicks on the game board
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                # read color and add to value_xy
                if 230<pos[0]<770 and 30<pos[1]<570:
                    mouseX.append((int(pos[0]) - 230) // 60)
                    mouseY.append((int(pos[1]) - 30) // 60)
                    value_xy.append(matrix_state[mouseY[-1]][mouseX[-1]])
                    # checking whether it is the first click of the mouse or the second and whether it is on an empty field or a field with a colored ball
                    if value_xy[-1] != 0 and correct_field % 2 == 0:
                        correct_field += 1
                        flag = True
                    elif value_xy[-1] == 0 and correct_field % 2 == 1:
                        correct_field += 1
                        flag = False
                        # checking if there is a path between the first and second mouse click
                        if path_check(mouseY[-2], mouseX[-2], mouseY[-1], mouseX[-1]):
                            # ball shift
                            matrix_state[mouseY[-1]][mouseX[-1]] = value_xy[-2]
                            matrix_state[mouseY[-2]][mouseX[-2]] = 0
                            # calling the check_5 function, clearing the fields and adding points to the result
                            for i in check_5(value_xy[-2]):
                                matrix_state[i[0]][i[1]] = 0
                                score += 2
                                draw = False
                            # drawing the next 3 balls and places for the previous ones
                            if draw:
                                for i in color_list:
                                    run = True
                                    while run:
                                        x = random.randint(0, 8)
                                        y = random.randint(0, 8)
                                        if matrix_state[x][y] == 0:
                                            matrix_state[x][y] = i
                                            # checking whether the added balls will not create a line of five
                                            for j in check_5(i):
                                                matrix_state[j[0]][j[1]] = 0
                                                score += 2
                                            run = False
                                # draw another 3 balls
                                color_list = []
                                for i in range(3):
                                    color_list.append(random.randint(1, 7))
                            
                            draw = True
                            clear_mouse()
                    else:
                        clear_mouse()
                        correct_field = 0
                        flag = False 