import sys
import math
import random
import pygame
import matplotlib.pyplot as plt
from numpy import log as ln

class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TSPSA:
    def __init__(self, filename, db, screen, params = {}):
        self.params = params
        self.filename = filename
        self.euclidian_matrix = []
        self.best_solution = []
        self.solution_s = []
        self.solution_s_line = []
        self.solution_cords = []
        self.best_cost_graphic_array = []
        self.data = []
        self.iteration_graphic_array = []
        self.temperature_graphic_array = []
        self.lenData = 0
        self.fixed_points = []
        self.db = db
        self.best_cost = 0
        self.cost_s = 0
        self.cost_s_line = 0
        self.screen = screen
        self.temperature = []
        self.iteration = []
        self.thermal_equilibrium = params[1]
        self.T0 = params[2] # Temperatura inicial
        self.Ti = params[2] # Temperatura na iteração
        self.N = params[0]  # Número máximo de iterações
        self.Tn = 0.1       # Temperatura Final
        self.I = 0          # Número da iteração
        self.current_formula = ''
    
    def defineFixedPoints(self):
        # print(len(self.data))
        # print("Definindo pontos...")
        for i in self.data:
            self.fixed_points.append((i[1], i[2]))

    def drawFixedPoints(self):
        # print("Desenhando pontos fixos...")
        for p in range(len(self.fixed_points)):
            if self.db == 'base51':
                x = int(self.fixed_points[p][0]) * 15.5
                y = int(self.fixed_points[p][1]) * 13
            else:
                x = int(self.fixed_points[p][0]) / 2.65
                y = int(self.fixed_points[p][1]) / 2.08
            pygame.draw.circle(surface = self.screen, color = (0,0,0), center = (x, y), radius = 10)
        # print("Pontos desenhados!")

    def resetSolutionCords(self):
        self.solution_cords.clear()
        # print("resetando solution cords", self.solution_cords)

    def drawSolutionLines(self):
        # print("Desenhando arestas de solução...")
        if self.db == 'base51':
            pygame.draw.lines(self.screen, (0,0,255), False, [(x[0] * 15.5, x[1] * 13) for x in self.solution_cords], width=2) 
        else:
            pygame.draw.lines(self.screen, (0,0,255), False, [(x[0] / 2.65, x[1] / 2.08) for x in self.solution_cords], width=2) 
        pygame.display.flip()
        # print("Arestas desenhadas!")

    def defineSolutionCords(self):
        # print("Definindo cordenadas de solução...")
        for i in self.best_solution:
            for j in self.data:
                if int(j[0]) == i:
                    self.solution_cords.append((int(j[1]), int(j[2])))
        self.solution_cords.append(self.solution_cords[0])
        # print("Solution Cords:", self.solution_cords)

    def loadInstance(self):
        # print("Carregando base de dados...")
        file = open(self.filename, 'r')
        for line in file:
            lineSplited = line.split(" ")
            self.data.append((lineSplited[0],lineSplited[1],lineSplited[2].rstrip()))
        self.lenData = len(self.data)
        # print(f"Base de dados carregada! '{self.filename[0]}'")

    def initializeMatrix(self):
        # print("Inicializando matriz...")
        self.euclidian_matrix = [[' ' for _ in range(self.lenData)] for _ in range(self.lenData)]
        # print(f"Matriz inicializada! {self.lenData} x {self.lenData}")
    
    def euclidianDistance(self, first_point, second_point):
        return round(math.sqrt(pow((first_point.x - second_point.x), 2) + pow((first_point.y - second_point.y), 2)),1)

    def calculateMatrix(self):
        # print("Calculando matriz de distâncias Euclidianas...")
        for i in range(self.lenData):
            first_index = int(self.data[i][0])
            first_point = point(int(self.data[i][1]), int(self.data[i][2]))
            for j in range(self.lenData):
                second_index = int(self.data[j][0])
                second_point = point(int(self.data[j][1]), int(self.data[j][2]))
                if (i >= j):
                    self.euclidian_matrix[first_index][second_index] = self.euclidianDistance(first_point, second_point)
        # print("Matriz de distâncias calculada!")
    
    def debugEuclidianMatrix(self):
        for i in range(self.lenData):
            for j in range(self.lenData):
                print(self.euclidian_matrix[i][j], end=' ')
            # print('')

    def generateInitialSolution(self):
        # print("Gerando primeira solução válida aleatóriamente...")
        self.best_solution = random.sample(range(0,self.lenData), self.lenData)
        # print("Primeira solução válida gerada!")
        # print("Primeira solução:", self.best_solution)

    def getDistanceByCityIndex(self, city_A, city_B):
        return self.euclidian_matrix[city_A][city_B] if city_A > city_B else self.euclidian_matrix[city_B][city_A]

    def calculateCostFirstSolution(self):
        # print("Calculando custo da primeira solução...")
        cost = 0
        solution_size = len(self.best_solution)
        for i in range(solution_size):
            first_city_of_sum = self.best_solution[i]
            if i == solution_size - 1:
                second_city_of_sum = self.best_solution[0]
            else:
                second_city_of_sum = self.best_solution[i+1]
            cost += self.getDistanceByCityIndex(first_city_of_sum, second_city_of_sum)

        self.best_cost = cost
        # print("Retornando custo da primeira solução...")

    def calculateCost(self, arraySolution):
        # print("Calculando custo da solução...")
        cost = 0
        solution_size = len(arraySolution)
        for i in range(solution_size):
            first_city_of_sum = arraySolution[i]
            if i == solution_size - 1:
                second_city_of_sum = arraySolution[0]
            else:
                second_city_of_sum = arraySolution[i+1]
            cost += self.getDistanceByCityIndex(first_city_of_sum, second_city_of_sum)

        # print("Retornando custo da solução...")
        return cost

    def generateNeighbor(self):
        self.solution_s_line = self.solution_s.copy()
        swaps_qtd = self.generateDisturbanceQuantity()

        for i in range(swaps_qtd):
            neighbor1ID, neighbor2ID = self.generatePairOfIDNeighbors()
            primeiro = self.solution_s_line[neighbor1ID]
            segundo = self.solution_s_line[neighbor2ID]
            self.solution_s_line[neighbor2ID] = primeiro
            self.solution_s_line[neighbor1ID] = segundo

    def routineUpdateScreen(self):
        self.screen.fill((255,255,255))
        self.drawFixedPoints()
        self.resetSolutionCords()
        self.defineSolutionCords()
        self.drawSolutionLines()
        pygame.display.flip()

    def plotGraphicTempByItr(self):
        plt.plot(self.iteration_graphic_array, self.temperature_graphic_array)
        plt.title("Temperatura por Iteração - " + self.current_formula)
        plt.xlabel('Iterações')
        plt.ylabel('Temperatura')
        plt.savefig("temp_by_itr_"+str(round(self.best_cost))+"_"+self.current_formula+"_"+str(self.N)+"_"+str(self.T0)+'.png')
        plt.figure().clear()

    def plotGraphicCostByItr(self):
        plt.plot(self.iteration_graphic_array, self.best_cost_graphic_array)
        plt.title("Custo por Iteração- " + self.current_formula)
        plt.xlabel('Iterações')
        plt.ylabel('Custo')
        plt.savefig("cost_by_itr_"+str(round(self.best_cost))+"_"+self.current_formula+"_"+str(self.N)+"_"+str(self.T0)+'.png')
        plt.figure().clear()

    def plotGraphicCostByTemp(self):
        self.best_cost_graphic_array = list(reversed(self.best_cost_graphic_array))
        plt.plot(self.best_cost_graphic_array,self.temperature_graphic_array)
        plt.title("Temperatura pelo Custo - " + self.current_formula)
        plt.xlabel('Custo')
        plt.ylabel('Temperatura')
        plt.savefig("temp_by_cost_"+str(round(self.best_cost))+"_"+self.current_formula+"_"+str(self.N)+"_"+str(self.T0)+'.png')
        plt.figure().clear()

    def generatePairOfIDNeighbors(self):
        return random.randint(0, self.lenData - 1), random.randint(0, self.lenData - 1)

    def generateDisturbanceQuantity(self):
        return random.randint(1, 5)

    def coolingFormula_1(self):
        self.current_formula = "Formula_1"
        self.Ti = self.T0 * pow((self.Tn/self.T0), self.I/self.N)

    def coolingFormula_2(self):
        A = ((self.T0 - self.Tn) * (self.N + 1)) / self.N
        B = self.T0 - A
        self.Ti = (A/(self.I+1)) + B
        self.current_formula = "Formula_2"

    def coolingFormula_7(self):
        self.current_formula = "Formula_7"
        self.Ti = ((self.T0 - self.Tn) / math.cosh((10*self.I)/self.N)) + self.Tn

    def coolingFormula_8(self):
        self.current_formula = "Formula_8"
        A = (1/self.N) * ln(self.T0/self.Tn)
        self.Ti = self.T0 * pow(math.e, (-A * self.I))

    def takeScreeshot(self):
        pygame.image.save(self.screen,"FIG_"+str(round(self.best_cost))+"_"+self.current_formula+"_"+str(self.N)+"_"+str(self.T0)+'.jpg')

    def routineIterationSimulatedAnnealing(self):
        self.coolingFormula_1()
        self.temperature_graphic_array.append(self.Ti)
        self.I += 1
        self.iteration_graphic_array.append(self.I)
        self.best_cost_graphic_array.append(self.best_cost)
        self.routineUpdateScreen()

    def simulatedAnnealing(self):
        self.solution_s = self.best_solution.copy()

        while self.I < self.N:
            for i in range(self.thermal_equilibrium):
                self.generateNeighbor()
                new_cost = self.calculateCost(self.solution_s_line)
                previous_cost = self.calculateCost(self.solution_s)
                delta = new_cost - previous_cost
                if delta < 0: # Custo da nova solução é menor, trocar
                    self.solution_s = self.solution_s_line.copy()
                    if new_cost < self.best_cost:
                        # print("Mudei a tela")
                        self.best_solution = self.solution_s_line.copy()
                        self.best_cost = new_cost
                else: # Custo é maior, estocasticidade
                    x = random.random() # Aleatório entre 0 e 1
                    if x < pow(math.e, - delta/self.Ti):
                        self.solution_s = self.solution_s_line.copy()
                # print(self.best_cost)
                self.routineIterationSimulatedAnnealing()
    

