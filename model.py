import numpy as np
from hmmlearn import hmm
from utils import get_transmat, get_emissionprobs, get_t1_t2


def setup_model(tau, t01, t12, t_admix):
    """
    Set up the HMM model.
    :param tau: introgression probability.
    :param t1: refer to figure.
    :param t2: refer to figure.
    :return: the HMM model parameterized by tau, t1, and t2.
    """
    model = hmm.MultinomialHMM(n_components=2)
    model.n_features = 5
    model.startprob_ = np.array([0.5, 0.5])
    model.transmat_ = get_transmat(tau)
    model.emissionprob_ = get_emissionprobs(t01, t12, t_admix)
    return model

