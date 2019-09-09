from utils import wins, MODE_VS, MODE_AI, MODE_AI_N

COMP = 1
HUMA = -1

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
    return wins(grid, 'X') or wins(grid, '0')

def minimax(grid, depth, player):
    if depth == 0 or is_over(grid):
        return [evaluate(grid), -1, -1]

    best = [-10000, -1, -1] if player == COMP else [10000, -1, -1]

    for c in empty_cells(grid):
        i, j = c[0], c[1]
        grid[i][j] = '0' if player == COMP else 'X'
        score = minimax(grid, depth-1, -player)
        grid[i][j] = None
        score[1], score[2] = i, j

        if player == COMP:
            if score[0] > best[0]:
                best = score
        else:
            if score[0] < best[0]:
                best = score

    return best

def move(board, mode):
    if(mode == MODE_AI_N):
        move = random.choice(empty_cells(board.grid))
    else:
        move = best_move(board.grid)

    board.make_move(move[0], move[1])

def best_move(grid):
    best = minimax(grid, len(empty_cells(grid)), COMP)
    return (best[1], best[2])
