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
#         print("Row: " + str(move[len(move)-1][0]))
#         print("Col: " + str(move[len(move)-1][1]))
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
        self.unexplored_moves = self.state.get_all_possible_moves(self.opponent[self.color])  # Unexplored moves from this node (2D list), get moves that opposing player can make, since nodes represent who JUST MOVED
        self.isRootNode = False
        # TEMP self.leaf_visit_count = 0 #3 #It's a counter that decrements every time we select this leaf node, and when it hits 0, expand off this leaf node (since it's not the root too)
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

    def good_move_or_not(self, board,move,color_moving): #Returns True or False if we make a move that's good (doesn't end with a piece next to an opposing king) or not
        move_status = True
        if color_moving == 1:
            opposingKing = 'W'
        else:
            opposingKing = 'B'
        if move[len(move)-1][0] - 1 >= 0 and move[len(move)-1][1] - 1>= 0: #Top left of a ending position, check for opposing king
            #within board, check for king, repeat 4 times
            if board.board[move[len(move)-1][0] - 1 ][move[len(move)-1][1]-1] == opposingKing:
                move_status = False
                return move_status
        if move[len(move)-1][0] - 1 >= 0 and move[len(move)-1][1] + 1 < board.col: #Top right of an ending positon, check for opposing king
            #within board, check for king, repeat 4 times
            if board.board[move[len(move)-1][0] - 1 ][move[len(move)-1][1]+1] == opposingKing:
                move_status = False
                return move_status
            
        if move[len(move)-1][0] + 1 < board.row and move[len(move)-1][1] -1 >= 0: #Bottom left of an ending position, check for opposing king
            #within board, check for king, repeat 4 times
            if board.board[move[len(move)-1][0] + 1 ][move[len(move)-1][1]-1] == opposingKing:
                move_status = False
                return move_status
        if move[len(move)-1][0] + 1 < board.row and move[len(move)-1][1] +1 < board.col: #Bottom right of an ending position, check for opposing king
            #within board, check for king, repeat 4 times
            if board.board[move[len(move)-1][0] + 1 ][move[len(move)-1][1]+1] == opposingKing:
                move_status = False
                return move_status
        return move_status

    def get_child_moves(self, moves): #something is wrong with 'move' / SOMETHING IS WRONG HERE ENTIRELY (EDITED) / Returns nothing, just adds child nodes to current node (the leaf node we selected)
        # Simulate applying a move from this node and FIX: adding a child that represents this new state to this current node(NOT return the resulting state.)
        for m in moves:
            new_state = deepcopy(self.state)  # Make a copy of the current state
            new_state.make_move(m, self.opponent[self.color]) #make said move as the response to our prompt (opponent's move or clean board)
            if self.good_move_or_not(new_state, m, self.opponent[self.color]):
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
        self.treeRoot = None
        self.UCT_C = 1.4 #2.0 #UCT's C value
        self.moveCounter = 0 # increment every time we move the self.treeRoot

    def UCT(self, node): #Runs the UCT calculation and returns child with best UCT value
        # C = 1.0  # Exploration parameter (adjust as needed)
        selected_child = None 
        max_uct = -float("inf") #NEGATIVE Infinity as starting point

        for child in node.children:
            if child.visits == 0:
                uct_value = float("inf")  # If a node has not been visited, set UCT to infinity
            else:
                exploitation = child.wins / child.visits  #QUESTION: I set the color of each node to be whoever is responding to the state given by said node, but what if that's throwing things off in selection and backpropagation
                exploration = self.UCT_C * math.sqrt(math.log(node.visits) / child.visits) #That's the UCT equation
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
            # node.leaf_visit_count -= 1 TEMP
            return node
        else:

            return self.selection(self.UCT(node)) #formerly returned self.selection(selected_child) 

    def MaxVal(self, boardState, movesList):
        if not movesList:
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
    # def simulate(self, node): #REDONE VERSION, score based on number of pieces on both sides
    #     current_state = deepcopy(node.state) #the state of the game is the board itself in the pov of our AI
    #     current_color_response = node.color


    #     number_of_opponent_kings = {2:0, 1:0}
    #     number_of_pieces = {2:0, 1:0}
    #     for row_index in range(current_state.row):
    #         for col_index in range(current_state.col):
    #             if current_state.board[row_index][col_index] == 'W':
    #                 number_of_opponent_kings[2] += 1
    #                 number_of_pieces[2] += 1
    #             if current_state.board[row_index][col_index] == 'B':
    #                 number_of_opponent_kings[1] += 1
    #                 number_of_pieces[1] += 1
        
    #     ourPieces = number_of_opponent_kings[self.color] + number_of_pieces[self.color]
    #     opponentPieces = number_of_opponent_kings[self.opponent[self.color]] + number_of_pieces[self.opponent[self.color]]
    #     return [ourPieces, opponentPieces]
        

