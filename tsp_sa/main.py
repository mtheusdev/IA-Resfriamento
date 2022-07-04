import sys
import math
import random

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def main():
    if len(sys.argv) == 1:
        print("Error! Missing params (base)")
        exit()

    filename = "bases/"+sys.argv[1]+".txt"

    objtsp = TSPSA(filename)
    objtsp.loadInstance()
    objtsp.initializeMatrix()
    objtsp.calculateMatrix()
    objtsp.generateInitialSolution()
    objtsp.calculateCostFirstSolution()

class TSPSA:
    def __init__(self, filename, params = {}):
        self.params = params,
        self.filename = filename,
        self.euclidian_matrix = [],
        self.first_solution = [],
        self.data = []
    
    def loadInstance(self):
        print("Carregando base de dados...")
        file = open(self.filename[0], 'r')
        for line in file:
            lineSplited = line.split(" ")
            self.data.append((lineSplited[0],lineSplited[1],lineSplited[2].rstrip()))
        print(f"Base de dados carregada! '{self.filename[0]}'")

    def initializeMatrix(self):
        print("Inicializando matriz...")
        self.euclidian_matrix = [[' ' for _ in range(len(self.data))] for _ in range(len(self.data))]
        print(f"Matriz inicializada! {len(self.data)} x {len(self.data)}")
    
    def euclidianDistance(self, first_point, second_point):
        return round(math.sqrt(pow((first_point.x - second_point.x), 2) + pow((first_point.y - second_point.y), 2)),1)

    def calculateMatrix(self):
        print("Calculando matriz de distâncias Euclidianas...")
        for i in range(len(self.data)):
            first_index = int(self.data[i][0])
            first_point = point(int(self.data[i][1]), int(self.data[i][2]))
            for j in range(len(self.data)):
                second_index = int(self.data[j][0])
                second_point = point(int(self.data[j][1]), int(self.data[j][2]))
                if (i >= j):
                    self.euclidian_matrix[first_index][second_index] = self.euclidianDistance(first_point, second_point)
        print("Matriz de distâncias calculada!")
        # self.debugEuclidianMatrix()
    
    def debugEuclidianMatrix(self):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                print(self.euclidian_matrix[i][j], end=' ')
            print('')

    def generateInitialSolution(self):
        print("Gerando primeira solução válida aleatóriamente...")
        self.first_solution = random.sample(range(0,51), 51)
        print("Primeira solução válida gerada!")
        print(self.first_solution )

    def getDistanceByCityIndex(self, city_A, city_B):
        # print(city_A, city_B)
        # print(f"PESO ENTRE {city_A} e {city_B} eh {self.euclidian_matrix[city_A][city_B]}")
        return self.euclidian_matrix[city_A][city_B] if city_A > city_B else self.euclidian_matrix[city_B][city_A]

    def calculateCostFirstSolution(self):
        print("Calculando custo da primeira solução...")
        cost = 0
        solution_size = len(self.first_solution)
        for i in range(solution_size):
            first_city_of_sum = self.first_solution[i]
            if i == solution_size - 1:
                second_city_of_sum = self.first_solution[0]
            else:
                second_city_of_sum = self.first_solution[i+1]

            cost += self.getDistanceByCityIndex(first_city_of_sum, second_city_of_sum)

        print("Custo da primeira solução calculado:", cost)

    def calculateCost():
        pass

    def generateNeighbor():
        pass

    def simulatedAnnealing():
        pass

main()
