import pygame
import datetime
from pygame.locals import *
pygame.init()
white = (255, 255, 255)

def make_relative((a, b)):
    return (a-200)/200, (b-200)/200

class Board:
    board = pygame.Surface((600, 600))
    screen = pygame.display.set_mode([1000, 1000])
    grid = []
    scores = {'X': 0, '0': 0, 'tie': 0}
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = pygame.font.SysFont('Comic Sans MS', 30).render("Player X: 0    Player O: 0    Ties: 0", True, white)
    player = 'X'
    remaining = 9

    def __init__(self):
        pygame.display.set_caption("Tic Tac Toe")
        self.reset_board()
        self.show_board()

    def reset_board(self):
        self.board = pygame.Surface((600, 600))
        ## vertical
        pygame.draw.line(self.board, white, [200, 0], [200, 600], 5)
        pygame.draw.line(self.board, white, [400, 0], [400, 600], 5)
        ## horizontal
        pygame.draw.line(self.board, white, [0, 200], [600, 200], 5)
        pygame.draw.line(self.board, white, [0, 400], [600, 400], 5)
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.text = self.font.render("Player X: %d    Player O: %d    Ties: %d" % (self.scores['X'], self.scores['0'], self.scores['tie']), True, white)
        self.player = 'X'
        self.remaining = 9

    def show_board(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.board, (200, 200))
        self.screen.blit(self.text, (10, 0))
        pygame.display.flip()

    def check(self):
        (row, col) = make_relative(pygame.mouse.get_pos())
        if row < 0 or row > 3 or col < 0 or col > 600:
            return

        if self.grid[row][col] == 0:
            self.make_move(row, col)

    def make_move(self, row, col):
        centerX, centerY = 100 + row*200, 100 + col*200
        if self.player == 'X':
            pygame.draw.line(self.board, white, [centerX-50, centerY-50], [centerX+50, centerY+50], 3)
            pygame.draw.line(self.board, white, [centerX+50, centerY-50], [centerX-50, centerY+50], 3)
        else:
            pygame.draw.circle(self.board, white, [centerX, centerY], 50, 3)
        self.grid[row][col] = self.player
        self.remaining -= 1

        self.player = 'X' if self.player == '0' else '0'
        print(self.grid)
        self.check_win(row, col)
        self.show_board()

    def has_won(self, whom):
        self.scores[whom] += 1
        self.reset_board()

    def check_win(self, row, col):
        if self.remaining == 0:
            return self.has_won('tie')

        if self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
            return self.has_won(self.grid[1][col])
        if self.grid[row][0] == self.grid[row][1] == self.grid[row][2]:
            return self.has_won(self.grid[row][1])
        if row == col and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return self.has_won(self.grid[1][1])
        if col + row == 2 and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return self.has_won(self.grid[1][1])

game_board = Board()
done = False
while not done:
    for event in pygame.event.get():
        if event.type is QUIT:
            done = True
        elif event.type is MOUSEBUTTONUP:
            game_board.check()
pygame.quit()
