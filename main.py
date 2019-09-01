import pygame
import datetime
from pygame.locals import *
from buttons import Button, font, sound
pygame.init()
white = (255, 255, 255)
green_active = (114, 207, 56)
green_inactive = (68, 148, 18)
red_active = (201, 68, 58)
red_inactive = (150, 18, 9)

buttons = []
MODE_VS = 1
MODE_AI = 2
game_mode = 0
screen = pygame.display.set_mode([1000, 1000])

def make_relative((a, b)):
    return (a-200)/200, (b-200)/200

class Board:
    grid = []
    scores = {'X': 0, '0': 0, 'tie': 0}
    player = 'X'
    remaining = 9
    is_drawn = False

    def __init__(self):
        self.font = pygame.font.SysFont("comicsansms",20)
        pygame.display.set_caption("Tic Tac Toe")

    def reset(self):
        self.board = pygame.Surface((600, 600))
        ## vertical
        pygame.draw.line(self.board, white, [200, 0], [200, 600], 5)
        pygame.draw.line(self.board, white, [400, 0], [400, 600], 5)
        ## horizontal
        pygame.draw.line(self.board, white, [0, 200], [600, 200], 5)
        pygame.draw.line(self.board, white, [0, 400], [600, 400], 5)
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]
        self.text = self.font.render("Player X: %d    Player O: %d    Ties: %d" % (self.scores['X'], self.scores['0'], self.scores['tie']), True, white)
        self.player = 'X'
        self.remaining = 9
        self.is_drawn = True

    def show(self):
        screen.fill((0, 0, 0))
        screen.blit(self.board, (200, 200))
        screen.blit(self.text, (10, 0))
        pygame.display.flip()

    def check(self):
        (row, col) = make_relative(pygame.mouse.get_pos())

        if row < 0 or row > 2 or col < 0 or col > 2:
            return

        if self.grid[row][col] == None:
            self.make_move(row, col)

    def make_move(self, row, col):
        centerX, centerY = 100 + row*200, 100 + col*200
        if self.player == 'X':
            pygame.draw.line(self.board, white, [centerX-50, centerY-50], [centerX+50, centerY+50], 3)
            pygame.draw.line(self.board, white, [centerX+50, centerY-50], [centerX-50, centerY+50], 3)
        else:
            pygame.draw.circle(self.board, white, [centerX, centerY], 50, 3)
        sound.play()
        self.grid[row][col] = self.player
        self.remaining -= 1

        last_player = self.player
        self.player = 'X' if self.player == '0' else '0'
        self.check_win(last_player)

    def has_won(self, whom):
        self.scores[whom] += 1
        self.reset()

    def check_win(self, player):
        if self.remaining == 0:
            return self.has_won('tie')

        if wins(self.grid, player):
            return self.has_won(player)

def draw_intro():
    text = font.render("Select game mode", True, white)
    screen.blit(text, (350, 400))

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

def start_game():
    global game_board
    game_board.reset()
    game_board.show()

def mode_vs():
    global game_mode, intro
    intro = False
    game_mode = MODE_VS
    start_game()

def mode_ai():
    global game_mode, intro
    intro = False
    game_mode = MODE_AI
    print("mode_ai")
    start_game()

def wins(grid, player):
    win_grids = [
        [grid[0][0], grid[0][1], grid[0][2]],
        [grid[1][0], grid[1][1], grid[1][2]],
        [grid[2][0], grid[2][1], grid[2][2]],
        [grid[0][0], grid[1][0], grid[2][0]],
        [grid[0][1], grid[1][1], grid[2][1]],
        [grid[0][2], grid[1][2], grid[2][2]],
        [grid[0][0], grid[1][1], grid[2][2]],
        [grid[2][0], grid[1][1], grid[0][2]],
    ]
    return [player, player, player] in win_grids

def empty_cells(grid):
    empty = []

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == None:
                empty.append([i, j])
    return empty

def evaluate(grid):
    if wins(grid, 'X'):
        return -10
    if wins(grid, '0'):
        return 10
    else:
        return 0

def is_over(grid):
    return wins(grid, 'X') or wins(grid, 'O')

def minimax(grid, depth, maximise):
    if depth == 0 or is_over(grid):
        return [evaluate(grid), -1, -1]

    if maximise:
        best = [-1000, -1, -1]
    else:
        best = [1000, -1, -1]

    for c in empty_cells(grid):
        i, j = c[0], c[1]
        grid[i][j] = '0' if maximise else 'X'
        score = minimax(grid, depth-1, False if maximise else True)
        grid[i][j] = None
        score[1], score[2] = i, j

        if maximise:
            if score[0] > best[0]:
                best = score
        else:
            if score[0] < best[0]:
                best = score

    return best

def best_ai_move():
    global game_board
    max_depth = len(empty_cells(game_board.grid))
    best = minimax(game_board.grid, max_depth, True)
    game_board.make_move(best[1], best[2])


done = False
intro = True
game_board = Board()
buttons.append(Button("vs player", 300, 800, 150, 200, green_active, green_inactive, mode_vs))
buttons.append(Button("vs computer", 500, 800, 150, 200, red_active, red_inactive, mode_ai))

while not done:
    for e in pygame.event.get():
        if e.type is QUIT:
            done = True
        elif e.type is MOUSEBUTTONUP and intro == False:
            if game_mode == MODE_VS or game_mode == MODE_AI and game_board.player == 'X':
                game_board.check()
    if game_mode == MODE_AI and game_board.player == '0':
        best_ai_move()

    if intro:
        draw_intro()
    else:
        game_board.show()

pygame.quit()