def main():
    if len(sys.argv) == 1:
        # print("Error! Missing params (base)")
        exit()

    parameters = [100000,5,50] if sys.argv[1] == 'base51' else [100000,5,100] # parameters = [QTD_ITERAÇÕES, EQUILIBRIO TERMICO, TEMPERATURA_INICIAL]
    resolution = [1024, 1024] if sys.argv[1] == 'base51' else [1500, 1024]

    pygame.init()
    screen = pygame.display.set_mode((resolution[0], resolution[1]))
    screen.fill((255,255,255))

    filename = "bases/"+sys.argv[1]+".txt"


    objtsp = TSPSA(filename, sys.argv[1], screen, parameters)
    objtsp.loadInstance()
    objtsp.initializeMatrix()
    objtsp.calculateMatrix()
    objtsp.generateInitialSolution()
    objtsp.calculateCostFirstSolution()
    objtsp.defineFixedPoints()
    objtsp.defineSolutionCords()
    objtsp.drawFixedPoints()
    objtsp.drawSolutionLines()
    objtsp.simulatedAnnealing()
    objtsp.routineUpdateScreen()
    objtsp.takeScreeshot()
    objtsp.plotGraphicTempByItr()
    objtsp.plotGraphicCostByItr()
    objtsp.plotGraphicCostByTemp()

main()
