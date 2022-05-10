from cmu_112_graphics import *
from chessPieces import *

def printBoard(app):
    for row in app.board:
        print(row)

def switchSelection(app,newLoc):
    app.pieceSelected.toggleSelect()
    app.pieceSelected = newLoc
    app.pieceSelected.toggleSelect()
    findPossibleMoves(app,app.pieceSelected,False)
    #adjustPossibleMoves(app)

def selectPiece(app,newLoc):
    app.pieceSelected = newLoc
    if (app.pieceSelected != False and app.pieceSelected != False and 
        app.pieceSelected.team == app.teamTurn):
        app.pieceSelected.toggleSelect()
        findPossibleMoves(app,app.pieceSelected,False)
    else:
        app.pieceSelected = False


def moveToSelection(app,startRow,startCol,row,col):
    # oldRow, oldCol = app.pieceSelected.row, app.pieceSelected.col

    app.pieceSelected = app.board[startRow][startCol]

    #checks for castling move
    if isinstance(app.pieceSelected,King):
        castle = False
        if app.pieceSelected.team == 'white':
            rookRow = 7
        else:
            rookRow = 0

        if col-startCol == 2:
            castle = True
            rookCol = 7
            rookMoveCol = 5
            rook = app.board[rookRow][rookCol]

        elif col-startCol == -2:
            castle = True
            rookCol = 0
            rookMoveCol = 3
            rook = app.board[rookRow][rookCol]

        if castle:
            app.board[rookRow][rookCol] = False
            rook.move(app,rookRow,rookMoveCol)
            app.board[rookRow][rookMoveCol] = rook
            app.castled = True

    # if isinstance(app.pieceSelected,Pawn):
    #     if app.pieceSelected.team == 'white' and row == 0:
    #         app.pieceSelected.kill()
    #         app.pieceSelected = Queen(app,row,col,'white',app.images['whiteQueen']
    #     # elif app.pieceSelected.team == 'black' and row == 7:
    #     #     app.pieceSelected.kill()
    #     #     app.pieceSelected = Queen(app,row,col,'black',app.images['whiteQueen']
        


    app.board[startRow][startCol] = False
    app.pieceSelected.move(app,row,col)
    newLoc = app.board[row][col]
    app.board[row][col] = app.pieceSelected
    

    piece = inCheck(app,app.pieceSelected.team)

    #undoes move if team is in check
    if (app.check == app.pieceSelected.team and not
        (piece != None and (piece.row,piece.col) #take second logic part out of this conditional and put in separate one - if condition met then make app.check == to none
        == (app.pieceSelected.row,app.pieceSelected.col))):

        app.pieceSelected.row,app.pieceSelected.col = startRow,startCol
        app.board[row][col] = False
        app.board[startRow][startCol] = app.pieceSelected
        app.pieceSelected.moveNum -= 1
    
    else:
        #removes piece if move lands it on another piece
        if newLoc != False and newLoc.team != app.pieceSelected.team:
            # print('attack')
            # print(newLoc.name,newLoc.row,newLoc.col)
            
            newLoc.kill()

        app.pieceSelected.toggleSelect()

        #switch team turn
        if app.teamTurn == 'white':
            app.teamTurn = 'black'
        elif app.teamTurn == 'black':
            app.teamTurn = 'white'

        inCheck(app,app.teamTurn) #checks if other team is in check after move
        if app.check == app.teamTurn:
            possibleMoves,kingsPossibleMoves = tryPossibleMoves(app,app.teamTurn)
            if len(possibleMoves) == 0 and len(kingsPossibleMoves) == 0:
                app.checkmate = app.teamTurn #checkmate
                print('checkmate')
            
        if app.aiMode and not app.aiMoving:
            app.aiMoving = True

        app.pieceSelected = False
    app.currentLegalMoves = set()

def findKing(app,team):
    # printBoard(app)
    # print('team',team)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if isinstance(piece,King) and piece.team == team:
                # print(team,piece.team)
                print('king found')
                return (row,col)
    return (-1,-1)


def findPossibleMoves(app,piece,tryingMoves):
    app.currentLegalMoves = set()
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            legal = piece.isLegal(app,row,col)
            if legal and not tryingMoves:
                if ((app.check == piece.team and (row,col) in 
                    app.movesOutOfCheck)
                    or app.check != piece.team):

                    app.currentLegalMoves.add((row,col))

                elif (isinstance(piece,King) and app.check == piece.team and 
                    (row,col) in app.kingsMovesOutOfCheck):
                    app.currentLegalMoves.add((row,col))

            elif legal:
                app.currentLegalMoves.add((row,col))


def tryPossibleMoves(app,team):
    app.movesOutOfCheck = set()
    curTurn = app.teamTurn
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if piece != False and piece.team == team:
                findPossibleMoves(app,piece,True)
                for (moveRow,moveCol) in app.currentLegalMoves:
                    #print(piece.moveNum)
                    # oldRow, oldCol = piece.row, piece.col
                    attackedPiece = app.board[moveRow][moveCol]
                    if attackedPiece != False and attackedPiece.team != team:
                        attackedPiece.kill()
                        app.board[moveRow][moveCol] = False
                        # print('attacked',attackedPiece)

                    app.board[row][col] = False
                    piece.move(app,row,col)
                    app.board[moveRow][moveCol] = piece

                    if inCheck(app,team) == None:
                        if isinstance(app.board[moveRow][moveCol],King):
                            app.kingsMovesOutOfCheck.add((moveRow,moveCol))
                        else:
                            app.movesOutOfCheck.add((moveRow,moveCol))
                    if attackedPiece != False and attackedPiece.isKilled: #undo kill
                        app.board[moveRow][moveCol] = attackedPiece
                        not attackedPiece.isKilled
                    else:
                        app.board[moveRow][moveCol] = False #undo move
                    piece.move(app,row,col)
                    app.board[row][col] = piece
                    
                    piece.moveNum -= 2 #reset movenum of piece
    app.teamTurn = curTurn
    app.check = team #reset check state
    print(app.movesOutOfCheck,app.kingsMovesOutOfCheck)
    return app.movesOutOfCheck,app.kingsMovesOutOfCheck
    

def inCheck(app,team):
    (kRow,kCol) = findKing(app,team)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if piece != False and piece.team != team:
                findPossibleMoves(app,piece,False)
                #current issue: move to kings pos (1,5) is not considered legal 
                # since queen not removed when king takes her in simulation
                if (kRow,kCol) in app.currentLegalMoves:
                    #print(team,'in Check')
                    app.check = team
                    return piece #piece that is threatening check
    app.check = None
    app.currentLegalMoves = set()