# ------------------------- Old Simulate -----------------------------------------------
    def MiniMaxSearch(self,color, board):
        val,move = self.MaxValue(color,board)
        return move
    
    def MaxValue(self,color,board):
        currentBestMove = None
        if board.is_win(color):
            return [board.is_win(color), currentBestMove]
        currentVal = -float("inf")
        for actions in board.get_all_possible_moves(self.opponent[color]):
            for action in actions:
                new_board = deepcopy(board)
                val2, action2 = self.MinValue(self.opponent[color], new_board.make_move(action, self.opponent[color]))
                if val2 > currentVal:
                    currentVal, currentBestMove = val2, action
        return [currentVal, currentBestMove]
    
    def MinValue(self, color, board):
        currentBestMove = None
        if board.is_win(color):
            return [board.is_win(color), currentBestMove]
        currentVal = float("inf")
        for actions in board.get_all_possible_moves(self.opponent[color]):
            for action in actions:
                new_board = deepcopy(board)
                val2, action2 = self.MaxValue(color, new_board.make_move(action, self.opponent[color]))
                if val2 <= currentVal:
                    currentVal, currentBestMove = val2, action
        return [currentVal, currentBestMove]
    
    def simulate(self, node): #returns the result of who won
        # Simulate phase (simplified, assuming random moves)
        current_state = deepcopy(node.state) #the state of the game is the board itself in the pov of our AI
        current_color_response = node.opponent[node.color] # ATTEMPT: trying to see if changing node.opponent[node.color] to just node.color will make a difference, since each node's color is representing who is going next; since the next move is done by the alternating player (either our opponent if the child node we're working with represents a board state that came from our move or vice versa)
        color_that_responded = node.color
        '''
        - The child node we're simulating just did a move for us so we need to start the simulation with opponent's move
        - Similarly, if we're at a child node that did the opponent's move, then start the simulation with our move
        - Using the base code provided, perhaps we can do something about simulating random moves
        '''

        #Minimax style

        m = current_state.get_all_possible_moves(current_color_response) #get all possible moves of the other player than what this child node's represented player was
        # print("outside simulate while loop")
        while len(m) != 0: #while we have possible moves left

            # max capture heuristic--------------------
            index = randint(0,len(m)-1)
            inner_index =  randint(0,len(m[index])-1)
            current_best_move = m[index][inner_index]
            
            for checker_index in range(len(m)):
                for move_index in range(len(m[checker_index])):
                    if len(current_best_move) < len(m[checker_index][move_index]):
                        current_best_move = m[checker_index][move_index]

            current_state.make_move(current_best_move,current_color_response)
            # -------------------------------------------------------
            
            # random move heuristic:
            index = randint(0,len(m)-1)
            inner_index =  randint(0,len(m[index])-1)
            random_move = m[index][inner_index]
            current_state.make_move(random_move,current_color_response)
            # -----------------------------------------------------
                
            current_color_response = node.opponent[current_color_response] #to switch the color for the next turn WITHIN the simulated play
            m = current_state.get_all_possible_moves(current_color_response)
        # If here, then we're out of moves, figure out who won:
        result = current_state.is_win(node.color) #POTENTIAL ISSUE: I have no clue how is_win() really works. Is it just throw in a random color and it'll return who really won?
        return result

