import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from collections import Counter

board = [['a','b','c','d'], ['a','b','c','d'], ['a','b','c','d'], ['a','b','c','d']]
letterDistribution = ['A','A','A','A','A','A','A','A','A','B','B','C','C','D','D','D','D','E','E','E','E','E','E','E',
                      'E','E','E','E','E','F','F','G','G','G','H','H','I','I','I','I','I','I','I','I','I','J','K','L',
                      'L','L','L','M','M','N','N','N','N','N','N','O','O','O','O','O','O','O','O','P','P','Q','R','R',
                      'R','R','R','R','S','S','S','S','T','T','T','T','T','T','U','U','U','U','V','V','W','W','X','Y',
                      'Y','Z']

# 2d array board
boardletters = str()
# 2d array board
for i in range(4):
    for j in range(4):
        board[i][j] = letterDistribution[np.random.randint(len(letterDistribution))]
        boardletters += board[i][j]
print('Board:\n', board[0], '\n', board[1], '\n', board[2], '\n', board[3])


file = open('Collins Scrabble Words (2019).txt')
dictionary = file.read().split()
print('Words in Dictionary:', len(dictionary))

def firstFilter(dictionary, board):
    initFilter = []
    for i in range(len(dictionary)):
        tracker = 0
        if len(dictionary[i]) >= 3 or len(dictionary[i]) <= 16:
            for j in range(len(board)):
                for k in range(len(board[j])):
                    letter = board[j][k]
                    check = dictionary[i].rfind(letter)
                    if check != -1:
                        tracker += 1
            if tracker >= len(dictionary[i]):
                initFilter.append(dictionary[i])
    initFilter = sorted(initFilter, key=len, reverse=True)
    print('Words available:', len(initFilter))
    return initFilter


def issubset_replicate(A, B):
    '''check if A is a subset of B'''
    return Counter(A) - Counter(B) == Counter()

def NextLetters(x, i, j):
    # x is the board
    # i is the first index
    # j is the second index
    NextLetterlist = []
    # if either index is <0 or >4 then it should not be appended
    m, n = i - 1, j - 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i - 1, j
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i - 1, j + 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i, j + 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i + 1, j + 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i + 1, j
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i + 1, j - 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    m, n = i, j - 1
    if 0 <= m <= 3 and 0 <= n <= 3:
        NextLetterlist.append(x[m][n])

    return NextLetterlist


def Solver(initFilter):
    hunted = []
    for word in initFilter:
        print(word)
        firstLetter = word[0]
        tracker = 1
        initIndex = []
        for i in range(len(board)):
            initIndex.append([])
            for tile in board[i]:
                if tile == firstLetter:
                    initIndex[i].append(i)
                    initIndex[i].append(board[i].index(tile))
        initIndex = [ele for ele in initIndex if ele != []]
        print(initIndex)
        for startpoint in initIndex:
            print(startpoint)
            ind1 = startpoint[0]
            ind2 = startpoint[1]
            while True:
                if tracker >= len(word):
                    hunted.append(word)
                    break
                nextLetter = NextLetters(board, ind1, ind2)
                print('Next Letters:', nextLetter)
                if len(nextLetter) == 0:
                    break
                else:
                    ind1 = nextLetter[0]
                    ind2 = nextLetter[1]
                    tracker += 1
    return hunted

initFilter = []
for word in dictionary:
    if issubset_replicate(word, boardletters):
        initFilter.append(word)

hunted = Solver(initFilter)




