import sys

DATA = []
EUCLIDIAN_MATRIX = []

def loadInstance(filename):
    file = open(filename, 'r')
    for line in file:
        lineSplited = line.split(" ")
        DATA.append((lineSplited[0],lineSplited[1],lineSplited[2].rstrip()))

def calculateMatrix():
    for data in DATA:
        print(data)

def generateInitialSolution():
    pass

def calculateCost():
    pass

def generateNeighbor():
    pass

def simulatedAnnealing():
    pass

db = sys.argv[1]

if db == 'base51':
    loadInstance('bases/base51.txt')
elif db == 'base100':
    loadInstance('bases/base100.txt')
else:
    print("Missing params")
    exit()

calculateMatrix()

# print(DATA[0])