# -------------------------- Old Simulate End -----------------------------------------------------------------------

    def backpropagate(self, node, result):
    # Backpropagation phase
        while node is not None:
            node.visits += 1
            
            # Check if your AI (self.color) has won
            if result == node.opponent[node.color]:#result[0] > result[1]: #if result == node.opponent[node.color]: #EDIT: Originally, it was result = self.color, but that increments node.wins of all nodes, whether ours or the opponentss, which throws off the win rates
                node.wins += 1  # Increment wins if your AI has won

                        
            node = node.parent


    def choose_best_move(self, node): # Returns a list [move we're going to make, the node that represents our move]
        # Choose the best move based on statistics
        best_move = None
        best_node = None
        max_win_rate = -float("inf")

        for child in node.children:
            if child.visits > 0:
                win_rate = child.wins / child.visits
                if win_rate > max_win_rate:
                    max_win_rate = win_rate
                    best_move = child.move
                    best_node = child
        return [best_move, best_node]
    
    def monte_carlo_tree_search(self, move_made):
        if self.treeRoot == None:
            self.treeRoot = TreeNode(self.board, move_made, self.opponent[self.color])  # Create a root node representing the current game state 
            #PersonalNote: color represents who's jsut moved to the current state of the board, so that's opponent at the root, 
            # since we're always starting our MCTS as a response to either an unmoved board or our opponent's move
            self.treeRoot.isRootNode = True # A boolean for forcing an expansion on the root, 
            #EDIT: for the sake of trying out professor's idea of not expanding each and every node 
            # until we visit it a few times and adjust its UCT value, but we have to expand the root
        else:
           currentRoot = self.treeRoot
           for c in self.treeRoot.children:
                if c.move == move_made:
                    self.treeRoot = c
                    self.treeRoot.parent = None
                    break
           if currentRoot == self.treeRoot:
                self.treeRoot = TreeNode(self.board, move_made, self.opponent[self.color])
                self.treeRoot.isRootNode = True
        # self.moveCounter += 1 TEMP
        # if self.moveCounter % 10 == 0 and self.UCT_C > 1.0:
        #     self.UCT_C = self.UCT_C - 0.2


        for _ in range(NUM_SIMULATIONS):
            # Selection phase
            selected_node = self.selection(self.treeRoot) #returns the leaf node that we need to expand

            # Expansion phase
            # new_node = None
            # EDIT: removed condition: 'selected_node is not None and' from while loop below 
            while (selected_node.isRootNode == True) or (selected_node is not None and not selected_node.is_fully_expanded()): #and selected_node.leaf_visit_count == 0):
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
                # Simulate all children start
                # --- ALICHA METHOD START ---
                # for timesToSimulate in range(50): #Originally wasn't here, then 10, 
                #     childNode = self.UCT(selected_node)
                #     result = self.simulate(childNode)
                #     self.backpropagate(childNode, result)
                # --- ALICHA METHOD END ---

                # Regular Method ---------
                # childNode = self.UCT(selected_node) # POTENTIAL Or try random picking
                # result = self.simulate(childNode)
                # self.backpropagate(childNode, result)
                # Regular Method end ----------

            # elif selected_node.leaf_visit_count > 0: # in the case of not expanding our selected node, run a simulation on itself
            #     # Alicia Method ------------------
            #     # for timesToSimulate in range(50):
            #     #     result = self.simulate(selected_node)
            #     #     self.backpropagate(selected_node, result)
            #     # ALicia Method End -----------------------

            #     # Regular Method ----------------
            #     result = self.simulate(selected_node)
            #     self.backpropagate(selected_node, result)
                # Regular Method End -------------

            # ------------------------------------------------------#
            # POTENTIAL: The code section below ran a simulation per child, so that might be a huge problem in terms of running time
            for c_node in selected_node.children: #every response/move our current leaf node could've done is simulated with a random move from the alternate player 
                result = self.simulate(c_node)
                self.backpropagate(c_node, result)
            # ----------------------------------------------------- #


        # Decision phase: Choose the best move
        best_move_list = self.choose_best_move(self.treeRoot) # EDIT now returns a list, check function for specifics

        # Make the selected move
        self.board.make_move(best_move_list[0], self.color)
        # TEMP self.moveCounter += 1

        #update root by 1 node (now it's pointing to our move)
        self.treeRoot = best_move_list[1]
        self.treeRoot.parent = None
        # TEMP if self.moveCounter % 10 == 0 and self.UCT_C > 1.0:
        #     self.UCT_C = self.UCT_C - 0.2
        return best_move_list[0]
    

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color]) #If opponent moves first, update our view of the board to match what they just did
        else:
            self.color = 1 #we're player one, we get a board with unmoved pieces and the first move for us to make
        

        #In either case above, we get to respond to some prompt (the board state) whether our opponent was first or not
        return self.monte_carlo_tree_search(move)

'''
Notes:
'''
