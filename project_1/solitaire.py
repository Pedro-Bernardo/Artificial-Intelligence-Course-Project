#!/usr/bin/env python3
from search import *
from utils import *
from copy import *

# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1]


# TAI pos
# Tuplo (l, c)
def  make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1]


# TAI content
def c_peg ():
    return "O"
def c_empty ():
    return "_"
def c_blocked ():
    return "X"
def is_empty (e):
    return e == c_empty()
def is_peg (e):
    return e == c_peg()
def is_blocked (e):
    return e == c_blocked()

def get_h_move(board, pos):
    moves = []
    l = pos_l(pos)
    c = pos_c(pos)
    left = board[l][c - 2:c]
    right = board[l][c + 1:c + 3]

    # if there are 2 slots left, look left
    if len(left) == 2:
        if is_peg(left[1]) and is_empty(left[0]):
            moves += [make_move(pos, make_pos(l, c - 2))]

    # if there are 2 slots right, look right
    if len(right) == 2:
        if is_peg(right[0]) and is_empty(right[1]):
            moves += [make_move(pos, make_pos(l, c + 2))]

    return moves

def get_v_move(board, pos):
    moves = []
    l = pos_l(pos)
    c = pos_c(pos)

    # if there are 2 slots up, look upwards
    if l > 1:
        if is_peg(board[l - 1][c]) and is_empty(board[l - 2][c]):
            moves += [make_move(pos, make_pos(l - 2, c))]

    # if there are 2 slots down, look downwards
    if l < len(board) - 2:
        if is_peg(board[l + 1][c]) and is_empty(board[l + 2][c]):
            moves += [make_move(pos, make_pos(l + 2, c ))]

    return moves
    
def board_moves(board):
    """
    Naive approach
    """

        
    move_list = []
    n_lines = len(board)
    n_cols = len(board[0])

    for line in range(n_lines):
        for column in range(n_cols):
            if is_peg(board[line][column]):
                move_list += get_h_move(board, make_pos(line, column))
                move_list += get_v_move(board, make_pos(line, column))

    return move_list;

def get_middle_pos(board, move):
        i_l = pos_l(move_initial(move))
        i_c = pos_c(move_initial(move))
        f_l = pos_l(move_final(move))
        f_c = pos_c(move_final(move))
        
        return make_pos(i_l + (f_l - i_l)//2, i_c + (f_c - i_c)//2)


def board_perform_move(board, move):
    local_board = deepcopy(board)
    mid_pos = get_middle_pos(board, move)
    
    local_board[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
    local_board[pos_l(mid_pos)][pos_c(mid_pos)] = c_empty()
    local_board[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()

    return local_board

def verify_move(board, move):
    middle = get_middle_pos(board, move)
    
    return (is_peg(board[pos_l(move_initial(move))][pos_c(move_initial(move))]) 
            and is_peg(board[pos_l(middle)][pos_c(middle)]) 
            and is_empty(board[pos_l(move_final(move))][pos_c(move_final(move))]))


class sol_state:
    def __init__(self, board):
        self.board = board
        self.n_peg = 0
        self.n_moves = 0

        for line in board:
            for column in line:
                if is_peg(column):
                    self.n_peg += 1
                    self.n_moves += len(get_h_move(board, make_pos(line, column)))
                    self.n_moves += len(get_v_move(board, make_pos(line, column)))
                

    def __lt__(self, other):    
        return True
    
    def get_board(self):
        return self.board

    def n_pegs(self):
        return self.n_peg

    def get_n_moves(self):
        return self.n_moves;


class Solitaire(Problem):
    """Models a Solitaire problem as a satisfaction problem.
        A solution cannot have more than 1 peg left on the board."""
    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):
        return board_moves(state.get_board())

        """
        # estudar yield
        if len(moves) > enorme:
            yield from moves
        """

    def result(self, state, action):
        if verify_move(state.get_board(), action):
            return sol_state(board_perform_move(state.get_board(), action))
           

        
    def goal_test(self, state):
        if state.n_pegs() == 1:
            return True
        
    def h(self, node):
        """Needed for informed search."""
        return self.h1(node);
    
    def h1(self, node):
        return  node.state.get_n_moves() / node.state.n_pegs();


def Main():
    board = [["O","O","O","X"],
       ["O","O","O","O"],
       ["O","_","O","O"],
       ["O","O","O","O"]]

    game = Solitaire(board)
    p = InstrumentedProblem(game)

    # tree search é o melhor para o nosso caso
    result = depth_first_tree_search(p)
    result = greedy_best_first_graph_search(p, p.h)
    result = astar_search(p)
    print(result.solution())
    #print(result.path())

if __name__ == "__main__":
    Main()
