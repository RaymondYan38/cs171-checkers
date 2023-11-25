from random import randint
from BoardClasses import Move
from BoardClasses import Board
from copy import deepcopy
import sys
import math
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
# class StudentAI():

#     def __init__(self,col,row,p):
#         self.col = col
#         self.row = row
#         self.p = p
#         self.board = Board(col,row,p)
#         self.board.initialize_game()
#         self.color = ''
#         self.opponent = {1:2,2:1}
#         self.color = 2
#     def get_move(self,move):
        
#         if len(move) != 0:
#             self.board.make_move(move,self.opponent[self.color])
#         else:
#             self.color = 1
#         moves = self.board.get_all_possible_moves(self.color) #This is a 2D list, first dimension is the checker that can be moved, 2nd dimension is a list of Move objects which represent possible moves for the checker that can move I THINK
#         index = randint(0,len(moves)-1)
#         inner_index =  randint(0,len(moves[index])-1)
#         move = moves[index][inner_index] #according to EdDiscussion, I find a random checker to move (represented by "index") and "inner_index" is a random move that random checker can make
#         self.board.make_move(move,self.color)
#         return move #Move Object that AI will return to make a move
# -------------- MIN-MAX ---------------------------------------

# class StudentAI():

#     def __init__(self,col,row,p):
#         self.col = col
#         self.row = row
#         self.p = p
#         self.board = Board(col,row,p)
#         self.board.initialize_game()
#         self.color = ''
#         self.opponent = {1:2,2:1}
#         self.color = 2

#     def MaxVal(self, boardState, movesList):
#         if not movesList:
#             return
#         else:
#             #we have possible moves
#             util = -float("inf") #negative utility
#             considered_move = None
#             for checker in movesList:
#                 for m in checker:
#                     util_2 = len(m)
#                     if util_2 > util:
#                         util = util_2
#                         considered_move = m
#             return considered_move
        
#     def get_move(self,move):
        
#         if len(move) != 0:
#             self.board.make_move(move,self.opponent[self.color])
#         else:
#             self.color = 1
#         moves = self.board.get_all_possible_moves(self.color) #This is a 2D list, first dimension is the checker that can be moved, 2nd dimension is a list of Move objects which represent possible moves for the checker that can move I THINK
#         # index = randint(0,len(moves)-1)
#         # inner_index =  randint(0,len(moves[index])-1)
#         move = self.MaxVal(self.board, moves)#moves[index][inner_index] #according to EdDiscussion, I find a random checker to move (represented by "index") and "inner_index" is a random move that random checker can make
#         self.board.make_move(move,self.color)
        # return move #Move Object that AI will return to make a move
#--------------------------------------------------------------

#-------------------------------------------------------------
#---------------- MONTE CARLO TREE SEARCH --------------------
# NUM_SIMULATIONS = 100

# class TreeNode:
#     def __init__(self, state, move, color):
#         # Initialize a node with the given game state.
#         self.state = state  # Represents the game state (current state of the checker's board)
#         self.move = move  # Store the move that led to this node
#         self.parent = None  # Reference to the parent node
#         self.children = []  # List of child nodes
#         self.wins = 0  # Number of wins from this node
#         self.visits = 0  # Number of visits to this node
#         self.color = color # Color of the pieces we're working with (the player we're currently simulating, either ourselves or the opponent)
#         self.opponent = {1:2,2:1} #To get opponent color info
#         self.unexplored_moves = self.state.get_all_possible_moves(self.color)  # Unexplored moves from this node (2D list)

#     def is_fully_expanded(self):
#         # Check if all possible moves have been explored from this node.
#         return not self.unexplored_moves #True if self.unexplored_moves is empty, False if there are moves left

#     def get_unexplored_move(self):
#         # Get an unexplored set of moves from the 2D list of [checkers#[Move Objects]].
#         if self.unexplored_moves:
#             return self.unexplored_moves.pop() #could have 1 move, could have multiple moves, all for 1 checker 
#         else:
#             return None

#     def add_child(self, child_node):
#         # Add a child node to this node.
#         child_node.parent = self
#         self.children.append(child_node)

#     def get_child_moves(self, moves): #something is wrong with 'move' / SOMETHING IS WRONG HERE ENTIRELY (EDITED) / Returns nothing, just adds child nodes to current node (the leaf node we selected)
#         # Simulate applying a move from this node and FIX: adding a child that represents this new state to this current node(NOT return the resulting state.)
#         for m in moves:
#             new_state = deepcopy(self.state)  # Make a copy of the current state
#             new_state.make_move(m, self.color) #make said move as the response to our prompt (opponent's move or clean board)
#             self.add_child(TreeNode(new_state, m, self.opponent[self.color]))

