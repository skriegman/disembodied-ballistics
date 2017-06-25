import sys
import numpy as np
import pandas as pd
from functools import partial
from problems import needle_in_a_haystack, time_on_needle
from replicators import Population

# SEED = 1
# np.random.seed(SEED)
# DEVO = True
# INTERVAL = 0.5  # how close you have to be to the needle

SEED = int(sys.argv[1])

RUNS = 30
MUT_RATE = 24/48.
MUT_SCALE = 1

GENS = 2000
POP_SIZE = 30
NUM_RAND_INDS = 1
PROTECT_AGE = True
PAIRWISE = False
TIME_STEP = 1/40.
LENGTH = 4*4*3

data = []
for DEVO in [False, True]:

    for INTERVAL in np.arange(0, 2, 0.01):

        # for SEED in range(1, RUNS+1):
        print DEVO, INTERVAL, SEED

        np.random.seed(SEED)

        NEEDLE = needle_in_a_haystack(LENGTH, INTERVAL)
        FIT_FUNC = partial(time_on_needle, needle=NEEDLE, devo=DEVO, time_step=TIME_STEP)

        pop = Population(POP_SIZE, LENGTH, FIT_FUNC, MUT_RATE, MUT_SCALE)

        for gen in range(GENS):
            pop.create_children_through_mutation()
            pop.add_random_inds(NUM_RAND_INDS)
            pop.increment_ages()
            pop.evaluate()
            pop.reduce(pairwise=PAIRWISE)
            # pop.print_non_dominated()
            pop.gen += 1

            if pop.cache.fitness >= 1 - TIME_STEP:
                print "Found it!"
                break

        print pop.cache.fitness

        if DEVO:
            name = "Evo-Devo"
        else:
            name = "Evo"
        data += [(name, INTERVAL, SEED, pop.gen)]


df = pd.DataFrame(data=data, columns=["Group", "Interval", "Run", "Time"])

df.to_csv("results_{}.csv".format(SEED))
