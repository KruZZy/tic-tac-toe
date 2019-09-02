import pygame
import time
import random
from pygame.locals import *
from utils import *
from buttons import *
import ai

pygame.init()

game_mode = 0

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

        (row, col) = pygame.mouse.get_pos()
        (row, col) = make_relative(row, col)

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
        self.show()
        time.sleep(2)
        self.scores[whom] += 1
        self.reset()

    def check_win(self, player):
        if self.remaining == 0:
            return self.has_won('tie')

        if wins(self.grid, player):
            return self.has_won(player)

done = False
intro = True
game_board = Board()

buttons = []

buttons.append(Button("vs player", 175, 800, 150, 200, green_active, green_inactive, lambda: start_game(MODE_VS)))
buttons.append(Button("vs computer (hard)", 375, 800, 150, 200, red_active, red_inactive, lambda: start_game(MODE_AI)))
buttons.append(Button("vs computer (normal)", 575, 800, 150, 200, orange_active, orange_inactive, lambda: start_game(MODE_AI_N)))

def start_game(mode):
    global intro, game_mode
    intro = False
    game_mode = mode
    game_board.reset()
    game_board.show()

def draw_intro():
    text = font.render("Select game mode", True, white)
    screen.blit(text, (350, 400))

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

while not done:
    for e in pygame.event.get():
        if e.type is QUIT:
            done = True
        elif e.type is MOUSEBUTTONUP and intro == False:
            if game_mode == MODE_VS or game_board.player == 'X':
                game_board.check()
    if game_mode != MODE_VS and game_board.player == '0':
        ai.move(game_board, game_mode)

    if intro:
        draw_intro()
    else:
        game_board.show()

pygame.quit()