# class StudentAI():

#     def __init__(self, col, row, p):
#         self.col = col
#         self.row = row
#         self.p = p
#         self.board = Board(col,row,p)
#         self.board.initialize_game()
#         self.color = ''
#         self.opponent = {1:2,2:1}
#         self.color = 2
    

#     def selection(self, node): #Returns a TreeNode that represents the leaf node
#         # Selection phase using UCT (Upper Confidence Bound for Trees)
#         if len(node.children) == 0:
#             #should be at a leaf node
#             return node
#         else:
#             C = 0.5 #1.0  # Exploration parameter (adjust as needed)
#             selected_child = None 
#             max_uct = -float("inf") #NEGATIVE Infinity as starting point

#             for child in node.children:
#                 if child.visits == 0:
#                     uct_value = float("inf")  # If a node has not been visited, set UCT to infinity
#                 else:
#                     exploitation = child.wins / child.visits 
#                     exploration = C * math.sqrt(math.log(node.visits) / child.visits) #That's the UCT equation
#                     uct_value = exploitation + exploration

#                 if uct_value > max_uct:
#                     max_uct = uct_value
#                     selected_child = child

#             return self.selection(selected_child) 


#     def simulate(self, node): #returns the result of who won
#         # Simulate phase (simplified, assuming random moves)
#         current_state = deepcopy(node.state) #the state of the game is the board itself in the pov of our AI
#         current_color_response = node.opponent[node.color] #since the next move is done by the alternating player (either our opponent if the child node we're working with represents a board state that came from our move or vice versa)
#         '''
#         - The child node we're simulating just did a move for us so we need to start the simulation with opponent's move
#         - Similarly, if we're at a child node that did the opponent's move, then start the simulation with our move
#         - Using the base code provided, perhaps we can do something about simulating random moves
#         '''
#         m = current_state.get_all_possible_moves(current_color_response) #get all possible moves of the other player than what this child node's represented player was
#         while len(m) != 0: #while we have possible moves left

#             index = randint(0,len(m)-1)
#             inner_index =  randint(0,len(m[index])-1)
#             random_move = m[index][inner_index]
#             current_state.make_move(random_move,current_color_response)
            
#             current_color_response = node.opponent[current_color_response] #to switch the color for the next turn WITHIN the simulated play
#             m = current_state.get_all_possible_moves(current_color_response)
#         # If here, then we're out of moves, figure out who won:
#         result = current_state.is_win(node.color) #POTENTIAL ISSUE: I have no clue how is_win() really works. Is it just throw in a random color and it'll return who really won?
#         return result

#         #---------------COMMENT OUT---------------------#
#         # while True:
#         #     if current_state.is_game_over():
#         #         result = current_state.is_win(self.color)
#         #         return result

#         #     possible_moves = current_state.get_all_possible_moves(self.color)
#         #     if not possible_moves:
#         #         return -1  # The game is a draw

#         #     random_move = random.choice(possible_moves)
#         #     current_state.make_move(random_move)
#         #---------------COMMENT OUT ABOVE---------------------#

#     def backpropagate(self, node, result):
#     # Backpropagation phase
#         while node is not None:
#             node.visits += 1
            
#             # Check if your AI (self.color) has won
#             if result == self.color:
#                 node.wins += 1  # Increment wins if your AI has won

#             #--------------COMMENT OUT----------------#
#             # Check if your AI (self.color) has lost FIX: If we lost, then don't decrement wins, since if we start from 1 win/ 1 simulation, then do another simulation but lost, then it would be 1 win / 2 simulations
#             # if result == self.opponent[self.color]:
#             #     node.wins -= 1  # Decrement wins if your AI has lost POTENTIAL ISSUE: what if we hit negatives for a node? we're never selecting this node again, but there's potential that this could be the winning node, we just never gave it a chance to be explored 
#             #-----------COMMENT OUT ABOVE-------------#

            
#             node = node.parent


#     def choose_best_move(self, node):
#         # Choose the best move based on statistics
#         best_move = None
#         max_win_rate = -float("inf")

#         for child in node.children:
#             if child.visits > 0:
#                 win_rate = child.wins / child.visits
#                 if win_rate > max_win_rate:
#                     max_win_rate = win_rate
#                     best_move = child.move
#         return best_move
    
