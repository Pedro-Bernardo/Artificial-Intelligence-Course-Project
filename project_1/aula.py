#import search
from search import *

class Solitaire(Problem):
    def __init__(self, board):
        self.initial = sol_state(board)
    
    def action(self, state):

    def result(self, state, action):
        # verify if action is valid
        moves = board_moves()

    def goal_test(self, state):
        #checkar se o board so tem uma ball
    
    def h(self, node):
        # node.state -> estado

    """
    definir varios h's e por o h a retornar os h's para testar
    DFS ftw
    """

    """
    # Correr algoritmos de procura

    game = solitaire(board)
    p = InstrumentedProblem(game)

    # tree search é o melhor para o nosso caso
    result = depth_first_tree_search(p)
    result = greedy_best_first_graph_search(p, p.h)
    result = astar_search(p)
    result.solution()
    result.path()
    """