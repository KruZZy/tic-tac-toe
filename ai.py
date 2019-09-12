from utils import wins, MODE_VS, MODE_AI, MODE_AI_N

COMP = 1
HUMA = -1
DEFAULT_MAX = -10000 # default value when maximising
DEFAULT_MIN = 10000 # default value when minimising
WIN = 10 # win modifier
LOSE = -10 # lose modifier
def empty_cells(grid):
    empty = []

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == None:
                empty.append([i, j])
    return empty

def evaluate(grid):
    if wins(grid, 'X'):
        return LOSE
    if wins(grid, '0'):
        return WIN
    else:
        return 0

def is_over(grid):
    return wins(grid, 'X') or wins(grid, '0')

def minimax(grid, depth, player, alpha, beta):
    if depth == 0 or is_over(grid):
        return [evaluate(grid), -1, -1]

    best = [DEFAULT_MAX, -1, -1] if player == COMP else [DEFAULT_MIN, -1, -1]

    for c in empty_cells(grid):
        i, j = c[0], c[1]
        grid[i][j] = '0' if player == COMP else 'X'
        score = minimax(grid, depth-1, -player, alpha, beta)
        grid[i][j] = None
        score[1], score[2] = i, j

        if player == COMP:
            if score[0] > best[0]:
                best = score
                alpha = max(best[0], alpha)
        else:
            if score[0] < best[0]:
                best = score
                beta = min(best[0], beta)

        if beta <= alpha:
            return best

    return best

def move(board, mode):
    if(mode == MODE_AI_N):
        move = random.choice(empty_cells(board.grid))
    else:
        move = best_move(board.grid, DEFAULT_MAX, DEFAULT_MIN)

    board.make_move(move[0], move[1])

def best_move(grid, alpha, beta):
    best = minimax(grid, len(empty_cells(grid)), COMP, alpha, beta)
    return (best[1], best[2])
