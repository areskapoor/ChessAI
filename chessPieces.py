from cmu_112_graphics import *
from bounds import *

#all images being used in the game were created by me


class Piece:

    def __init__(self,app,row,col,team,image):
        self.isAlive = True
        self.row = row
        self.col = col
        self.team = team
        self.color = f'{team}'
        self.moveNum = 0
        self.name = 'piece'
        self.image = app.scaleImage(image,1/4)
        self.isKilled = False
        # self.makeTransparent(app)
        #bool on whether next proposed move is on opponents piece
        self.moveIsOnPiece = False
    
    def __repr__(self):
        return self.team[0] + self.name

    def toggleSelect(self):
        if self.color == f'{self.team}':
            if self.team == 'black':
                self.color = '#1c1c1c'
            else:
                self.color = '#e0e0e0'
        else:
            self.color = f'{self.team}'

    def kill(self):
        self.isKilled = True

    def collision(self,app,drow,dcol):
        (r,c) =(0,0)
        while (r,c) != (drow,dcol):
            if (r,c) != (0,0) and app.board[r+self.row][c+self.col] != False:
                return False
            if drow < 0:
                if r != drow:
                    r -= 1
            else:
                if r != drow:
                    r += 1
            if dcol < 0:
                if c != dcol:
                    c -= 1
            else:
                if c != dcol:
                    c += 1
        return True

    #checks if new row and col are a legal move to make
    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False
        if (drow,dcol) in self.legalMove:
            return True
        return False

    def move(self,app,newRow,newCol):
        print('moving',self,'from',(self.row,self.col),'to',(newRow,newCol))
        #app.board[self.row][self.col] = False
        self.row = newRow
        self.col = newCol
        #app.board[newRow][newCol] = self
        self.moveNum += 1

    #function from chessFuncs and only here bc of circular dependencies
    def findPossibleMovesKing(self,app,piece,tryingMoves):
        app.currentLegalMoves = []
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                legal = piece.isLegal(app,row,col)
                if legal and not tryingMoves:
                    if ((app.check == piece.team and (row,col) in 
                        app.movesOutOfCheck)
                        or app.check != piece.team):

                        app.currentLegalMoves.append((row,col))

                    elif (isinstance(piece,King) and app.check == piece.team and 
                        (row,col) in app.kingsMovesOutOfCheck):

                        app.currentLegalMoves.append((row,col))

                elif legal: #and app.check != piece.team:
                    app.currentLegalMoves.append((row,col))
    
    #function from chessFuncs and only here bc of circular dependencies
    def kingInCheck(self,app,team):
        (kRow,kCol) = self.findTheKing(app,team)
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                piece = app.board[row][col]
                if piece != False and piece.team != team and not isinstance(piece,King):
                    self.findPossibleMovesKing(app,piece,False)
                    #current issue: move to kings pos (1,5) is not considered legal 
                    # since queen not removed when king takes her in simulation
                    if (kRow,kCol) in app.currentLegalMoves:
                        #print(team,'in Check')
                        app.check = team
                        return piece #piece that is threatening check
        app.check = None

    #function from chessFuncs and only here bc of circular dependencies
    def findTheKing(self,app,team):
        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                piece = app.board[row][col]
                if isinstance(piece,King) and piece.team == team:
                    # print(team,piece.team)
                    print('king found')
                    return (row,col)
        return (-1,-1)

    def drawPiece(self,app,canvas):
        (x0,y0,x1,y1) = getCellBounds(app,self.row,self.col)
        canvas.create_image(x0+33, y0+33, image=ImageTk.PhotoImage(self.image))
        # canvas.create_rectangle(x0,y0,x1,y1,fill=self.color,outline='grey')
        # canvas.create_text(x0+ 0.5*((app.width-2*app.margin)/app.cols),
        #     y0+ 0.5*((app.height-2*app.margin)/app.rows),text=self.abbrev,
        #                font="Arial 26 bold", fill="darkBlue")


