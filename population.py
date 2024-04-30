import gamereqs
import math
import operator
import species

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        for i in range(0, self.size, 1):
            self.players.append(gamereqs.Player())

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(gamereqs.window)
                p.update(gamereqs.ground)

    # Function begins a natural selection cycle, calling all genome culling methods
    def natural_selection(self):
        print("NEW NATURAL SELECTION CYCLE: ")

        print('func call: SPECIATE')
        self.speciate()

        print('func call: CALCULATE FITNESS')
        self.calculate_fitness()

        print('func call: KILL EXTINCT')
        self.kill_extinct_species()

        print('func call: KILL STALE')
        self.kill_stale_species()

        print('func call: SORT BY FITNESS')
        self.sort_species_by_fitness()

        print('func call: CHILDREN FOR NEXT GEN')
        self.next_gen()

    # Function splits the population into different species.
    # The grouping is determined by the similarity of weights on their connections
    def speciate(self):
        for s in self.species:
            s.players = []

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    # Function determines fitness level
    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_extinct_species(self):
        species_bin = []
        for s in self.species:
            if len(s.players) == 0:
                species_bin.append(s)
        for s in species_bin:
            self.species.remove(s)

    def kill_stale_species(self):
        player_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)

    # Function sorts all players in a species by fitness
    # then, sports all species within population by average fitness
    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)

    # Children are created through mutations in weights of neural network connections
    def next_gen(self):
        children = []

        # Clone of champion is added to each species
        for s in self.species:
            children.append(s.champion.clone())

        # Fill open player slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1

    # Return true if all players are dead
    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct