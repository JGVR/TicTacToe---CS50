"""
Tic Tac Toe Player
"""

import math
import copy
import json

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    #determine whose turn it is by counting the amount of moves for each player
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if board[row][cell] == X:
                x_count += 1
            elif board[row][cell] == O:
                o_count += 1
    
    #if X has more moves the it is O turn, otherwise it is X turn
    if x_count > o_count:
        return O
    else: 
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    #loop over board, if a cell is empty, add it to the moves set along with the row
    #this determines those slots are available for X or O
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if board[row][cell] == EMPTY:
                moves.add((row, cell))
    
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #make a deep copy of board
    deep_copy_board = copy.deepcopy(board)

    #check for moves outside the range of the board
    if(action[0] > 2 or action[1] < 0):
        raise Exception("The player made an invalid move.")
    
    #update the deep copy board with the current players action/move
    current_player = player(board)
    deep_copy_board[action[0]][action[1]] = current_player
    return deep_copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check if X or O have 3 in a row: horizontally, vertically or diagonally
    for i in range(3):
        #horizontally
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        
        #vertically
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    #diagonally
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #check if there is a winner
    if winner(board) is not None:
        return True

    #check if there is any open cells, if yes the game is not over,
    #if not, then it is a tie
    if(any(cell is None for row in board for cell in row)):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    current_winner = winner(board)

    if current_winner == X:
        return 1
    elif current_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    #if game over return none
    if terminal(board):
        return None
    
    stack = [board]
    scores = {} #dict of boards containing the board score and the move that led to the score

    #loop over stack
    while len(stack) > 0:
        #peek at stack
        current_board = stack[-1]
        current_json_board = json.dumps(current_board) #parsing to json to make the board hashable

        #get all actions available at current_board
        action_list = actions(current_board)

        are_child_explored = True #will determine if all childs of current_board have been explored
        child_boards = {} #will store the score of the child board, and the action that let to child board

        for action in action_list:
            #apply action to current board and store new board state
            new_board = result(current_board, action)
            json_board = json.dumps(new_board) #parsing to json to make the board hashable

            #check if new_board has already been explored and has a score
            if scores.get(json_board) is not None:
                child_boards[json_board] = (scores[json_board][0], action)
                continue
            else:
                are_child_explored = False

            #check if new_board is a terminal state
            if terminal(new_board):
                #check who is the winner and store the score
                score = utility(new_board)

                #add the board, and the score and action to scores
                scores[json_board] = (score, action)
            else: #if not a terminal state, there are more boards to explore
                stack.append(new_board)
        
        #if all childs have NOT been explored, go to next board in the stack
        if are_child_explored is False:
            continue

        #if all childs have been explored, loop over childs
        for child in child_boards.keys():
            #extract current player
            current_player = player(current_board)

            #check if current_player is maximazer
            if current_player == X:
                #check if current board has been explored and has a score
                if scores.get(current_json_board) is None:
                    scores[current_json_board] = child_boards[child]

                #if child score is > than current_board score
                elif child_boards[child][0] > scores[current_json_board][0]: 
                    scores[current_json_board] = child_boards[child]
            
            #check if current_player is minimazer
            if current_player == O:
                #check if current board has been explored and has a score
                if scores.get(current_json_board) is None:
                    scores[current_json_board] = child_boards[child]

                #if child score is > than current_board score
                elif child_boards[child][0] < scores[current_json_board][0]: 
                    scores[current_json_board] = child_boards[child]
        
        #remove from stack since current_board has now been fully explored
        stack.pop()

    #return optimal move for current board
    return scores[json.dumps(board)][1]