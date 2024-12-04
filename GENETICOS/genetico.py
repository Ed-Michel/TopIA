import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Definir la función fitness
def fitness_func(individual):
    x, y = individual
    return x**2 + y**2  # La idea es maximizar esta función

# Clase para el Algoritmo Genético
class GeneticAlgorithm:
    def __init__(self, n_genes, n_iterations, gene_limits, mutation_rate, crossover_rate):
        self.n_genes = n_genes
        self.n_iterations = n_iterations
        self.gene_limits = gene_limits
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = self._initialize_population()
        self.best_fitness_evolution = []
    
    # Inicialización aleatoria de la población
    def _initialize_population(self):
        return np.random.uniform(self.gene_limits[0], self.gene_limits[1], (self.n_genes, 2))
    
    # Obtener los puntajes de fitness para la población
    def get_fitness_scores(self):
        return np.array([fitness_func(ind) for ind in self.population])
    
    # Selección por ruleta
    def _select_parents(self, fitness_scores):
        prob = fitness_scores / fitness_scores.sum()
        parents_indices = np.random.choice(range(self.n_genes), size=self.n_genes, p=prob)
        return self.population[parents_indices]
    
    # Cruce de dos puntos
    def _crossover(self, parent1, parent2):
        if np.random.rand() < self.crossover_rate:
            crossover_point = np.random.randint(1, len(parent1))
            child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
            child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
            return child1, child2
        return parent1, parent2
    
    # Mutación
    def _mutate(self, individual):
        for i in range(len(individual)):
            if np.random.rand() < self.mutation_rate:
                individual[i] = np.random.uniform(self.gene_limits[0], self.gene_limits[1])
        return individual
    
    # Optimización del algoritmo genético
    def optimize(self):
        for iteration in tqdm(range(self.n_iterations)):
            fitness_scores = self.get_fitness_scores()
            self.best_fitness_evolution.append(fitness_scores.max())
            selected_parents = self._select_parents(fitness_scores)
        
            # Generar nueva población mediante cruce y mutación
            new_population = []
            for i in range(0, self.n_genes, 2):
                parent1, parent2 = selected_parents[i], selected_parents[i+1]
                child1, child2 = self._crossover(parent1, parent2)
                new_population.append(self._mutate(child1))
                new_population.append(self._mutate(child2))
        
            self.population = np.array(new_population)
        
            # Imprimir la población cada 10 iteraciones
            if iteration % 10 == 0:
                print(f"\nPoblación en la iteración {iteration}:")
                print(self.population)
    
        # Evaluar la mejor solución
        fitness_scores = self.get_fitness_scores()
        best_index = np.argmax(fitness_scores)
        best_solution = self.population[best_index]
    
        return best_solution, fitness_scores[best_index]
    
    # Visualizar la evolución de la fitness
    def view_fitness_evolution(self):
        plt.plot(self.best_fitness_evolution)
        plt.title('Evolución del mejor Fitness')
        plt.xlabel('Iteraciones')
        plt.ylabel('Fitness')
        plt.show()

# Parámetros del algoritmo
n_genes = 20            # Tamaño de la población
n_iterations = 100      # Número de iteraciones
gene_limits = [-10, 10] # Límites de los genes (x, y)
mutation_rate = 0.1     # Tasa de mutación
crossover_rate = 0.7    # Tasa de cruce

# Inicializar y ejecutar el algoritmo genético
ga = GeneticAlgorithm(
    n_genes=n_genes, 
    n_iterations=n_iterations, 
    gene_limits=gene_limits, 
    mutation_rate=mutation_rate, 
    crossover_rate=crossover_rate
)

best_solution, best_fitness = ga.optimize()
print(f"Mejor solución: {best_solution}, con fitness: {best_fitness}")
ga.view_fitness_evolution()