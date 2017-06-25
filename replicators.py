import numpy as np
from copy import deepcopy


class Individual(object):
    def __init__(self, idx, length, devo=False):
        size = length
        if devo:
            size = (2, length)

        self.length = length
        self.devo = devo
        self.genome = 2 * np.random.random(size) - 1
        self.id = idx
        self.fitness = 0
        self.age = 0
        self.dominated_by = []
        self.pareto_level = 0
        self.already_evaluated = False

    def __iter__(self):
        """Iterate over the genome. Use the expression 'for n in ind'."""
        return np.nditer(self.genome, flags=['external_loop', 'buffered'])

    def __len__(self):
        """Return the length of the genotype. Use the expression 'len(ind)'."""
        return len(self.genome)

    def __getitem__(self, n):
        """Return gene n.  Use the expression 'ind[n]'."""
        return self.genome[n]

    def __setitem__(self, n, val):
        """Set gene n to val. Use the expression 'ind[n]=val'."""
        self.genome[n] = val

    def mutate(self, new_id, prob=None, scale=None):
        if prob is None:
            prob = 1 / float(len(self))

        if scale is None:
            scale = np.abs(self.genome+1)

        change = np.random.normal(scale=scale)
        new = np.clip(self.genome + change, -1, 1)

        if not self.devo:
            selection = np.random.random(len(self)) < prob
            self[selection] = new[selection]
        else:
            choice = [False, False]
            while np.sum(choice) == 0:
                choice = np.random.random(2) < 0.5

            if choice[0]:
                selection = np.random.random(self.length) < prob
                self[0, selection] = new[0, selection]
            if choice[1]:
                selection = np.random.random(self.length) < prob
                self[1, selection] = new[1, selection]

        self.id = new_id
        self.already_evaluated = False

    def compute_fitness(self, fitness_func):
        self.fitness = fitness_func(self.genome)

    def dominates(self, other, protect_age=True):
        ages = [self.age, other.age]
        if not protect_age:
            ages = [0, 0]

        if self.fitness > other.fitness and ages[0] <= ages[1]:
            return True

        elif self.fitness == other.fitness and ages[0] < ages[1]:
            return True

        elif self.fitness == other.fitness and ages[0] == ages[1] and self.id < other.id:
            return True

        else:
            return False


class Population(object):
    def __init__(self, size, ind_length, fitness_func, mut_rate=None, mut_scale=None, protect_age=True):
        self.size = size
        self.ind_length = ind_length
        self.fitness_func = fitness_func
        self.protect_age = protect_age
        self.mut_rate = mut_rate
        self.mut_scale = mut_scale
        self.gen = 0
        self.individuals_dict = {}
        self.max_id = 0
        self.non_dominated_size = 0
        self.pareto_levels = {}
        self.add_random_inds(size)
        self.cache = self.individuals_dict[0]
        self.evaluate()

    def print_non_dominated(self):
        best_living = np.max([ind.fitness for key, ind in self.individuals_dict.items()])
        print self.gen, self.pareto_levels[0]

    def evaluate(self):
        for key, ind in self.individuals_dict.items():
            if not ind.already_evaluated:
                ind.compute_fitness(self.fitness_func)

                if ind.fitness > self.cache.fitness:
                    self.cache = ind

    def create_children_through_mutation(self):
        for key, parent in self.individuals_dict.items():
            child = deepcopy(parent)
            child.mutate(self.max_id, self.mut_rate, self.mut_scale)
            child.already_evaluated = False
            self.individuals_dict[self.max_id] = child
            self.max_id += 1

    def increment_ages(self):
        for key, ind in self.individuals_dict.items():
            ind.age += 1

    def add_random_inds(self, num_random=1):
        for _ in range(num_random):
            self.individuals_dict[self.max_id] = Individual(self.max_id, self.ind_length)
            self.max_id += 1

    def update_dominance(self):
        for key, ind in self.individuals_dict.items():
            ind.dominated_by = []

        for key1, ind1 in self.individuals_dict.items():
            for key2, ind2 in self.individuals_dict.items():
                if key1 != key2:
                    if self.individuals_dict[key1].dominates(self.individuals_dict[key2], self.protect_age):
                        self.individuals_dict[key2].dominated_by += [key1]

        self.non_dominated_size = 0
        self.pareto_levels = {}
        for key, ind in self.individuals_dict.items():
            ind.pareto_level = len(ind.dominated_by)
            if ind.pareto_level in self.pareto_levels:
                self.pareto_levels[ind.pareto_level] += [(ind.id, ind.fitness, ind.age)]
            else:
                self.pareto_levels[ind.pareto_level] = [(ind.id, ind.fitness, ind.age)]
            if ind.pareto_level == 0:
                self.non_dominated_size += 1

    def reduce(self, pairwise=False):
        self.update_dominance()

        if pairwise:  # reduce by calculating pairwise dominance (least pressure, most diversity)

            while len(self.individuals_dict) > self.size and len(self.individuals_dict) > self.non_dominated_size:
                current_ids = [idx for idx in self.individuals_dict]
                np.random.shuffle(current_ids)
                inds_to_remove = []
                for idx in range(1, len(self.individuals_dict)):
                    this_id = current_ids[idx]
                    previous_id = current_ids[idx - 1]
                    if self.individuals_dict[previous_id].dominates(self.individuals_dict[this_id], self.protect_age):
                        inds_to_remove += [this_id]
                for key in inds_to_remove:
                    del self.individuals_dict[key]

        else:  # add by pareto level until full

            children = {}
            for level in sorted(self.pareto_levels):
                sorted_level = sorted(self.pareto_levels[level], key=lambda x: x[1], reverse=True)
                for idx, fit, age in sorted_level:
                    if len(children) < self.size:
                        children[idx] = self.individuals_dict[idx]
            self.individuals_dict = children
