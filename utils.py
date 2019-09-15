import pygame

pygame.init()

screenInfo = pygame.display.Info()

game_w = min(screenInfo.current_w, screenInfo.current_h)
game_h = game_w
screen = pygame.display.set_mode([game_w, game_h])
font = pygame.font.SysFont("comicsansms",20)

white = (255, 255, 255)
green_active = (114, 207, 56)
green_inactive = (68, 148, 18)
red_active = (201, 68, 58)
red_inactive = (150, 18, 9)
orange_active = (232, 192, 63)
orange_inactive = (168, 138, 40)
blue = (60, 127, 185)
yellow = (239, 235, 100)

MODE_VS = 1
MODE_AI = 2
MODE_AI_N = 3

def make_relative(a, b):
    return int((a-.2 * game_w)//(.2 * game_w)), int((b-.2 * game_h)//(.2 * game_h))

def wins(grid, player):
    win_grids = [
        [grid[0][0], grid[0][1], grid[0][2]], # row 1
        [grid[1][0], grid[1][1], grid[1][2]], # row 2
        [grid[2][0], grid[2][1], grid[2][2]], # row 3
        [grid[0][0], grid[1][0], grid[2][0]], # col 1
        [grid[0][1], grid[1][1], grid[2][1]], # col 2
        [grid[0][2], grid[1][2], grid[2][2]], # col 3
        [grid[0][0], grid[1][1], grid[2][2]], # diag 1
        [grid[2][0], grid[1][1], grid[0][2]], # diag 2
    ]
    return [player, player, player] in win_grids
