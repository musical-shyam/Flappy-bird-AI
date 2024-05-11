import random
import operator

class Species:
    def __init__(self, player):
        self.players = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.benchmark_fitness = player.fitness # Fitness of the best player in the species
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0

    # Compares benchmark brain of Specie & the passed in brain.
    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    # Difference of connection weights of both brains
    @staticmethod
    def weight_difference(brain_1, brain_2):
        total_weight_difference = 0
        for i in range(0, len(brain_1.connections)): # Compares the weights of the connections of the two brains(assuming they have the same number of connections)
            total_weight_difference += abs(brain_1.connections[i].weight - brain_2.connections[i].weight)
        return total_weight_difference

    # Adds the specimen to the species of the passed in player
    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))

        else:
            self.average_fitness = 0

    def offspring(self):
        baby = self.players[random.randint(1, len(self.players)) - 1].clone()
        baby.brain.mutate()
        return baby