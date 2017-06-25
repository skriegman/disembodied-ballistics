import numpy as np
from functools import partial
from problems import needle_in_a_haystack, time_on_needle
from replicators import Population

SEED = 1
np.random.seed(SEED)

MUT_RATE = 16/48.
DEVO = True

GENS = 1000
POP_SIZE = 30
NUM_RAND_INDS = 1
PROTECT_AGE = True
PAIRWISE = False
TIME_STEP = 1/10.
LENGTH = 4*4*3
INTERVAL = 1.2  # how close you have to be to the needle
NEEDLE = needle_in_a_haystack(LENGTH, INTERVAL)
FIT_FUNC = partial(time_on_needle, needle=NEEDLE, devo=DEVO, time_step=TIME_STEP)

pop = Population(POP_SIZE, LENGTH, FIT_FUNC, MUT_RATE)

for gen in range(GENS):
    pop.create_children_through_mutation()
    pop.add_random_inds(NUM_RAND_INDS)
    pop.increment_ages()
    pop.evaluate()
    pop.reduce(pairwise=PAIRWISE)
    pop.print_non_dominated()
    pop.gen += 1

    if pop.cache.fitness >= 1 - TIME_STEP:
        print "Found it!"
        break

print pop.cache.fitness

