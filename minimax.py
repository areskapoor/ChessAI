from chessFuncs import *
from evaluation import *
from chessPieces import *

def makeMinimaxMove(app,whiteTeam,depth,aiTeam):
    
    bestScore = 100000
    alpha = 100000
    beta = -100000
    bestMoveRow,bestMoveCol = 1,1 

    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if piece != False and piece.team == aiTeam:
                findPossibleMoves(app,piece,False)
                for (moveRow,moveCol) in app.currentLegalMoves:
                    #saves cur instance of board
                    curBoard = copy.deepcopy(app.board)
                    check = app.check
                    checkmate = app.checkmate

                    moveToSelection(app,row,col,moveRow,moveCol) #row and col are start row and col of piece

                    moveScore = minimax(app,not whiteTeam,alpha,beta,depth)
                    print('score:',moveScore)
                    printBoard(app)

                    newLoc = False
                    app.pieceSelected = False
                    app.board = curBoard #reset board
                    app.checkmate = checkmate
                    app.check = app.check

                    if moveScore < bestScore: #finds best move at cur pos
                        bestPieceRow,bestPieceCol = row,col
                        bestMoveRow,bestMoveCol = moveRow,moveCol
                        bestScore = moveScore

    bestPiece = app.board[bestPieceRow][bestPieceCol]
    print('best score:',bestScore)

    #make the best move
    moveToSelection(app,bestPieceRow,bestPieceCol,bestMoveRow,bestMoveCol)
    
    # app.board = curBoard
    app.aiMoving = False

def minimax(app,isMax,alpha,beta,depth): #board just pieces so can be found w app
    score = evaluate(app)

    if score >= 7500: #if maximizer captured opponents King
        return score

    elif score <= -7500: #if minimizer captured opponents King
        return score

    elif depth <= 0:
        # printBoard(app)
        return score

    if isMax:
        team = 'white'
        best = -100000
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                piece = app.board[row][col]
                if piece != False and piece.team == team:
                    findPossibleMoves(app,piece,False)
                    # print(app.currentLegalMoves)
                    # print(piece.name,'pos:',piece.row,piece.col)
                    for (moveRow,moveCol) in app.currentLegalMoves:
                        #saving current instance of board
                        curBoard = copy.deepcopy(app.board)
                        check = app.check
                        checkmate = app.checkmate
                        app.teamTurn = team
                        
                        if isinstance(app.board[moveRow][moveCol],King):
                            app.board = curBoard 
                            newLoc = False
                            app.pieceSelected = False
                            app.checkmate = checkmate
                            app.check = app.check
                            app.teamTurn = team
                            return score

                        moveToSelection(app,row,col,moveRow,moveCol)
                        curScore = minimax(app,False,alpha,beta,depth-1)
                        
                        #undo move
                        app.board = curBoard 
                        newLoc = False
                        app.pieceSelected = False
                        app.checkmate = checkmate
                        app.check = app.check
                        app.teamTurn = team

                        best = max(best,curScore)

                        alpha = max(curScore,alpha)
                        if beta <= alpha:
                            break
                        
        return best

    else:
        team = 'black'
        best = 100000
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                piece = app.board[row][col]
                if piece != False and piece.team == team:
                    findPossibleMoves(app,piece,False)
                    # print(app.currentLegalMoves)
                    # print(piece.name,'pos:',piece.row,piece.col)
                    for (moveRow,moveCol) in app.currentLegalMoves:
                        #saving current instance of board
                        curBoard = copy.deepcopy(app.board)
                        check = app.check
                        checkmate = app.checkmate
                        app.teamTurn = team

                        if isinstance(app.board[moveRow][moveCol],King):
                            app.board = curBoard 
                            newLoc = False
                            app.pieceSelected = False
                            app.checkmate = checkmate
                            app.check = app.check
                            app.teamTurn = team
                            return score

                        moveToSelection(app,row,col,moveRow,moveCol)
                        
                        curScore = minimax(app,True,alpha,beta,depth-1)

                        #undo move
                        app.board = curBoard
                        newLoc = False
                        app.pieceSelected = False
                        app.checkmate = checkmate
                        app.check = app.check
                        app.teamTurn = team

                        best = min(best,curScore)

                        beta = min(curScore,beta)
                        if beta <= alpha:
                            break
                        
                        #reset all other app instances too
        return best