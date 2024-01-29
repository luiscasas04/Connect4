# Global constants
numRows = 6
numCols = 7
humanPlayer = 'X'
AIplayer = 'O'

# Prints board updated board
def printBoard(board):
    for row in board:
        print("|" + "|".join(row) + "|")
    print(" 1 2 3 4 5 6 7")

# Gets player's choice
def playerInput(board, player):
    while True:
        column = int(input(f"Player {player}, choose a column (1-7) or 0 to exit: ")) - 1

        if column == -1:
            print("Exiting game.")
            exit(0)

        if not (0 <= column < numCols) or board[0][column] != ' ':
            print("Invalid input. Try again.")
            continue

        for row in range(numRows - 1, -1, -1):
            if board[row][column] == ' ':
                board[row][column] = player
                return

# Checks if the entire board is full (draw)
def checkDraw(board):
    return all(cell != ' ' for cell in board[0])

# Checks if the given player has won (horizontal, vertical & diagonal check)
def checkWin(board, player):
    for i in range(numRows):
        for j in range(numCols):
            # checks horizontal
            if j + 3 < numCols and all(board[i][j + k] == player for k in range(4)):
                return True

            # checks vertical
            if i + 3 < numRows and all(board[i + k][j] == player for k in range(4)):
                return True

            # checks diagonal (from top-left to bottom-right)
            if i + 3 < numRows and j + 3 < numCols and all(board[i + k][j + k] == player for k in range(4)):
                return True

            # checks diagonal (from bottom-left to top-right)
            if i - 3 >= 0 and j + 3 < numCols and all(board[i - k][j + k] == player for k in range(4)):
                return True
    return False

# Provides an evaluation for the AI to make decisions for moves (used in the minimax() function)
def evaluateBoard(board):
    if checkWin(board, AIplayer):
        return 1  # returns 1 if the move favors the AI
    elif checkWin(board, humanPlayer):
        return -1  # returns -1 if the move does not favor the AI
    else:
        return 0  # returns 0 if neither the AI nor the human player has an advantage

# Finds optimal column for the AI to place its choice (uses minimax() function)
def bestAIMove(board, depth):
    bestScore = float('-inf')
    move = -1
    for j in range(numCols):
        if board[0][j] == ' ':
            for i in range(numRows - 1, -1, -1):  # find the first empty row in this column
                if board[i][j] == ' ':
                    # place temporary AI Token and call minimax() to evaluate score
                    board[i][j] = AIplayer
                    tempScore = minimax(board, depth, float('-inf'), float('inf'), False)
                    board[i][j] = ' '  # remove temp AI token
                    if tempScore > bestScore:
                        bestScore = tempScore
                        move = j
                    break
    return move

# Implementation of Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or checkWin(board, AIplayer) or checkWin(board, humanPlayer) or checkDraw(board):
        return evaluateBoard(board)

    if maximizingPlayer:
        maxEvaluatedScore = float('-inf')
        for col in range(numCols):
            if board[0][col] == ' ':
                row = next((r for r, cell in enumerate(board[::-1]) if cell[col] == ' '), None)
                if row is not None:
                    row = numRows - 1 - row
                    board[row][col] = AIplayer
                    evaluatedScore = minimax(board, depth - 1, alpha, beta, False)
                    board[row][col] = ' '
                    maxEvaluatedScore = max(maxEvaluatedScore, evaluatedScore)
                    alpha = max(alpha, evaluatedScore)
                    if beta <= alpha:
                        break
        return maxEvaluatedScore
    else:
        minEvaluatedScore = float('inf')
        for col in range(numCols):
            if board[0][col] == ' ':
                row = next((r for r, cell in enumerate(board[::-1]) if cell[col] == ' '), None)
                if row is not None:
                    row = numRows - 1 - row
                    board[row][col] = humanPlayer
                    evaluatedScore = minimax(board, depth - 1, alpha, beta, True)
                    board[row][col] = ' '
                    minEvaluatedScore = min(minEvaluatedScore, evaluatedScore)
                    beta = min(beta, evaluatedScore)
                    if beta <= alpha:
                        break
        return minEvaluatedScore

# Main driver
def main():
    # Initialize 2D list board
    board = [[' ' for _ in range(numCols)] for _ in range(numRows)]
    currentPlayer = humanPlayer

    # Game loop
    while True:
        printBoard(board)
        if currentPlayer == humanPlayer:  # human's turn
            playerInput(board, currentPlayer)
        else:  # AI's turn
            col = bestAIMove(board, 2)  # calls bestMove() to find the best column for the AI's move
            if col != -1:
                for i in range(numRows - 1, -1, -1):
                    if board[i][col] == ' ':
                        board[i][col] = AIplayer
                        print(f"Player AI chose column {col + 1}")
                        break

        # Check for win or draw
        if checkWin(board, currentPlayer):
            printBoard(board)
            print(f"Player {currentPlayer} wins!")
            break
        elif checkDraw(board):
            printBoard(board)
            print("It's a draw!")
            break

        # Switch players after each turn
        currentPlayer = AIplayer if currentPlayer == humanPlayer else humanPlayer

if __name__ == "__main__":
    main()
