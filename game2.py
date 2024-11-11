import numpy as np
import random
import pygame
import sys
import math

# Colors and constants
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

# GA parameters
POPULATION_SIZE = 10
MUTATION_PROBABILITY = 0.1
CROSSOVER_PROBABILITY = 0.7
GENERATION_LIMIT = 50

# Game functions
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

# GA Chromosome Class
class Chromosome:
    def __init__(self, moves=None):
        if moves is None:
            self.moves = [random.randint(0, COLUMN_COUNT - 1) for _ in range(ROW_COUNT)]
        else:
            self.moves = moves
        self.fitness = 0
    
    def evaluate_fitness(self, board):
        for move in self.moves:
            if is_valid_location(board, move):
                row = get_next_open_row(board, move)
                drop_piece(board, row, move, AI_PIECE)
        self.fitness = score_position(board, AI_PIECE)
        return self.fitness

def evaluate_window(window, piece, opponent_piece):
    score = 0

    if window.count(piece) == 4:
        score += 100  # Winning configuration
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5  # Three pieces with one open spot
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2  # Two pieces with two open spots

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4  # Block opponent's winning configuration

    return score

def score_position(board, piece):
    score = 0
    opponent_piece = 1 if piece == 2 else 2  # Assuming pieces are represented as 1 and 2

    # Score center column for priority in the middle
    center_array = [board[i][COLUMN_COUNT // 2] for i in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3  # Center column has higher score for control

    # Score horizontal sequences
    for r in range(ROW_COUNT):
        row_array = [board[r][c] for c in range(COLUMN_COUNT)]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece, opponent_piece)

    # Score vertical sequences
    for c in range(COLUMN_COUNT):
        col_array = [board[r][c] for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece, opponent_piece)

    # Score positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

    # Score negatively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece, opponent_piece)

    return score


def select_parents(population):
    total_fitness = sum(chromo.fitness for chromo in population)
    selection_probs = [chromo.fitness / total_fitness for chromo in population]
    return random.choices(population, weights=selection_probs, k=2)

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROBABILITY:
        cross_point = random.randint(1, ROW_COUNT - 1)
        child1_moves = parent1.moves[:cross_point] + parent2.moves[cross_point:]
        child2_moves = parent2.moves[:cross_point] + parent1.moves[cross_point:]
    else:
        child1_moves, child2_moves = parent1.moves, parent2.moves
    return Chromosome(child1_moves), Chromosome(child2_moves)

def mutate(chromosome):
    if random.random() < MUTATION_PROBABILITY:
        mutation_point = random.randint(0, ROW_COUNT - 1)
        chromosome.moves[mutation_point] = random.randint(0, COLUMN_COUNT - 1)

def genetic_algorithm(board):
    population = [Chromosome() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATION_LIMIT):
        for chromo in population:
            temp_board = board.copy()
            chromo.evaluate_fitness(temp_board)
        
        population.sort(key=lambda x: x.fitness, reverse=True)
        
        new_population = population[:2]  # Elitism: carry best two
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        
        population = new_population
    
    best_chromosome = max(population, key=lambda x: x.fitness)
    for move in best_chromosome.moves:
        if is_valid_location(board, move):
            return move  # Return the best move from GA

# Pygame code setup
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
turn = random.randint(PLAYER, AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        col = genetic_algorithm(board)  # Call GA to get the best move

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