#     def monte_carlo_tree_search(self, move_made):
#         root_node = TreeNode(self.board, move_made, self.color)  # Create a root node representing the current game state 
#         #PersonalNote: color represents who's responding to the current state of the board, so that's us at the root, 
#         # since we're always starting our MCTS as a response to either an unmoved board or our opponent's move


#         for _ in range(NUM_SIMULATIONS):
#             # Selection phase
#             selected_node = self.selection(root_node) #returns the leaf node that we need to expand

#             # Expansion phase
#             # new_node = None
#             while selected_node is not None and not selected_node.is_fully_expanded(): #if the leaf node isn't None, and hasn't been fully expanded (replace with while loop maybe, but same conditions to get all children = future next moves)
                
#                 unexplored_moves = selected_node.get_unexplored_move() #get a move from list of available moves (need to repeat probably, but that functionality hasn't been confirmed to be needed yet so not yet made)
#                 selected_node.get_child_moves(unexplored_moves) #ASSUMPTION, move objects affect the board once put into make_move, returns a new board showing the new move made (not official move in the game yet, just a potential move), EDIT: took out new_state, since I made this function not return anything
#                 # new_node = TreeNode(new_state, unexplored_move, self.color)
#                 # selected_node.add_child(new_node) <- and ^ are done in simulate_moves()

#             # Simulation phase
#             # if new_node is not None:
#             for c_node in selected_node.children: #every response/move our current leaf node could've done is simulated with a random move from the alternate player 
#                 result = self.simulate(c_node)
#                 self.backpropagate(c_node, result)

#         # Decision phase: Choose the best move
#         best_move = self.choose_best_move(root_node)

#         # Make the selected move
#         self.board.make_move(best_move, self.color)

#         return best_move
    

#     def get_move(self, move):
#         if len(move) != 0:
#             self.board.make_move(move,self.opponent[self.color]) #If opponent moves first, update our view of the board to match what they just did
#         else:
#             self.color = 1 #we're player one, we get a board with unmoved pieces and the first move for us to make
        

#         #In either case above, we get to respond to some prompt (the board state) whether our opponent was first or not
#         return self.monte_carlo_tree_search(move)

#         # This is the old code that was provided that just made a random move:
#         # moves = self.board.get_all_possible_moves(self.color)
#         # index = randint(0,len(moves)-1)
#         # inner_index =  randint(0,len(moves[index])-1)
#         # move = moves[index][inner_index]
#         # self.board.make_move(move,self.color)
#         # return move


# '''
# NOTES:
# - Selection:
# - at the start, I guess there's no simulations done yet, so parent's total number of simulations is 0 (s_p = 0)
# - done recursively, where I call the selection function again and again on the child with highest UCT score until leaf node is reached (no children? perhaps a different indicator is needed?)

# - Expansion:
# - Create more nodes (I guess use the get all possible moves function given to us)

# - Simulation:
# - Play the game til someone wins

# - Backpropagation:
# - Send info about who won back up the tree thru parent pointers/variables

# - CURRENT STATE OF AFFAIRS:
# - MCTS works, but rather slow (little over 7 mins for a single game)


# Keywords: Ctrl-f to find these
# ASSUMPTION: what I assume is going on, so I could be very wrong or super general
# POTENTIAL ISSUE: down the line of execution, what I predict to cause problems
# FIX: A plan I have to fix what I find to be an issue
# EDIT/EDITED: I changed the code (usually goes with FIX, but might not, so don't count on these 2 being together)
# COMMENT OUT/COMMENT OUT ABOVE: I thought the code was unneeded

# TIME with MCTS (AND C VALUE):
# - ITERATIONS: 
# 100, ~2 mins, little over (2:13) (C = 1)
# 1000, ~7 mins, little over (7:12) (C = 1)
# 1000 (100 games), ~3 hours (47/100) (C = 1)
# 100 ~40 seconds, little over (43.51 s) (C=0.5)
# 100 (100 games) ~2 hours, (34/100) (C = 0.5) 
# '''






'''
Side Notes:
MCTS shouldn't take that long, make sure we run thru overview of MCTS and compare with code
MCTS 1 Simulation per iteration (tentative, suggested by professor) (So if X = 1000, then only 1000 simulations)
MCTS don't always expand
MCTS take average of simulations if we simulate multiple times
'''

#---------------- MONTE CARLO TREE SEARCH REDONE--------------------
NUM_SIMULATIONS = 1000

