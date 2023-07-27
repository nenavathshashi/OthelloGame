EMPTY, BLACK, WHITE, OUTER = '.', 'B', 'W', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
global board
def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]
def initial_board():
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45] = BLACK,WHITE
    board[54], board[55] =  WHITE,BLACK
    print(board)
    return board

def print_board(board):
    # return board
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep
def is_valid(move):
    return isinstance(move, int) and move in squares()
def opponent(player):
    return BLACK if player is WHITE else WHITE
def make_move(move, player, board):
    print(move,board)
    board[move] = player
    print(board)
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction
def any_legal_move(player, board):
    return any(is_legal(sq, player, board) for sq in squares())

def next_player(board, prev_player):
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None


def get_move(strategy, player, board):
    copy = list(board) # copy the board to prevent cheating
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move


def score(player, board):
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player: mine += 1
        elif piece == opp: theirs += 1
    return mine,theirs

def find_bracket(square, player, board, direction):
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket



def is_legal(move, player, board):
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))




def legal_moves(player, board):
    legalMovesList=[sq for sq in squares() if is_legal(sq, player, board)]
    return legalMovesList



SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]




import random
def random_strategy(player, board):
    print(print_board(board))
    return random.choice(legal_moves(player, board))

def human_strategy(player,board):
    print(print_board(board))
    print(legal_moves(player,board))
    user=int(input("Enter your choice"))
    return user



def weighted_score(player, board):
    opp = opponent(player)
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total
def maximizer(evaluate):
    def strategy(player, board):
        def score_move(move):
            return evaluate(player, make_move(move, player, list(board)))
        return max(legal_moves(player, board), key=score_move)
    return strategy(player,board)






def minimax(player, board, depth, evaluate):
    def value(board):
        return -minimax(opponent(player), board, depth-1, evaluate)[0]
    if depth == 0:
        return evaluate(player, board), None
    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board), None
    return max((value(make_move(m, player, list(board))), m) for m in moves)
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE
def final_value(player, board):
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

def minimax_searcher(depth, evaluate,board,player):
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy(player,board)



def alphabeta(player, board, alpha, beta, depth, evaluate):

    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move
def alphabeta_searcher(depth, evaluate,board,player):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]
    return strategy(player,board)