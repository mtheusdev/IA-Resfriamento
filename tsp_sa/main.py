import sys
import math
import random
import pygame

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TSPSA:
    def __init__(self, filename, db, params = {}):
        self.params = params
        self.filename = filename
        self.euclidian_matrix = []
        self.first_solution = []
        self.solution = []
        self.solution_TMP = []
        self.solution_cords = []
        self.data = []
        self.lenData = 0
        self.fixed_points = []
        self.db = db
        self.best_cost = 0
    
    def defineFixedPoints(self):
        # print(len(self.data))
        print("Definindo pontos...")
        for i in self.data:
            self.fixed_points.append((i[1], i[2]))

    def drawFixedPoints(self, screen):
        print("Desenhando pontos fixos...")
        for p in range(len(self.fixed_points)):
            if self.db == 'base51':
                x = int(self.fixed_points[p][0]) * 15.5
                y = int(self.fixed_points[p][1]) * 13
            else:
                x = int(self.fixed_points[p][0]) / 2.65
                y = int(self.fixed_points[p][1]) / 2.08
            pygame.draw.circle(surface = screen, color = (0,0,0), center = (x, y), radius = 10)
        print("Pontos desenhados!")

    def drawSolutionLines(self, screen):
        print("Desenhando arestas de solução...")
        if self.db == 'base51':
            pygame.draw.lines(screen, (0,0,255), False, [(x[0] * 15.5, x[1] * 13) for x in self.solution_cords], width=2) 
        else:
            pygame.draw.lines(screen, (0,0,255), False, [(x[0] / 2.65, x[1] / 2.08) for x in self.solution_cords], width=2) 
        pygame.display.flip()
        print("Arestas desenhadas!")

    def defineSolutionCords(self):
        print("Definindo cordenadas de solução...")
        for i in self.solution:
            for j in self.data:
                if int(j[0]) == i:
                    self.solution_cords.append((int(j[1]), int(j[2])))
        self.solution_cords.append(self.solution_cords[0])
        # print("Solution Cords:", self.solution_cords)

    def loadInstance(self):
        print("Carregando base de dados...")
        file = open(self.filename, 'r')
        for line in file:
            lineSplited = line.split(" ")
            self.data.append((lineSplited[0],lineSplited[1],lineSplited[2].rstrip()))
        self.lenData = len(self.data)
        print(f"Base de dados carregada! '{self.filename[0]}'")

    def initializeMatrix(self):
        print("Inicializando matriz...")
        self.euclidian_matrix = [[' ' for _ in range(self.lenData)] for _ in range(self.lenData)]
        print(f"Matriz inicializada! {self.lenData} x {self.lenData}")
    
    def euclidianDistance(self, first_point, second_point):
        return round(math.sqrt(pow((first_point.x - second_point.x), 2) + pow((first_point.y - second_point.y), 2)),1)

    def calculateMatrix(self):
        print("Calculando matriz de distâncias Euclidianas...")
        for i in range(self.lenData):
            first_index = int(self.data[i][0])
            first_point = point(int(self.data[i][1]), int(self.data[i][2]))
            for j in range(self.lenData):
                second_index = int(self.data[j][0])
                second_point = point(int(self.data[j][1]), int(self.data[j][2]))
                if (i >= j):
                    self.euclidian_matrix[first_index][second_index] = self.euclidianDistance(first_point, second_point)
        print("Matriz de distâncias calculada!")
    
    def debugEuclidianMatrix(self):
        for i in range(self.lenData):
            for j in range(self.lenData):
                print(self.euclidian_matrix[i][j], end=' ')
            print('')

    def generateInitialSolution(self):
        print("Gerando primeira solução válida aleatóriamente...")
        solution = random.sample(range(0,self.lenData), self.lenData)
        self.first_solution = solution
        self.solution = solution
        print("Primeira solução válida gerada!")
        # print("Primeira solução:", self.first_solution)

    def getDistanceByCityIndex(self, city_A, city_B):
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
        self.best_cost = cost
        print("Custo da primeira solução calculado:", cost)

    def calculateCost(self, arraySolution):
        print("Calculando custo da nova solução...")
        cost = 0
        solution_size = len(arraySolution)
        for i in range(solution_size):
            first_city_of_sum = arraySolution[i]
            if i == solution_size - 1:
                second_city_of_sum = arraySolution[0]
            else:
                second_city_of_sum = arraySolution[i+1]
            cost += self.getDistanceByCityIndex(first_city_of_sum, second_city_of_sum)
        print("Retornando custo da nova solução...")
        return cost

    def generateNeighbor(self):
        self.solution_TMP = self.solution.copy()
        swaps_qtd = self.generateDisturbanceQuantity()

        for i in range(swaps_qtd):
            neighbor1ID, neighbor2ID = self.generatePairOfIDNeighbors()
    
            primeiro = self.solution_TMP[neighbor1ID]
            segundo = self.solution_TMP[neighbor2ID]

            print(primeiro, segundo)

            self.solution_TMP[neighbor2ID] = primeiro
            self.solution_TMP[neighbor1ID] = segundo

        print("SOLUÇÃO INICIAL", self.solution)
        print("NOVA SOLUÇÃO   ", self.solution_TMP)

    def generatePairOfIDNeighbors(self):
        return random.randint(0, self.lenData - 1), random.randint(0, self.lenData - 1)

    def generateDisturbanceQuantity(self):
        return random.randint(1, 5)

    def simulatedAnnealing(self):
        self.generateNeighbor()

def main():

    # PARAMETROS PARA MUDAR ENTRE AS BASES: TAMANHO DA TELA DO PYGAME E MULTIPLICAÇÃO/DIVISÃO DOS VALORES NA FUNÇÃO drawFixedPoints

    if len(sys.argv) == 1:
        print("Error! Missing params (base)")
        exit()
    
    resolution = [1024, 1024] if sys.argv[1] == 'base51' else [1500, 1024]

    pygame.init()
    screen = pygame.display.set_mode((resolution[0], resolution[1]))
    screen.fill((255,255,255))

    filename = "bases/"+sys.argv[1]+".txt"

    objtsp = TSPSA(filename, sys.argv[1])
    objtsp.loadInstance()
    objtsp.initializeMatrix()
    objtsp.calculateMatrix()
    objtsp.generateInitialSolution()
    objtsp.calculateCostFirstSolution()
    objtsp.defineFixedPoints()
    objtsp.defineSolutionCords()
    objtsp.drawFixedPoints(screen)
    objtsp.drawSolutionLines(screen)
    objtsp.simulatedAnnealing()

    while True:
        pass


main()
