from random import choice
from tkinter import *
#import time

class Connect4:
    """This is the Connect4 Constructor"""
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.turn = 1

        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.frameWidth = 600
        self.frameHeight = 650
        #Buttons
        self.quit = Button(self.frame, text = 'Quit', command = self.quitClick)
        self.quit.pack(side = 'left')
        self.restart = Button(self.frame, text = 'Restart', command = self.clear)
        self.restart.pack(side = 'left')
        self.fill = Button(self.frame, text = 'Fill Board', command = self.fillBoard)
        self.fill.pack(side = 'left')
        #Slider
        self.scale = Scale(self.frame, from_ = 0, to = 5, length = 200, tickinterval = 1, orient = HORIZONTAL)
        self.scale.set(0)
        self.scale.pack()
        self.scale.bind("<ButtonRelease-1>", self.scaleChange)
        #for GUI
        self.data = []
        self.diameter = int(self.frameWidth/self.width)
        self.initialColor = 'white'
        self.draw = Canvas(window, height = self.frameHeight, width = self.frameWidth)
        self.draw.bind('<Button-1>', self.mouseInput)
        self.draw.pack()
        self.circles = []
        self.colors = []
        y = 0
        for row in range(self.height):
            circleRow = []
            colorRow = []
            x = 0
            boardRow = []
            for col in range(self.width):
                circleRow += [self.draw.create_oval(x, y, x + self.diameter, y + self.diameter, fill = self.initialColor)]
                colorRow += [self.initialColor]
                x += self.diameter
                boardRow += [' ']
            self.circles += [circleRow]
            self.colors += [colorRow]
            y += self.diameter
            self.data += [boardRow]
        #for text
        self.messageSize = 25
        self.gameMessage = 'Starting the game!'
        self.message = self.draw.create_text(self.messageSize, self.frameHeight-self.messageSize, text = self.gameMessage, anchor = 'w', font = 'Courier 24')
        #for X & O
        # for row in range(self.height):
        #     boardRow = []
        #     for col in range(self.width):
        #         boardRow += [' ']
        #     self.data += [boardRow]

    def __repr__(self):
        """ this method returns a string representation
        for an object of type Board """
        s = ''
        for row in range( self.height ):
            s += '|'
            for col in range( self.width ):
                s += self.data[row][col] + '|'
            s += '\n'
        s += '--'*self.width + '-\n'
        for col in range( self.width ):
            s += ' ' + str(col % 10)
        s += '\n'
        return s

    def clear(self):
        """ Same method in __init__ """
        self.turn = 1
        self.data = []
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
                self.draw.itemconfig(self.circles[row][col], fill = self.initialColor)
            self.data += [boardRow]
        return


    def addMove(self, col, ox):
        """ Checks the column (col) from top to bottom,
         looking for the last ' ' <-empty space """
        #print (range(len(self.data)))
        for row in range(self.height):
            if self.data[row][col] == ' ':
                bottom = row
        if Connect4.allowsMove(self, col):
            self.data[bottom][col] = ox
            newColor = self.setColor(bottom, col)
            self.draw.itemconfig(self.circles[bottom][col], fill = newColor)

    def allowsMove(self, col):
        """ Checks if column (col) has any ' ' <-empty space """
        for row in range(self.height):
            if self.data[row][col] == ' ':
                return True
        return False

    def delMove(self, col):
        """ Checks column (col) from top to bottom for a ox
        if it finds a ox, overwrite it with a ' ' <-empty space """
        for row in range(self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                self.draw.itemconfig(self.circles[row][col], fill = self.initialColor)
                return

    def isFull(self):
        """ Uses function allowsMove to check ever column """
        Full = 0
        for len in range(self.width):
            Full += Connect4.allowsMove(self, len)
        if Full == 0:
                return True
        return False

    def winsFor(self, ox):
        """ Checks if there are 4 ox's in a row through
         one of the ox's reference point """
        #Horizontal - reference: Left most ox
        for row in range(self.height):
            for col in range(self.width - 3):
                if self.data[row][col] == ox and \
                self.data[row][col + 1] == ox and \
                self.data[row][col + 2] == ox and \
                self.data[row][col + 3] == ox:
                    return True
        #Vertical - reference: Top most ox
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.data[row][col] == ox and \
                self.data[row + 1][col] == ox and \
                self.data[row + 2][col] == ox and \
                self.data[row + 3][col] == ox:
                    return True
        #Diagonally increasing - reference: Top Right most ox
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.data[row][col] == ox and \
                self.data[row + 1][col - 1] == ox and \
                self.data[row + 2][col - 2] == ox and \
                self.data[row + 3][col - 3] == ox:
                    return True
        #Diagonally decreasing - reference: Top Left most ox
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.data[row][col] == ox and \
                self.data[row + 1][col + 1] == ox and \
                self.data[row + 2][col + 2] == ox and \
                self.data[row + 3][col + 3] == ox:
                    return True
        return False

    def playGameWith(self, aiPlayer): # get the move self.addMove(oMove,’O’) # make the move
        turn = 1
        while True:
            #print (self)
            if turn == 1: # X turn
                print ('Column Choice:')
                playerInput = int(input())
                if self.allowsMove(playerInput):
                    self.addMove(playerInput, 'X')
                    if self.winsFor('X'):
                        print ("X wins")
                        return
                    turn = not turn
                else:
                    print ('Column Full, Try Again')
            else:
                oMove = aiPlayer.nextMove(self)
                #print (oMove)
                if self.allowsMove(oMove):
                    self.addMove(oMove, 'O')
                if self.winsFor('O'):
                    print ("O wins")
                    return
                turn = not turn

    def hostGame(self):
        turn = 1
        while True:
            #print (self)
            if turn == 1: # X turn
                print ('X Column Choice:')
                playerInput = int(input())
                if self.allowsMove(playerInput):
                    self.addMove(playerInput, 'X')
                    if self.winsFor('X'):
                        print ("X wins")
                        return
                    turn = not turn
                else:
                    print ('Column Full, Try Again')
            else:
                print ('O Column Choice:')
                playerInput = int(input())
                if self.allowsMove(playerInput):
                    self.addMove(playerInput, 'O')
                    if self.winsFor('O'):
                        print ("O wins")
                        return
                    turn = not turn
                else:
                    print ('Column Full, Try Again')

    def quitClick(self):
        self.window.destroy()

    def playGUI(self, aiPlayer):
        self.aiPlayer = aiPlayer

    def scaleChange(self, event):
        #self.scaleValue = int(self.scale.get())
        #self.aiPlayer.ply = self.scaleValue
        self.aiPlayer.ply = self.scale.get()

    def mouseInput(self, event):
        #print(int(event.x/self.diameter))
        col = int(event.x/self.diameter)
        #row = int(event.y/self.diameter)
        #print('board[%s][%s]' % (row, col))
        #print ('col:%d turn:%d' % (col, self.turn))
        if self.turn == 1: # X turn
            playerInput = col
            if self.isFull():
                return self.changeText("Draw")
            if self.allowsMove(playerInput):
                self.addMove(playerInput, 'X')
                if self.winsFor('X'):
                    return self.changeText("Red wins")
                self.turn = not self.turn
                oMove = self.aiPlayer.nextMove(self)
                if self.isFull():
                    return self.changeText("Draw")
                if self.allowsMove(oMove):
                    #time.sleep(.5)
                    self.addMove(oMove, 'O')
                if self.winsFor('O'):
                    return self.changeText("Black wins")
                self.changeText('Player %d\'s turn' % (self.turn + 1))
                self.turn = not self.turn
            else:
                self.changeText('Column Full, Try Again')
        #newColor = self.setColor(row, col)
        #self.draw.itemconfig(self.circles[row][col], fill = newColor)
        #self.column = col

    def changeText(self, s):
        self.draw.itemconfigure(self.message, text = s)

    def fillBoard(self):
        self.turn = 1
        #self.data = []
        for row in range(self.height):
            #boardRow = []
            for col in range(self.width):
                #boardRow += [' ']
                if int(row/2) % 2 == 1:
                    if col % 2 == 1:
                        self.data[row][col] = 'X'
                        self.draw.itemconfig(self.circles[row][col], fill = 'black')
                    else:
                        self.data[row][col] = 'O'
                        self.draw.itemconfig(self.circles[row][col], fill = 'red')
                else:
                    if col % 2 == 1:
                        self.data[row][col] = 'O'
                        self.draw.itemconfig(self.circles[row][col], fill = 'red')
                    else:
                        self.data[row][col] = 'X'
                        self.draw.itemconfig(self.circles[row][col], fill = 'black')
                if row == 0 and col == (self.width - 1):
                    self.data[row][col] = ' '
                    self.draw.itemconfig(self.circles[row][col], fill = self.initialColor)
        #print (self.data)

    def setColor(self, row, col):
        #color = self.colors[row][col]
        if self.turn == 1:
            color = 'red'
        else:
            color = 'black'
        self.colors[row][col] = color
        return color

class Player:
    def __init__(self, ox, tie, ply):
        self.ox = ox
        self.tie = tie
        self.ply = ply

    def __repr__(self, ply):
        return (ply)

    def nextMove(self, b):
        c = self.scoresFor(b, self.ox, self.ply)
        #print (c)
        return (self.tiebreakMove(c))
        #b.addMove(t, self.ox)

    def scoresFor(self, b, ox, ply): # USE RECURSIVE!
        score = []
        xo = self.notOX(ox)
        for col in range(b.width):
            if b.allowsMove(col):
                b.addMove(col, ox)
                if b.winsFor(ox):
                    score.append(100)
                elif ply > 1:
                        score.append(100 - max(self.scoresFor(b, xo, ply - 1)))
                else:
                    score.append(50)
                b.delMove(col)
            else:
                score.append(-1)
        return score

    def tiebreakMove(self, scores):
        if self.tie == 'Left':
            highest = 0
            bestCol = 0
            for col in range(len(scores) - 1):
                if scores[col] > highest:
                    highest = scores[col]
                    bestCol = col
            return bestCol
        if self.tie == 'Right':
            highest = 0
            bestCol = 0
            for col in range(-(len(scores) - 1)):
                if scores[abs(col)] > highest:
                    highest = scores[abs(col)]
                    bestCol = abs(col)
            return bestCol
        if self.tie == 'Random':
            bestCol = []
            for col in range(len(scores)):
                if scores[col] == max(scores):
                    bestCol.append(col)
            r = choice(bestCol)
            return r

    def notOX(self, ox):
        if ox == 'X':
            ox = chr((ord(ox)) - 9)
        if ox == 'O':
            ox = chr((ord(ox)) + 9)
        return ox

def main():
    #b = Connect4(7, 6)
    #b.hostGame()
    #b.playGameWith(Player('O', 'Random', 3))
    root = Tk()
    root.title('Connect4')
    bd = Connect4(7, 6, root)
    #print (bd.scale.get())
    aiPlayer = Player('O', 'Random', bd.scale.get())
    bd.playGUI(aiPlayer)
    root.mainloop()

if __name__ == '__main__':
    main()
