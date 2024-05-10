import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)

# Colors
BG_COLOR = (214, 201, 227)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

# Load Images
BOARD = pygame.transform.scale(pygame.image.load("assets/Board.png"), (WIDTH, HEIGHT))
X_IMG = pygame.transform.scale(pygame.image.load("assets/X.png"), (CELL_SIZE, CELL_SIZE))
O_IMG = pygame.transform.scale(pygame.image.load("assets/O.png"), (CELL_SIZE, CELL_SIZE))
WINNING_X_IMG = pygame.transform.scale(pygame.image.load("assets/Winning X.png"), (WIDTH, HEIGHT))
WINNING_O_IMG = pygame.transform.scale(pygame.image.load("assets/Winning O.png"), (WIDTH, HEIGHT))

# Initialize the game
board = [[None, None, None], [None, None, None], [None, None, None]]
to_move = 'X'
game_finished = False

# Initialize Pygame screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (0, 0))
pygame.display.update()

def render_board(board, ximg, oimg):
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == 'X':
                SCREEN.blit(ximg, (j * CELL_SIZE, i * CELL_SIZE))
            elif board[i][j] == 'O':
                SCREEN.blit(oimg, (j * CELL_SIZE, i * CELL_SIZE))

def add_XO(board, move):
    if board[move[0]][move[1]] is None:
        board[move[0]][move[1]] = to_move

    render_board(board, X_IMG, O_IMG)

    pygame.display.update()

def check_win(board):
    for row in range(ROWS):
        if all(board[row][col] == 'X' for col in range(COLS)) or all(board[row][col] == 'O' for col in range(COLS)):
            return True

    for col in range(COLS):
        if all(board[row][col] == 'X' for row in range(ROWS)) or all(board[row][col] == 'O' for row in range(ROWS)):
            return True

    if all(board[i][i] == 'X' for i in range(ROWS)) or all(board[i][i] == 'O' for i in range(ROWS)):
        return True

    if all(board[i][ROWS - 1 - i] == 'X' for i in range(ROWS)) or all(board[i][ROWS - 1 - i] == 'O' for i in range(ROWS)):
        return True

    return False

def ai_move(board):
    while True:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if board[row][col] is None:
            return row, col

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_finished and to_move == 'X':
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if row < ROWS and col < COLS and board[row][col] is None:
                add_XO(board, (row, col))
                if check_win(board):
                    game_finished = True
                to_move = 'O'

        if not game_finished and to_move == 'O':
            row, col = ai_move(board)
            add_XO(board, (row, col))
            if check_win(board):
                game_finished = True
            to_move = 'X'

    if game_finished:
        winner = 'Human' if to_move == 'O' else 'AI'
        font = pygame.font.Font(None, 36)
        text = font.render(f"{winner} is the winner!", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(text, text_rect)
        pygame.display.update()
