import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from collections import Counter


class MyWindow(QWidget):
    def __init__(self, parent=None):
        # Generate placeholder board and set up letter ratios for more common letters
        self.board = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']]
        self.letterDistribution = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E',
                              'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I','I',
                              'I', 'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 'M', 'N', 'N', 'N','N',
                              'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R','R',
                              'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 'V', 'W', 'W', 'X',
                              'Y', 'Y', 'Z']

        super(MyWindow, self).__init__(parent)
        # Set window information (size, title, color)
        self.setGeometry(500, 200, 800, 600)
        self.setWindowTitle("Word Hunt Helper")
        self.setStyleSheet("background-color: lightgreen;")
        layout = QVBoxLayout()
        self.initUI(layout)


    def initUI(self, layout):
        font = 'Georgia'
        self.title = QLabel("WordHunt Helper")
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setFont(QFont('Georgia', 25))

        self.author = QLabel("by: Rishabh Kanodia and Angelo Chen")
        self.author.setAlignment(Qt.AlignHCenter)
        self.author.setFont(QFont(font, 15))

        # Make Button to Generate a board
        self.btnGenBoard = QPushButton("Generate Board")
        self.btnGenBoard.setFixedSize(400, 50)
        self.btnGenBoard.move(510, 410)
        self.btnGenBoard.setStyleSheet("QPushButton{background-color : #40bf80;} QPushButton::pressed{background-color : #66cc99;} QPushButton::hover{background-color : #66cc99;}")
        self.btnGenBoard.setFont(QFont(font, 15))
        self.boardMade = False
        self.btnGenBoard.clicked.connect(self.getBoard)

        # Make Button to Insert a board
        self.btnInsBoard = QPushButton("Insert Board")
        self.btnInsBoard.setFixedSize(400, 50)
        self.btnInsBoard.setStyleSheet("QPushButton{background-color : #40bf80;} QPushButton::pressed{background-color : #66cc99;} QPushButton::hover{background-color : #66cc99;}")
        self.btnInsBoard.setFont(QFont(font, 15))
        self.btnInsBoard.clicked.connect(self.insertBoard)

        # Make Button to Run the word finder code
        self.btnFindWords = QPushButton('Find Words')
        self.btnFindWords.setStyleSheet("QPushButton{background-color : #40bf80;} QPushButton::pressed{background-color : #66cc99;} QPushButton::hover{background-color : #66cc99;}")
        self.btnFindWords.setFixedSize(400, 50)
        self.btnFindWords.setFont(QFont(font, 15))
        self.btnFindWords.clicked.connect(self.findWords)

        self.le = QLabel("Board")
        self.le.setAlignment(Qt.AlignCenter)
        self.le.setFont(QFont(font, 15))

        # Set up place holders for where the board will print
        self.row1 = QLabel('....')
        self.row1.setAlignment(Qt.AlignHCenter)
        self.row1.setFont(QFont(font, 20))
        self.row2 = QLabel('....')
        self.row2.setAlignment(Qt.AlignHCenter)
        self.row2.setFont(QFont(font, 20))
        self.row3 = QLabel('....')
        self.row3.setAlignment(Qt.AlignHCenter)
        self.row3.setFont(QFont(font, 20))
        self.row4 = QLabel('....')
        self.row4.setAlignment(Qt.AlignHCenter)
        self.row4.setFont(QFont(font, 20))

        # Make box where words will print
        self.printer = QLabel('Words Found:')
        self.printer.setAlignment(Qt.AlignCenter)
        self.printer.setFont(QFont(font, 15))
        self.output = QTextBrowser()
        self.output.setFont(QFont(font, 15))


        topGroup = QHBoxLayout()

        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.author)
        layout.addSpacing(20)

        # Add button widgets to a vertical group to later be put in horizontal group
        buttonGroup = QVBoxLayout()
        buttonGroup.addWidget(self.btnGenBoard)
        buttonGroup.addWidget(self.btnInsBoard)
        buttonGroup.addWidget(self.btnFindWords)
        buttonGroup.setAlignment(Qt.AlignCenter)

        # Add board widgets to a vertical group to later be put in horizontal group
        boardGroup = QVBoxLayout()
        boardGroup.addWidget(self.le)
        boardGroup.addWidget(self.row1)
        boardGroup.addWidget(self.row2)
        boardGroup.addWidget(self.row3)
        boardGroup.addWidget(self.row4)
        boardGroup.setAlignment(Qt.AlignCenter)

        # Add board and button widgets to a horizontal group
        topGroup.addSpacing(50)
        topGroup.addLayout(buttonGroup)
        topGroup.addLayout(boardGroup)

        # Add horizontal group and output to main layout
        layout.addLayout(topGroup)
        layout.addSpacing(20)
        layout.addWidget(self.printer)
        layout.addWidget(self.output)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


    def loadDictionary(self):
        # Load the dictionary from its file
        file = open('Collins Scrabble Words (2019).txt')
        self.dictionary = file.read().split()
        return self.dictionary

    def getBoard(self):
        # Randomly generate a board based on the letter distribution
        self.boardletters = str()
        # 2d array board
        for i in range(4):
            for j in range(4):
                self.board[i][j] = self.letterDistribution[np.random.randint(len(self.letterDistribution))]
                self.boardletters += self.board[i][j]
        print('Board:\n', self.board[0], '\n', self.board[1], '\n', self.board[2], '\n', self.board[3])

        # Print the board to the GUI
        row1, row2, row3, row4 = str(self.board[0]), str(self.board[1]), str(self.board[2]), str(self.board[3])
        row1, row2, row3, row4 = filter(str.isalpha,row1), filter(str.isalpha,row2), filter(str.isalpha,row3), filter(str.isalpha,row4)
        row1, row2, row3, row4 = " ".join(row1), " ".join(row2), " ".join(row3), " ".join(row4)
        self.row1.setText(row1)
        self.row2.setText(row2)
        self.row3.setText(row3)
        self.row4.setText(row4)

        # Load and reset the GUI
        self.printer.setText('Words Found:')
        self.dictionary = self.loadDictionary()
        self.boardMade = True
        self.output.clear()

    def insertBoard(self):
        # Intake a string for a board and turn into a grid
        self.boardletters, ok = QInputDialog.getText(self, 'Board Input', 'Enter the board as 16-letter string in all caps: ')
        self.boardletters = self.boardletters.upper()
        print(self.boardletters)
        if ok and len(self.boardletters) == 16 and self.boardletters.isalpha():
            for i in range(4):
                for j in range(4):
                    self.board[i][j] = self.boardletters[i * 4 + j]
            print('Board:\n', self.board[0], '\n', self.board[1], '\n', self.board[2], '\n', self.board[3])

            # Print the board to the GUI
            row1, row2, row3, row4 = str(self.board[0]), str(self.board[1]), str(self.board[2]), str(self.board[3])
            row1, row2, row3, row4 = filter(str.isalpha, row1), filter(str.isalpha, row2), filter(str.isalpha, row3), filter(str.isalpha, row4)
            row1, row2, row3, row4 = " ".join(row1), " ".join(row2), " ".join(row3), " ".join(row4)
            self.row1.setText(row1)
            self.row2.setText(row2)
            self.row3.setText(row3)
            self.row4.setText(row4)

            self.printer.setText('Words Found:')
            self.dictionary = self.loadDictionary()
            self.boardMade = True
            self.output.clear()
        # If input string does not have a length of 16
        elif len(self.boardletters) != 16:
            self.printer.setText('Please input a 16 letter string')



    def findWords(self):
        # Condition to check if board was generated yet
        if self.boardMade:
            # Run first filter to narrow down words then solve for actual words
            self.firstFilter()
            self.Solver(self.initFilter)
        else:
            self.printer.setText('Please generate/input a board first.')


    def issubset_replicate(self, A, B):
        # check if A is a subset of B
        subset = Counter(A) - Counter(B) == Counter()
        return subset

    def firstFilter(self):
        # Checks if the word is a subset of boardLetters (the board as a string)
        # Basically means if all the letters to make the word are in the board
        self.initFilter = []
        for word in self.dictionary:
            if len(word) == 16:
                print(word)
            if 3 <= len(word) <= 16:
                if self.issubset_replicate(word, self.boardletters):
                    self.initFilter.append(word)
        print('First Filter:', len(self.initFilter))



    def NextLetters(self, x, i, j):
        # x is the board
        # i is the first index
        # j is the second index
        i = int(i)
        j = int(j)
        NextLetterlist = []
        NextIndexlist = []
        # if either index is <0 or >4 then it should not be appended
        m, n = i - 1, j - 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i - 1, j
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i - 1, j + 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i, j + 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i + 1, j + 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i + 1, j
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i + 1, j - 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        m, n = i, j - 1
        if 0 <= m <= 3 and 0 <= n <= 3:
            NextLetterlist.append(x[m][n])
            NextIndexlist.append([m, n])

        return NextIndexlist

    def findIndex(self, letter):
        indexes = []
        for i in range(len(self.boardletters)):
            col = i % 4
            row = int(i / 4)
            tile = self.board[row][col]
            if tile == letter:
                indexes.append([row, col])
        return indexes

    def Solver(self, initFilter):
        hunted = []
        # Iterate through every single word
        for word in initFilter:
            # Find the indexes of the first letter in word
            initIndex = self.findIndex(word[0])

            # Turn the word into a list of letters
            letters = [x for x in word]

            # Iterate through every startpoint
            for startpoint in initIndex:
                # Variable initializations
                tracker = 1
                restricted = []
                isRestricted = False

                #Add startpoint as current position and to restricted list
                indexes = [startpoint[0], startpoint[1]]
                restricted.append([startpoint[0], startpoint[1]])
                # print('Index Letters:', indexes)

                # Runs through every letter possibility
                while True:
                    # If tracker (how many letters found) is equal to the length of the word, add it to final list
                    if tracker == len(word):
                        hunted.append(word)
                        # print('Word added:', word)
                        break

                    # Find all the letters around the current position
                    # If index is empty meaning no letter found before, then catch error and break
                    try:
                        nextIndex = self.NextLetters(self.board, indexes[0], indexes[1])
                    except:
                        break

                    # Iterate through every letter around current position
                    for i in range(len(nextIndex)):
                        # print(tracker)
                        # Checking if each surrounding letter is what the next letter in word needs to be
                        if self.board[nextIndex[i][0]][nextIndex[i][1]] == letters[tracker]:
                            # Check if surrounding letter is in the restricted list
                            for k in range(len(restricted)):
                                if [nextIndex[i][0], nextIndex[i][1]] == restricted[k]:
                                    indexes = []
                                    isRestricted = True
                                    break
                            # Add letter to restricted list and changes current position to that letter
                            if not isRestricted:
                                restricted.append([nextIndex[i][0], nextIndex[i][1]])
                                indexes = [nextIndex[i][0], nextIndex[i][1]]
                                tracker += 1
                                break

                        # If letter not equal, empty indexes to cause error in find letter statement
                        else:
                            indexes = []

        # Sort the final word list and print it to GUI
        hunted = set(hunted)
        hunted = sorted(hunted, key=len)
        print('Words Found:', len(hunted))
        print(hunted)
        for word in hunted:
            self.output.append(str(word))
        return hunted


def main():
    # Main GUI initialization
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()