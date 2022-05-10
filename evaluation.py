from chessFuncs import *

def protectedPieceFinder(app):
    #loop through all pieces and find their possible moves
    #create a set of poss moves of all pieces that land on another one of their pieces {(row,col,piece obj)}

    #at the end loop thru set and add score of pieceWeight/2 (maybe/2 or smth else)
    protectedPieces = set()
    attackedPieces = set()
    app.findingSafePieces = True
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if piece != False:
                findPossibleMoves(app,piece,False)
                for (moveRow,moveCol) in app.currentLegalMoves:
                    movePiece = app.board[moveRow][moveCol]
                    if movePiece != False and movePiece.team == piece.team:
                        protectedPieces.add(movePiece)
                    elif movePiece != False and movePiece.team != piece.team:
                        attackedPieces.add(movePiece)

    print(protectedPieces)
    app.findingSafePieces = False

    return protectedPieces,attackedPieces



def evaluate(app):
    score = 0
    
    
    bPiecePosWeight = {
        'Pawn': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 3, 7, 7, 3, 1, 0], 
        [0, 1, 6, 7, 7, 6, 1, 0], 
        [2, 3, 6, 7, 7, 6, 3, 2],
        [8, 8, 8, 8, 8, 8, 8, 8], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
        'Knight': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 5, 3, 3, 5, 1, 1],
        [1, 1, 5, 4, 4, 5, 1, 1], 
        [1, 3, 6, 7, 7, 6, 3, 1], 
        [1, 1, 3, 1, 1, 3, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
        'Bishop': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 3, 0, 1, 1, 0, 3, 0],
        [0, 3, 1, 3, 3, 1, 3, 0],
        [0, 0, 1, 2, 2, 1, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
        'Rook': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, 1, 1, 1, 1, 1, 1, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1], 
        [-1, 0, 0, 0, 0, 0, 0, -1], 
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
        'Queen': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1.5, 1.5, 1.5, 1.5, 0, 0],
        [0, 0, 1.5, 1.5, 1.5, 1.5, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
        'King': [
        #a  b  c  d  e  f  g  h
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
        }

        #dont count pawns for endgame calculator (0-6 pieces = endgame)
        #make sure it doesn't make stupid sacrifices(queen takes knight that is protected)
    
    wPiecePosWeight = {
        'Pawn': list(reversed(bPiecePosWeight['Pawn'])),
        'Knight': list(reversed(bPiecePosWeight['Knight'])),
        'Bishop': list(reversed(bPiecePosWeight['Bishop'])),
        'Rook': list(reversed(bPiecePosWeight['Rook'])),
        'Queen': list(reversed(bPiecePosWeight['Queen'])),
        'King': list(reversed(bPiecePosWeight['King']))
        }

    pieceWeight = {
        'white' : {
            'Pawn': 50,
            'Knight': 150,
            'Bishop': 150,
            'Rook': 250,
            'Queen': 450,
            'King': 4500
            },
        'black' : {
            'Pawn': -50,
            'Knight': -250,
            'Bishop': -150,
            'Rook': -250,
            'Queen': -450,
            'King': -4500
            }
        }

    for row in range(len(app.board)): #piece posession
        for col in range(len(app.board[0])):
            piece = app.board[row][col]
            if piece != False:
                score += pieceWeight[piece.team][piece.name]
                if piece.team == 'white': #add pos weight for white to score
                    piecePosWeight = wPiecePosWeight[piece.name]
                    score += piecePosWeight[row][col]
                elif piece.team == 'black': #add pos weight for black to score
                    piecePosWeight = bPiecePosWeight[piece.name]
                    score -= piecePosWeight[row][col]
    
    protectedPieces,attackedPieces = protectedPieceFinder(app)
    # for piece in protectedPieces:
    #     if not isinstance(piece,King) and not isinstance(piece,Pawn):
    #         score += (pieceWeight[piece.team][piece.name])/15
    #     elif isinstance(piece,Pawn):
    #         score += (pieceWeight[piece.team][piece.name])/20
    for piece in attackedPieces:
        if (app.teamTurn == 'black' and piece.team == 'white' and 
            not isinstance(piece,King)):

            score += (pieceWeight['black'][piece.name]) #keep track of which piece is attacking the piece
        
        elif (app.teamTurn == 'white' and piece.team == 'black' and 
            not isinstance(piece,King)):

            score += (pieceWeight['white'][piece.name])
    
    if app.castled == 'white':
        score += 10
    elif app.castled == 'black':
        score -= 10

    if app.checkmate == 'white':
        score -= 4500
    elif app.checkmate == 'black':
        score += 4500
    
    if app.check == 'white':
        score -= 10
    elif app.check == 'black':
        score += 10

    return score