class TreeNode:
    def __init__(self, state, move, color):
        # Initialize a node with the given game state.
        self.state = state  # Represents the game state (current state of the checker's board)
        self.move = move  # Store the move that led to this node
        self.parent = None  # Reference to the parent node
        self.children = []  # List of child nodes
        self.wins = 0  # Number of wins from this node
        self.visits = 0  # Number of visits to this node
        self.color = color # Color of the pieces we're working with (the player we're currently simulating, either ourselves or the opponent)
        self.opponent = {1:2,2:1} #To get opponent color info
        self.unexplored_moves = self.state.get_all_possible_moves(self.color)  # Unexplored moves from this node (2D list)
        self.isRootNode = False
        self.leaf_visit_count = 3 #It's a counter that decrements every time we select this leaf node, and when it hits 0, expand off this leaf node (since it's not the root too)
        self.uct_value = float("inf")

    def is_fully_expanded(self):
        # Check if all possible moves have been explored from this node.
        return not self.unexplored_moves #True if self.unexplored_moves is empty, False if there are moves left

    def get_unexplored_move(self):
        # Get an unexplored set of moves from the 2D list of [checkers#[Move Objects]].
        if self.unexplored_moves:
            return self.unexplored_moves.pop() #could have 1 move, could have multiple moves, all for 1 checker 
        else:
            return None

    def add_child(self, child_node):
        # Add a child node to this node.
        child_node.parent = self
        self.children.append(child_node)

    def get_child_moves(self, moves): #something is wrong with 'move' / SOMETHING IS WRONG HERE ENTIRELY (EDITED) / Returns nothing, just adds child nodes to current node (the leaf node we selected)
        # Simulate applying a move from this node and FIX: adding a child that represents this new state to this current node(NOT return the resulting state.)
        for m in moves:
            new_state = deepcopy(self.state)  # Make a copy of the current state
            new_state.make_move(m, self.color) #make said move as the response to our prompt (opponent's move or clean board)
            self.add_child(TreeNode(new_state, m, self.opponent[self.color]))

