#function taken from 112 notes: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col) 

#function taken from 112 notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app,row,col):
    gridWidth = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col/app.cols
    y0 = app.margin + gridHeight * row/app.rows
    x1 = app.margin + gridWidth * (col+1)/app.cols
    y1 = app.margin + gridHeight * (row+1)/app.rows
    return (x0,y0,x1,y1)

#from 112 notes:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))