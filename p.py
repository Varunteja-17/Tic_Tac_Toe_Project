import pygame as pg, sys, time, random
from pygame.locals import *

XO = 'x'
winner = None
draw = False
width, height = 400, 400
white = (255, 255, 255)
line_color = (10, 10, 10)
TTT = [[None]*3 for _ in range(3)] 

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe with Bot")

# Load images (make sure these files exist)
opening = pg.image.load('tic tac opening.png')
x_img = pg.image.load('x.png')
o_img = pg.image.load('o.png')
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))

def game_opening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    pg.draw.line(screen, line_color, (width/3, 0), (width/3, height), 7)
    pg.draw.line(screen, line_color, (2*width/3, 0), (2*width/3, height), 7)
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, 2*height/3), (width, 2*height/3), 7)
    draw_status()

def draw_status():
    global draw
    font = pg.font.Font(None, 30)

    if winner:
        message = winner.upper() + " won!"
    elif draw:
        message = "Game Draw!"
    else:
        message = XO.upper() + "'s Turn"

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(width/2, 450))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global TTT, winner, draw
    for row in range(3):
        if TTT[row][0] == TTT[row][1] == TTT[row][2] and TTT[row][0] is not None:
            winner = TTT[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row+0.5)*height/3), (width, (row+0.5)*height/3), 4)
            break
    for col in range(3):
        if TTT[0][col] == TTT[1][col] == TTT[2][col] and TTT[0][col] is not None:
            winner = TTT[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col+0.5)*width/3, 0), ((col+0.5)*width/3, height), 4)
            break
    if TTT[0][0] == TTT[1][1] == TTT[2][2] and TTT[0][0] is not None:
        winner = TTT[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
    elif TTT[0][2] == TTT[1][1] == TTT[2][0] and TTT[0][2] is not None:
        winner = TTT[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all(all(cell is not None for cell in row) for row in TTT) and winner is None:
        draw = True

    draw_status()

def drawXO(row, col):
    global XO
    posx = (row - 1) * width/3 + 30
    posy = (col - 1) * height/3 + 30
    TTT[row-1][col-1] = XO
    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()

def userClick():
    x, y = pg.mouse.get_pos()
    col = x // (width // 3) + 1 if x < width else None
    row = y // (height // 3) + 1 if y < height else None
    if row and col and TTT[row-1][col-1] is None:
        drawXO(row, col)
        check_win()
        if not (winner or draw):
            pg.time.delay(500)
            bot_move()

def bot_move():
    global XO
    if winner or draw:
        return
    empty = [(r, c) for r in range(3) for c in range(3) if TTT[r][c] is None]
    if empty:
        row, col = random.choice(empty)
        drawXO(row+1, col+1)
        check_win()


game_opening()
running = True


while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
            break
        elif event.type == MOUSEBUTTONDOWN and XO == 'x' and not (winner or draw):
            userClick()
    
    if winner or draw:
        pg.display.update()
        time.sleep(2)
        if winner:
            print(f"\nGame Over: {winner.upper()} won!")
        elif draw:
            print("\nGame Over: It's a Draw!")
        running = False

    pg.display.update()
    CLOCK.tick(fps)

pg.quit()
sys.exit()
