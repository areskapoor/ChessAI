from cmu_112_graphics import *
from chessPieces import *
from bounds import *
from chessFuncs import *
from minimax import *
from evaluation import *
from tkinter import *
import os

os.chdir(os.path.dirname(__file__)) #allows for files to be found 

############################
# Start Screen Mode
############################

def startScreenMode_mousePressed(app, event):
    x,y = event.x,event.y
    if x >= app.width/2-app.width/6 and x <= app.width/2+app.width/6:
        
        if y >= app.height/1.65+app.height/16 and y <= app.height/1.65+app.height/8:
            app.aiMode = True
            app.depth = 0
            app.mode = 'chessMode'
        elif y >= app.height/1.425+app.height/16 and y <= app.height/1.425+app.height/8:
            app.aiMode = True
            app.depth = 1
            app.mode = 'chessMode'
        elif y >= app.height/1.26+app.height/16 and y <= app.height/1.26+app.height/8:
            app.aiMode = True
            app.depth = 2
            app.mode = 'chessMode'

    if x >= app.width/2-app.width/4 and x <= app.width/2+app.width/4:
        # print(x,y)
        if y >= app.height/3+app.height/16 and y <= app.height/3+app.height/6:
            app.aiMode = False
            app.mode = 'chessMode'

def startScreenMode_redrawAll(app, canvas):

    #titles
    canvas.create_rectangle(0,0,app.width,app.height,
        fill='#bf9468',outline='#bf9468')
    canvas.create_text(app.width/2,app.height/4,text='Chess Ai',
        font='Guatami 65',fill='white')

    canvas.create_text(app.width/2,app.height/3,text='select a mode',
        font='Guatami 24 italic',fill='light grey')
    
    #multiplayer mode
    canvas.create_rectangle(app.width/2-app.width/4,app.height/3+app.height/16,\
        app.width/2+app.width/4,app.height/3+app.height/6,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/3+app.height/9,text='Multiplayer',
        font='Guatami 40',fill='#bf9468')

    #AI text
    canvas.create_text(app.width/2,app.height/2+app.height/9,text='Play Against AI',
        font='Guatami 40',fill='white')


    #easy mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.65+app.height/16,\
        app.width/2+app.width/6,app.height/1.65+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.65+app.height/11,text='Easy',
        font='Guatami 26',fill='#bf9468')

    #medium mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.425+app.height/16,\
        app.width/2+app.width/6,app.height/1.425+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.425+app.height/11,text='Medium',
        font='Guatami 26',fill='#bf9468')
    
    #hard mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.26+app.height/16,\
        app.width/2+app.width/6,app.height/1.26+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.26+app.height/11,text='Hard',
        font='Guatami 26',fill='#bf9468')


############################
# Checkmate Mode
############################
def checkmateMode_mousePressed(app, event):
    app.checkmate = None
    x,y = event.x,event.y
    if x >= app.width/2-app.width/6 and x <= app.width/2+app.width/6:
        
        if y >= app.height/1.65+app.height/16 and y <= app.height/1.65+app.height/8:
            app.aiMode = True
            app.depth = 0
            app.mode = 'chessMode'
        elif y >= app.height/1.425+app.height/16 and y <= app.height/1.425+app.height/8:
            app.aiMode = True
            app.depth = 1
            app.mode = 'chessMode'
        elif y >= app.height/1.26+app.height/16 and y <= app.height/1.26+app.height/8:
            app.aiMode = True
            app.depth = 2
            app.mode = 'chessMode'

    if x >= app.width/2-app.width/4 and x <= app.width/2+app.width/4:
        # print(x,y)
        if y >= app.height/3+app.height/16 and y <= app.height/3+app.height/6:
            app.aiMode = False
            app.mode = 'chessMode'

def checkmateMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,
        fill='#bf9468',outline='#bf9468')
    canvas.create_text(app.width/2,app.height/4,text='Checkmate',
        font='Guatami 65',fill='white')
    if app.checkmate == 'white':
        winner = 'Black'
    else:
        winner = 'White'
    canvas.create_text(app.width/2,app.height/3,
        text=f'{winner} Wins',
        font='Guatami 24 italic',fill='light grey')

    canvas.create_rectangle(app.width/2-app.width/4,app.height/3+app.height/16,\
        app.width/2+app.width/4,app.height/3+app.height/6,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/3+app.height/9,text='Multiplayer',
        font='Guatami 40',fill='#bf9468')

    #AI text
    canvas.create_text(app.width/2,app.height/2+app.height/9,text='Play Against AI',
        font='Guatami 40',fill='white')

    #easy mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.65+app.height/16,\
        app.width/2+app.width/6,app.height/1.65+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.65+app.height/11,text='Easy',
        font='Guatami 26',fill='#bf9468')

    #medium mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.425+app.height/16,\
        app.width/2+app.width/6,app.height/1.425+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.425+app.height/11,text='Medium',
        font='Guatami 26',fill='#bf9468')
    
    #hard mode
    canvas.create_rectangle(app.width/2-app.width/6,app.height/1.26+app.height/16,\
        app.width/2+app.width/6,app.height/1.26+app.height/8,
        fill='white',outline='white')
    canvas.create_text(app.width/2,app.height/1.26+app.height/11,text='Hard',
        font='Guatami 26',fill='#bf9468')



############################
# Chess Mode
############################

def chessMode_mousePressed(app, event):
    (row, col) = getCell(app, event.x, event.y)
    newLoc = app.board[row][col]
    #if piece hasn't been selected yet
    if app.pieceSelected == False:
        selectPiece(app,newLoc)

    #if selection is another piece on player's team, switch selection
    elif newLoc != False and newLoc.team == app.pieceSelected.team:
        switchSelection(app,newLoc)

    #move to selection if a piece is currently selected
    elif (row,col) in app.currentLegalMoves: #MAKE SURE MOVE DOESN"T PUT OWN TEAM IN CHECK 
        moveToSelection(app,app.pieceSelected.row,app.pieceSelected.col,row,col)

