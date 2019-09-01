import pygame
import datetime
from pygame.locals import *
pygame.init()
white = (255, 255, 255)
green_active = (114, 207, 56)
green_inactive = (68, 148, 18)
red_active = (201, 68, 58)
red_inactive = (150, 18, 9)
screen = pygame.display.set_mode([1000, 1000])
sound = pygame.mixer.Sound("hover.wav")
buttons = []
MODE_VS = 1
MODE_AI = 2
game_mode = 0
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms",30)
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
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
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

        if self.grid[row][col] == 0:
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

        self.player = 'X' if self.player == '0' else '0'
        self.check_win(row, col)

    def has_won(self, whom):
        self.scores[whom] += 1
        self.reset()

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

def text_obj(text, font):
    text_surf = font.render(text, True, white)
    return text_surf, text_surf.get_rect()

class Button:
    def __init__(self, msg, x, y, width, height, color_active, color_inactive, function = None):
        self.rect_area = pygame.Rect(x, y, width, height)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color_active, self.color_inactive = color_active, color_inactive
        self.function = function
        self.msg = msg

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.rect_area.collidepoint(mouse):
            pygame.draw.rect(screen, self.color_active, (self.x, self.y, self.width, self.height))
            if click[0] == 1 and self.function != None:
                sound.play()
                self.function()
        else:
            pygame.draw.rect(screen, self.color_inactive, (self.x, self.y, self.width, self.height))

        text = pygame.font.SysFont("comicsansms",15)
        text_surf, text_rect = text_obj(self.msg, text)
        text_rect.center = (self.x + self.width/2, self.y + self.height/2)
        screen.blit(text_surf, text_rect)

def draw_intro():
    text = font.render("Select game mode", True, white)
    screen.blit(text, (350, 400))

    for button in buttons:
        button.draw()

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

done = False
intro = True
game_board = Board()
buttons.append(Button("vs player", 300, 800, 150, 200, green_active, green_inactive, mode_vs))
buttons.append(Button("vs computer", 500, 800, 150, 200, red_active, red_inactive))

while not done:
    for event in pygame.event.get():
        if event.type is QUIT:
            done = True
        elif event.type is MOUSEBUTTONUP and intro == False:
            game_board.check()

    if intro:
        draw_intro()
    else:
        game_board.show()
pygame.quit()
