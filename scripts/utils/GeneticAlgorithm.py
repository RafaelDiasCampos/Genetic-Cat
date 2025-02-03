import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size: int, n_generations: int, 
                 crossover_rate: float, mutation_rate: float, 
                 elitism: int, tournament_size: int, 
                 fitness_function: callable, crossover_function: callable, mutation_function: callable):
        self.population_size = population_size
        self.n_generations = n_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.tournament_size = tournament_size
        self.fitness_function = fitness_function
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function
        
        self.run_stats = {
            "max_fitness": [],
            "min_fitness": [],
            "avg_fitness": [],
            "best_individual": []
        }
        
    def run(self, initial_population: np.array, verbose=False) -> np.array:
        self.current_population = initial_population
        
        if verbose:
            print(f"Starting execution")
        
        for i in range(self.n_generations):
            if verbose:
                print(f"Generation {i + 1}")
            self.evolve()
    
    def evolve(self) -> np.array:
        # Calculate the fitness of the current population
        population = [ { "individual": individual, "fitness": self.fitness_function(individual) } for individual in self.current_population ]
        
        # Save the statistics
        self.run_stats["max_fitness"].append(sorted(population, key = lambda x: x["fitness"], reverse = True)[0]["fitness"])
        self.run_stats["min_fitness"].append(sorted(population, key = lambda x: x["fitness"])[0]["fitness"])
        self.run_stats["avg_fitness"].append(np.mean([individual["fitness"] for individual in population]))
        self.run_stats["best_individual"].append(sorted(population, key = lambda x: x["fitness"], reverse = True)[0]["individual"])
        
        # Initialize the new population
        new_population = []
        
        # Create new individuals
        while len(new_population) < self.population_size:            
            # Select individuals for the tournament
            tournament = np.random.choice(population, size = self.tournament_size, replace = False)
            
            # Choose the best individuals
            parents = sorted(tournament, key = lambda x: x["fitness"], reverse = True)[:2]
            
            # Do the crossover
            if np.random.rand() < self.crossover_rate:
                children = self.crossover_function(parents[0]["individual"], parents[1]["individual"])
                new_population.extend(children)
            
                
            # Do the mutation
            if np.random.rand() < self.mutation_rate:
                children = [ self.mutation_function(parent["individual"]) for parent in parents ]
                new_population.extend(children)
        
        # Add the best individuals to the new population (elitism)
        best_individuals = sorted(population, key = lambda x: x["fitness"], reverse = True)[:self.elitism]        
        new_population.extend([individual["individual"] for individual in best_individuals])
        
        # Update the population
        self.current_population = new_population

    
    def __str__(self):
        return f"GA(population_size = {self.population_size}, n_generations = {self.n_generations}, crossover_rate = {self.crossover_rate}, mutation_rate = {self.mutation_rate}, elitism = {self.elitism}, tournament_size = {self.tournament_size})"