def chessMode_timerFired(app):
    if app.aiMoving:
        makeMinimaxMove(app,False,app.depth,'black')
        app.teamTurn = 'white'
    
    if app.checkmate != None:
        app.mode = 'checkmateMode'

def chessMode_keyPressed(app,event):
    if event.key == 'e':
        evaluate(app)
    if event.key == 'm':
       app.aiMode = not app.aiMode
       print('AI Mode:',app.aiMode)
    if event.key == 'r':
        resetApp(app)
        app.aiMode = False
        app.mode = 'startScreenMode'

def chessMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,
        fill='#522200',outline='#522200')
    drawBoard(app, canvas)
    for move in app.currentLegalMoves:
        (x0,y0,x1,y1) = getCellBounds(app,move[0],move[1])
        canvas.create_text(x0+ 0.5*((app.width-2*app.margin)/app.cols),
            y0+ 0.5*((app.height-2*app.margin)/app.rows),text='o',
                       font="Arial 26 bold", fill="green")


############################
# Main app
############################
def appStarted(app):
    resetApp(app)

def resetApp(app):
    app.rows = 8
    app.cols = 8
    app.margin = 40
    app.pieceR = (app.width-2*app.margin)/2*app.cols
    app.pieceSelected = False
    app.aiMode = True
    app.teamTurn = 'white' #ai is set as black by default
    app.aiTurn = False #starts with real player's turn
    app.check = None #can be either None, 'white' or 'black'
    app.checkmate = None
    app.aiMoving = False
    app.castled = None
    app.depth = 2
    app.findingSafePieces = False
    app.movesOutOfCheck = set()
    app.kingsMovesOutOfCheck = set()
    app.mode = 'startScreenMode'
    app.images = {
        'blackPawn': app.loadImage('blackPawn.png'),
        'whitePawn': app.loadImage('whitePawn.png'),

        'blackKnight': app.loadImage('blackKnight.png'),
        'whiteKnight': app.loadImage('whiteKnight.png'),

        'blackRook': app.loadImage('blackRook.png'),
        'whiteRook': app.loadImage('whiteRook.png'),

        'blackQueen': app.loadImage('blackQueen.png'),
        'whiteQueen': app.loadImage('whiteQueen.png'),

        'blackBishop': app.loadImage('blackBishop.png'),
        'whiteBishop': app.loadImage('whiteBishop.png'),

        'blackKing': app.loadImage('blackKing.png'),
        'whiteKing': app.loadImage('whiteKing.png'),
    }
    makeBoard(app)

    app.currentLegalMoves = set()

def makeBoard(app):
    app.board = [
        #a  b  c  d  e  f  g  h
        [False,False,False,False,False,False,False,False], #8
        [False,False,False,False,False,False,False,False], #7
        [False,False,False,False,False,False,False,False], #6
        [False,False,False,False,False,False,False,False], #5
        [False,False,False,False,False,False,False,False], #4
        [False,False,False,False,False,False,False,False], #3
        [False,False,False,False,False,False,False,False], #2
        [False,False,False,False,False,False,False,False]  #1
    ]

    #initialize board with pieces
    for col in range(app.cols):
        app.board[1][col] = Pawn(app,1,col,'black',app.images['blackPawn'])
        app.board[6][col] = Pawn(app,6,col,'white',app.images['whitePawn'])

    app.board[0][0] = Rook(app,0,0,'black',app.images['blackRook'])
    app.board[0][7] = Rook(app,0,7,'black',app.images['blackRook'])
    app.board[7][0] = Rook(app,7,0,'white',app.images['whiteRook'])
    app.board[7][7] = Rook(app,7,7,'white',app.images['whiteRook'])

    app.board[0][1] = Knight(app,0,1,'black',app.images['blackKnight'])
    app.board[0][6] = Knight(app,0,6,'black',app.images['blackKnight'])
    app.board[7][1] = Knight(app,7,1,'white',app.images['whiteKnight'])
    app.board[7][6] = Knight(app,7,6,'white',app.images['whiteKnight'])

    app.board[0][2] = Bishop(app,0,2,'black',app.images['blackBishop'])
    app.board[0][5] = Bishop(app,0,5,'black',app.images['blackBishop'])
    app.board[7][2] = Bishop(app,7,2,'white',app.images['whiteBishop'])
    app.board[7][5] = Bishop(app,7,5,'white',app.images['whiteBishop'])

    app.board[0][3] = Queen(app,0,3,'black',app.images['blackQueen'])
    app.board[7][3] = Queen(app,7,3,'white',app.images['whiteQueen'])

    app.board[0][4] = King(app,0,4,'black',app.images['blackKing'])
    app.board[7][4] = King(app,7,4,'white',app.images['whiteKing'])


def drawBoard(app,canvas):
    brown = '#bf9468'
    whiteSquare = False
    for row in range(len(app.board)):
        whiteSquare = not whiteSquare
        for col in range(len(app.board[0])):
                #gets coords of cell
                (x0,y0,x1,y1) = getCellBounds(app,row,col)
                if whiteSquare:
                    fillColor = 'beige'
                elif not whiteSquare:
                    fillColor = brown
                canvas.create_rectangle(x0,y0,x1,y1,
                    fill=fillColor,outline=fillColor)
                whiteSquare = not whiteSquare
                if app.board[row][col] != False:
                    piece = app.board[row][col]
                    piece.drawPiece(app,canvas)

runApp(width=600, height=600)