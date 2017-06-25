import numpy as np


def needle_in_a_haystack(length, interval=0.1):
    needle = np.random.random(length)
    return np.array([needle-interval, needle+interval])


def time_on_needle(genome, needle, devo=False, time_step=0.001):
    if not devo:
        if (needle[0] < genome).all() and (genome < needle[1]).all():
            return 1.0
        else:
            return 0.0
    else:
        score = 0
        for t in np.arange(0, 1, time_step):
            this_genome = genome[0] + t * (genome[1]-genome[0])
            if (needle[0] < this_genome).all() and (this_genome < needle[1]).all():
                score += time_step
        return score
