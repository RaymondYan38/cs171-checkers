import random
import math
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
NUM_SIMULATIONS = 100

class Node:
    def __init__(self, state):
        # Initialize a node with the given game state.
        self.state = state  # Represents the game state
        self.parent = None  # Reference to the parent node
        self.children = []  # List of child nodes
        self.wins = 0  # Number of wins from this node
        self.visits = 0  # Number of visits to this node
        self.unexplored_moves = self.state.get_all_possible_moves()  # Unexplored moves from this node

    def is_fully_expanded(self):
        # Check if all possible moves have been explored from this node.
        return not self.unexplored_moves

    def get_unexplored_move(self):
        # Get an unexplored move from the list.
        if self.unexplored_moves:
            return self.unexplored_moves.pop()
        else:
            return None

    def add_child(self, child_node):
        # Add a child node to this node.
        child_node.parent = self
        self.children.append(child_node)

    def simulate_move(self, move):
        # Simulate applying a move from this node and return the resulting state.
        new_state = self.state.copy()  # Make a copy of the current state
        new_state.make_move(move)
        return new_state

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def selection(self, node):
        # Selection phase using UCT (Upper Confidence Bound for Trees)
        C = 1.0  # Exploration parameter (adjust as needed)
        selected_child = None
        max_uct = -float("inf")

        for child in node.children:
            if child.visits == 0:
                uct_value = float("inf")  # If a node has not been visited, set UCT to infinity
            else:
                exploitation = child.wins / child.visits
                exploration = C * math.sqrt(math.log(node.visits) / child.visits)
                uct_value = exploitation + exploration

            if uct_value > max_uct:
                max_uct = uct_value
                selected_child = child

        return selected_child


    def simulate(self, node):
        # Simulate phase (simplified, assuming random moves)
        current_state = node.state.copy()
    
        while True:
            if current_state.is_game_over():
                result = current_state.is_win(self.color)
                return result

            possible_moves = current_state.get_all_possible_moves(self.color)
            if not possible_moves:
                return 0  # The game is a draw

            random_move = random.choice(possible_moves)
            current_state.make_move(random_move)

    def backpropagate(self, node, result):
    # Backpropagation phase
        while node is not None:
            node.visits += 1
            # Adjust wins based on the result from simulate
            if result == -1:  # Tie
                node.wins += 0  # No win points for a tie
            elif result == 2:  # Your AI ("W") has won
                node.wins += 1  # +1 for a win
            elif result == 1:  # Your AI ("W") has lost
                node.wins -= 1  # -1 for a loss
            node = node.parent


    def choose_best_move(self, node):
        # Choose the best move based on statistics
        best_move = None
        max_win_rate = -float("inf")

        for child in node.children:
            if child.visits > 0:
                win_rate = child.wins / child.visits
                if win_rate > max_win_rate:
                    max_win_rate = win_rate
                    best_move = child.state.get_last_move()
        return best_move

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        # MCTS Algorithm
        root_node = Node(self.board)  # Create a root node representing the current game state

        for _ in range(NUM_SIMULATIONS):
            # Selection phase
            selected_node = self.selection(root_node)

            # Expansion phase
            if not selected_node.is_fully_expanded():
                unexplored_move = selected_node.get_unexplored_move()
                new_state = selected_node.simulate_move(unexplored_move)
                new_node = Node(new_state)
                selected_node.add_child(new_node)

            # Simulation phase
            result = self.simulate(new_node)

            # Backpropagation phase
            self.backpropagate(new_node, result)

        # Decision phase: Choose the best move
        best_move = self.choose_best_move(root_node)

        # Make the selected move
        self.board.make_move(best_move, self.color)

        return best_move
        # moves = self.board.get_all_possible_moves(self.color)
        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        # self.board.make_move(move,self.color)
        # return move