class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2 #will be 1 if we're player 1

    def MaxVal(self, movesList):
        if not movesList: # we have no moves at this point
            return
        else:
            #we have possible moves
            util = -float("inf") #negative utility
            considered_move = None
            for checker in movesList:
                for m in checker:
                    util_2 = len(m)
                    if util_2 > util:
                        util = util_2
                        considered_move = m
            return considered_move

    def UCT(self, node): #Runs the UCT calculation and returns child with best UCT value
        C = 1.0  # Exploration parameter (adjust as needed)
        selected_child = None 
        max_uct = -float("inf") #NEGATIVE Infinity as starting point

        for child in node.children:
            if child.visits == 0:
                uct_value = float("inf")  # If a node has not been visited, set UCT to infinity
            else:
                exploitation = child.wins / child.visits 
                exploration = C * math.sqrt(math.log(node.visits) / child.visits) #That's the UCT equation
                uct_value = exploitation + exploration
                child.uct_value = uct_value

            if uct_value > max_uct:
                max_uct = uct_value
                selected_child = child
        return selected_child
    

    def selection(self, node): #Returns a TreeNode that represents the leaf node
        # Selection phase using UCT (Upper Confidence Bound for Trees)
        if len(node.children) == 0:
            #should be at a leaf node
            node.leaf_visit_count -= 1
            return node
        else:

            return self.selection(self.UCT(node)) #formerly returned self.selection(selected_child) 


    def simulate(self, node): #returns the result of who won
        # Simulate phase (simplified, assuming random moves)
        current_state = deepcopy(node.state) #the state of the game is the board itself in the pov of our AI
        current_color_response = node.opponent[node.color] #since the next move is done by the alternating player (either our opponent if the child node we're working with represents a board state that came from our move or vice versa)
        '''
        - The child node we're simulating just did a move for us so we need to start the simulation with opponent's move
        - Similarly, if we're at a child node that did the opponent's move, then start the simulation with our move
        - Using the base code provided, perhaps we can do something about simulating random moves
        '''
        m = current_state.get_all_possible_moves(current_color_response) #get all possible moves of the other player than what this child node's represented player was
        while len(m) != 0: #while we have possible moves left

            index = randint(0,len(m)-1)
            inner_index =  randint(0,len(m[index])-1)
            #maxCapMove = self.MaxVal(m)
            random_move = m[index][inner_index]
            current_state.make_move(random_move,current_color_response)
            
            # if maxCapMove == None:
                # break
            #current_state.make_move(maxCapMove, current_color_response)
            
            current_color_response = node.opponent[current_color_response] #to switch the color for the next turn WITHIN the simulated play
            m = current_state.get_all_possible_moves(current_color_response)
        # If here, then we're out of moves, figure out who won:
        result = current_state.is_win(node.color) #POTENTIAL ISSUE: I have no clue how is_win() really works. Is it just throw in a random color and it'll return who really won?
        return result

    def backpropagate(self, node, result):
    # Backpropagation phase
        while node is not None:
            node.visits += 1
            
            # Check if your AI (self.color) has won
            if result == node.color: #EDIT: Originally, it was result = self.color, but that increments node.wins of all nodes, whether ours or the opponentss, which throws off the win rates
                node.wins += 1  # Increment wins if your AI has won

                        
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
                    best_move = child.move
        return best_move
    
    def monte_carlo_tree_search(self, move_made):
        root_node = TreeNode(self.board, move_made, self.color)  # Create a root node representing the current game state 
        #PersonalNote: color represents who's responding to the current state of the board, so that's us at the root, 
        # since we're always starting our MCTS as a response to either an unmoved board or our opponent's move
        root_node.isRootNode = True # A boolean for forcing an expansion on the root, 
        #EDIT: for the sake of trying out professor's idea of not expanding each and every node 
        # until we visit it a few times and adjust its UCT value, but we have to expand the root
        



        for _ in range(NUM_SIMULATIONS):
            # Selection phase
            selected_node = self.selection(root_node) #returns the leaf node that we need to expand

            # Expansion phase
            # new_node = None
            # EDIT: removed condition: 'selected_node is not None and' from while loop below 
            while (selected_node.isRootNode == True) or (selected_node is not None and not selected_node.is_fully_expanded() and selected_node.leaf_visit_count == 0):
                '''
                Expand this current leaf node if it's the root node (first iteration of MCTS) 
                or if we're at an actual leaf node, make sure it still has move choices to make
                children of (not selected_node.is_fully_expanded()) and the times we've visited this node is sufficient
                (selected_node.leaf_visit_count == 0)
                '''
                
                
                unexplored_moves = selected_node.get_unexplored_move() #get a move from list of available moves (need to repeat probably, but that functionality hasn't been confirmed to be needed yet so not yet made)
                if unexplored_moves != None:
                    selected_node.get_child_moves(unexplored_moves) #ASSUMPTION, move objects affect the board once put into make_move, returns a new board showing the new move made (not official move in the game yet, just a potential move), EDIT: took out new_state, since I made this function not return anything
                if selected_node.is_fully_expanded():
                    break

            # Simulation phase
            '''
            Only run a single simulation (either going to be a leaf node that's revisited over and over since
            it hasn't been expanded yet OR it's going to be some random child we made from the expansion phase)
            '''
            if selected_node.is_fully_expanded() and len(selected_node.children) != 0: # in the case of having expanded our selected_node, run a simulation on one of its children
                '''
                Pick a random child of this current node to run a simulation from
                '''
                childNode = self.UCT(selected_node)
                result = self.simulate(childNode)
                self.backpropagate(childNode, result)
            elif selected_node.leaf_visit_count > 0: # in the case of not expanding our selected node, run a simulation on itself
                result = self.simulate(selected_node)
                self.backpropagate(selected_node, result)
            # ------------------------------------------------------#
            # FIX: The code section below ran a simulation per child, so that might be a huge problem in terms of running time
            # for c_node in selected_node.children: #every response/move our current leaf node could've done is simulated with a random move from the alternate player 
            #     result = self.simulate(c_node)
            #     self.backpropagate(c_node, result)
            # ----------------------------------------------------- #


        # Decision phase: Choose the best move
        best_move = self.choose_best_move(root_node)

        # Make the selected move
        self.board.make_move(best_move, self.color)

        return best_move
    

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color]) #If opponent moves first, update our view of the board to match what they just did
        else:
            self.color = 1 #we're player one, we get a board with unmoved pieces and the first move for us to make
        

        #In either case above, we get to respond to some prompt (the board state) whether our opponent was first or not
        return self.monte_carlo_tree_search(move)

        # This is the old code that was provided that just made a random move:
        # moves = self.board.get_all_possible_moves(self.color)
        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        # self.board.make_move(move,self.color)
        # return move

'''
Notes:
'''