class Pawn(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'P'
        self.name = 'Pawn'
        if self.team == 'black':
            self.legalMove = {(1,0)}
            self.attackLegalMove = {(1,-1),(1,1)}
            self.firstLegalMove = {(2,0)}

            #images not working
            #self.image = app.loadImage('blackPawn.png') 
        else:
            self.legalMove = {(-1,0)}
            self.attackLegalMove = {(-1,-1),(-1,1)}
            self.firstLegalMove = {(-2,0)}
            #self.image = app.loadImage('whitePawn.png')

    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False
        if attackedPiece != False:
            if (drow,dcol) in self.legalMove: #cannot move if opponent in front
                return False 
            elif (drow,dcol) in self.attackLegalMove:
                #print('attack')
                return True
        if (drow,dcol) in self.legalMove:
            return True
        
        #allows pawn to move 2 spaces on first move - BUGGY CODE
        elif (not attackedPiece and self.moveNum == 0 and 
        (drow,dcol) in self.firstLegalMove):
            return self.collision(app,drow,dcol)
        return False

class Rook(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'R'
        self.name = 'Rook'

    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False
        if drow == 0 or dcol == 0:
            return self.collision(app,drow,dcol)
        return False

class Knight(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'Kn'
        self.name = 'Knight'
        self.legalMove = {(1,2),(2,1),(1,-2),(-1,2),(-1,-2),
            (2,-1),(-2,1),(-2,-1)}
        if self.team == 'black': None
            #self.image = app.loadImage('blackKnight.png')
        else: None
            #self.image = app.loadImage('whiteKnight.png')
        

class Bishop(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'B'
        self.name = 'Bishop'


    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False
        if abs(drow) == abs(dcol):
            return self.collision(app,drow,dcol)
        return False

class Queen(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'Q'
        self.name = 'Queen'


    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False
        if abs(drow) == abs(dcol) or drow == 0 or dcol == 0:
            return self.collision(app,drow,dcol)
        return False

class King(Piece):
    def __init__(self,app,row,col,team,image):
        super().__init__(app,row,col,team,image)
        self.abbrev = 'Ki'
        self.name = 'King'
        self.legalMove = {(1,1),(1,0),(-1,0),(1,-1),
            (0,1),(0,-1),(-1,1),(-1,-1)}

        self.leftCastlingMove = {(0,-2)}
        self.rightCastlingMove ={(0,2)}

    def isLegal(self,app,newRow,newCol):
        attackedPiece = app.board[newRow][newCol]
        drow, dcol = newRow-self.row, newCol-self.col
        #print('shit cock:',newRow,newCol)

        if (attackedPiece != False and 
            (attackedPiece.team == self.team and not app.findingSafePieces)):
            return False

        if (drow,dcol) in self.legalMove:
            print(newRow,newCol)
            return True

        elif (drow,dcol) in self.rightCastlingMove:
            return self.canCastle(app,drow,dcol)

        elif (drow,dcol) in self.leftCastlingMove:
            return self.canCastle(app,drow,dcol)

        return False
    
    def canCastle(self,app,drow,dcol):
        if self.moveNum != 0:
            #print(self.moveNum)
            #print('movenum aint 0 for',self)
            return False
        if dcol > 0:

            piece = app.board[self.row+drow][self.col+dcol+1]
            if not isinstance(piece,Rook):
                #print('rook aint where it should be')
                return False
            elif piece.moveNum != 0:
                #print('rook already moved bitch')
                return False
        elif dcol < 0:
            piece = app.board[self.row+drow][self.col+dcol-2]
            if not isinstance(piece,Rook):
                #print('rook aint where it should be')
                return False
            elif piece.moveNum != 0:
                #print('rook already moved bitch')
                return False
        result = self.tryCastle(app,drow,dcol,piece)   
        #print('can castle:',result)
        return result

    def tryCastle(self,app,drow,dcol,rook):
        (r,c) =(0,0)
        startRow,startCol = self.row,self.col
        curLegalMoves = app.currentLegalMoves
        self.kingInCheck(app,self.team)
        app.currentLegalMoves = curLegalMoves

        if app.check == self.team:
            #print('cant castle: in check')
            return False
        while (self.row+r,self.col+c) != (drow,dcol):
            #print(self.row,self.col)

            if drow < 0:
                if r != drow:
                    r = -1
            else:
                if r != drow:
                    r = 1
            if dcol < 0:
                if c != dcol:
                    c = -1
            else:
                if c != dcol:
                    c = 1
            if app.board[r+self.row][c+self.col] == rook:
                app.board[self.row][self.col] = False
                self.col = 4 #always 4 if moveNum = 0
                app.board[startRow][startCol] = self
                self.moveNum = 0
                break

            elif app.board[r+self.row][c+self.col] != False:
                #reset move
                app.board[self.row][self.col] = False
                self.col = 4 #always 4 if moveNum = 0
                app.board[startRow][startCol] = self
                self.moveNum = 0

                #print('cant castle: piece in castling path')
                #print('the piece is',app.board[r+self.row][c+self.col],f'at ({r+self.row},{c+self.col})')
                return False
            
            app.board[self.row][self.col] = False
            self.move(app,r+self.row,c+self.col)
            app.board[self.row][self.col] = self

            curLegalMoves = app.currentLegalMoves
            self.kingInCheck(app,self.team)
            app.currentLegalMoves = curLegalMoves

            if app.check == self.team:
                app.board[self.row][self.col] = False
                self.col = 4 #always 4 if moveNum = 0
                app.board[startRow][startCol] = self
                self.moveNum = 0
                app.check == None
                #print('cant castle: in check during path')
                return False

        return True

        


