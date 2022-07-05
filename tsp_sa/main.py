import sys
import math
import random
import pygame

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TSPSA:
    def __init__(self, filename, params = {}):
        self.params = params
        self.filename = filename
        self.euclidian_matrix = []
        self.first_solution = []
        self.solution_cords = []
        self.data = []
        self.fixed_points = []
    
    def defineFixedPoints(self):
        for i in self.data:
            self.fixed_points.append((i[1], i[2]))

    def drawFixedPoints(self, screen):
        for p in range(len(self.fixed_points)):
            x = int(self.fixed_points[p][0]) * 15.5
            y = int(self.fixed_points[p][1]) * 12.8
            pygame.draw.circle(surface = screen, color = (0,0,0), center = (x, y), radius = 10)

    def drawSolutionLines(self, screen):
        pygame.draw.lines(screen, (0,0,255), False, [(x[0]*15.5, x[1]*12.8) for x in self.solution_cords], width=2) 
        pygame.display.flip()

    def defineSolutionCords(self):
        for i in self.first_solution:
            for j in self.data:
                if int(j[0]) == i:
                    self.solution_cords.append((int(j[1]), int(j[2])))
        self.solution_cords.append(self.solution_cords[0])

    def loadInstance(self):
        print("Carregando base de dados...")
        file = open(self.filename, 'r')
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
        # print(self.first_solution)

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    screen.fill((255,255,255))

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
    objtsp.defineFixedPoints()
    objtsp.defineSolutionCords()
    objtsp.drawFixedPoints(screen)
    objtsp.drawSolutionLines(screen)

    while True:
        pass


main()
