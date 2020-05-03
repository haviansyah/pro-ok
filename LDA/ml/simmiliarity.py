from gensim import similarities
import gensim
import numpy as np
import scipy.stats


def jensen_shannon_distance(p, q):
    """
    method to compute the Jenson-Shannon Distance
    between two probability distributions
    """
    # convert the vectors into numpy arrays in case that they aren't
    p = np.array(p)
    q = np.array(q)
    # calculate m
    m = (p + q) / 2
    # compute Jensen Shannon Divergence
    divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2
    # compute the Jensen Shannon Distance
    distance = np.sqrt(divergence)
    return distance[1]

def cossine(p,q):
    sims = gensim.matutils.cossim(p, q)
    return sims

