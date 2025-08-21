import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def get_top(board, col):
            for i in range(5,-1, -1):
                if board[i][col] == 0:
                    return i
            return 10
        def switch_number(player_number):
            if player_number == 1:
                return 2
            else:
                return 1
        def game_completed(board, player_num):
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))
            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False
            def check_verticle(b):
                return check_horizontal(b.T)
            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b 
                    root_diag = np.diagonal(op_board, offset=0).astype(int)
                    if player_win_str in to_str(root_diag):
                        return True
                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(int))
                            if player_win_str in diag:
                                return True
                            return False
                return (check_horizontal(board) or
                    check_verticle(board) or
                    check_diagonal(board))
        def minimax_prune(aiPlayer, board, depth, player_number, maxPlayer, alpha, beta, bestMove):
            all_values = [0, 0, 0, 0, 0, 0, 0]
            if game_completed(board, player_number) == True and maxPlayer == True:
                return (bestMove, aiPlayer.evaluation_function(board), all_values)
            if game_completed(board, player_number) == True and maxPlayer == False:
                return (bestMove, aiPlayer.evaluation_function(board), all_values)
            if depth == 0:
                return (bestMove, aiPlayer.evaluation_function(board), all_values)
            if maxPlayer == True:
                value = 0;
                v = -10000000
                for i in range(0,7):
                    tempBoard = board.copy()
                    top = get_top(tempBoard, i)
                    if top != 10:
                        tempBoard[top][i] = player_number
                        result = minimax_prune(aiPlayer, tempBoard, depth - 1, switch_number(player_number), False, alpha, beta, bestMove)
                        value = result[1]
                        all_values[i] = value
                        if v < value:
                            v = value
                            bestMove = i

                        if v >= beta:
                            break
                        alpha = max(alpha, v)
                    else:
                        if bestMove == i:
                            bestMove = (i + 1) % 7
                    tempBoard = np.zeros([6,7]).astype(np.uint8)
            else:
                v = 10000000
                for i in range(0,7):
                    tempBoard = board.copy()
                    top = get_top(tempBoard, i)
                    if top != 10:
                        tempBoard[top][i] = player_number
                        result = minimax_prune(aiPlayer, tempBoard, depth - 1, switch_number(player_number), True, alpha, beta, bestMove)
                        value = result[1]
                        all_values[i] = value
                        if v > value:
                            v = value
                            bestMove = i
                        if v <= alpha:
                            break
                        beta = min(beta, v)
                    else:
                        if bestMove == i:
                            bestMove = (i + 1) % 7
                        tempBoard = np.zeros([6,7]).astype(np.uint8)
            return (bestMove, v, all_values)
        result_alg = minimax_prune(self, board, 4, self.player_number, True, -10000000, 10000000, 0)
        return result_alg[0]
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        def get_top(board, col):
            for i in range(5,-1, -1):
                if board[i][col] == 0:
                    return i
            return 10
        def switch_number(player_number):
            if player_number == 1:
                return 2
            else:
                return 1
        def game_completed(board, player_num):
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))
            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False
            def check_verticle(b):
                return check_horizontal(b.T)
            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                    root_diag = np.diagonal(op_board, offset=0).astype(int)
                    if player_win_str in to_str(root_diag):
                        return True
                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(int))
                            if player_win_str in diag:
                                return True
                return False
            return (check_horizontal(board) or
            check_verticle(board) or
            check_diagonal(board))
        
        def expectimax(aiPlayer, board, depth, player_number, maxPlayer, alpha, beta, bestMove):
            if game_completed(board, player_number) == True and maxPlayer == True:
                return (bestMove, aiPlayer.evaluation_function(board))
            if game_completed(board, player_number) == True and maxPlayer == False:
                return (bestMove, aiPlayer.evaluation_function(board))
            if depth == 0:
                return (bestMove, aiPlayer.evaluation_function(board))
            if maxPlayer == True:
                value = 0;
                v = -10000000
                for i in range(0,7):
                    tempBoard = board.copy()
                    top = get_top(tempBoard, i)
                    if top != 10:
                        tempBoard[top][i] = player_number
                        result = expectimax(aiPlayer, tempBoard, depth - 1, switch_number(player_number), False, alpha, beta, bestMove)
                        value = result[1]
                        if v < value:
                            v = value
                            bestMove = i
                        if v >= beta:
                            break
                        alpha = max(alpha, v)
                    else:
                        if bestMove == i:
                            bestMove = (i + 1) % 7
                        tempBoard = np.zeros([6,7]).astype(np.uint8)
            else:
                v = 0
                available = 7
                for i in range(0,7):
                    tempBoard = board.copy()
                    top = get_top(tempBoard, i)
                    if top != 10:
                        tempBoard[top][i] = player_number
                        result = expectimax(aiPlayer, tempBoard, depth - 1, switch_number(player_number), True, alpha, beta, bestMove)
                        p = 1 / available
                        value = result[1]
                        v += p * value
                    else:
                        available -= 1
                        if bestMove == i:
                            bestMove = (i + 1) % 7
                    tempBoard = np.zeros([6,7]).astype(np.uint8)
            return (bestMove, v)
        result_alg = expectimax(self, board, 4, self.player_number, True, -10000000, 10000000, 0)
        return result_alg[0]

        raise NotImplementedError('Whoops I don\'t know what to do')

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        def game_completed(board, player_num):
            player_win_str = '{0}{0}{0}{0}'.format(player_num)
            to_str = lambda a: ''.join(a.astype(str))

            def check_horizontal(b):
                for row in b:
                    if player_win_str in to_str(row):
                        return True
                return False
            def check_verticle(b):
                return check_horizontal(b.T)

            def check_diagonal(b):
                for op in [None, np.fliplr]:
                    op_board = op(b) if op else b
                    root_diag = np.diagonal(op_board, offset=0).astype(int)
                    if player_win_str in to_str(root_diag):
                        return True
                    for i in range(1, b.shape[1]-3):
                        for offset in [i, -i]:
                            diag = np.diagonal(op_board, offset=offset)
                            diag = to_str(diag.astype(int))
                            if player_win_str in diag:
                                return True
                return False

            return (check_horizontal(board) or
                    check_verticle(board) or
                    check_diagonal(board))
        
        def switch_number(player_number):
            if player_number == 1:
                return 2
            return 1
        
        def check_out_of_bounds(row, col):
            if row >= 0 and row <= 5 and col >= 0 and col <= 6:
                return True
            return False
        
        def check_around(board, row, col, player_number):
            value = 0
            options = [-1, 0, 1]
            for i in options:
                for j in options:
                    tempRow = row + i
                    tempCol = col + j
                    tempRow2 = col + i + i
                    tempCol2 = col + j + j
                    if check_out_of_bounds(tempRow, tempCol):
                        if board[row][col] == board[tempRow][tempCol]:
                            value += 1
                            if check_out_of_bounds(tempRow2, tempCol2) and check_out_of_bounds(tempRow2 + i, tempCol2 + j):
                                if board[row][col] == board[tempRow2][tempCol2] and board[tempRow2 + i][tempCol2 + j] == 0:
                                    value += 2
                                if board[row][col] == player_number and board[tempRow][tempCol] == 0 and board[row][col] == board[tempRow2][tempCol2] and board[tempRow2 + i][tempCol2 + j] == board[row][col]:
                                    value += 10
            return value
        
        value = 0
        winning = 0
        losing = 0
       
        if game_completed(board, self.player_number) == True:
            winning += 100000
        
        if game_completed(board, switch_number(self.player_number)) == True:
            losing += -1000000
        
        priority = [2, 3, 4]
        for col in range(0,7):
            for row in range(0,6):
                oppo = switch_number(self.player_number)

                if col in priority:
                    if board[5][3] == self.player_number:
                        winning += .2
                    if board[5][3] == oppo:
                        winning -= .2
                    if board[row][col] == self.player_number:
                        winning += .3
                    if board[row][col] == oppo:
                        losing -= .3
                if board[5][col] == self.player_number:
                    winning += .2
                    
                if board[row][col] == self.player_number:
                    winning += check_around(board, row, col, self.player_number)
                
                if board[row][col] == oppo:
                    losing -= check_around(board, row, col, oppo)
                
                if board[5][col] == oppo:
                    losing -= .2
        return winning + losing


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

