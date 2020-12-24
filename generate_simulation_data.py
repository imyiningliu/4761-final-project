# Seed was 3
from simulation import run_sim
import numpy as np
import os
import pickle
from model import setup_model
from utils import get_t1_t2

# Generate Simulation Data: Symbols
np.random.seed(3)
num_samples = 100

t01 = 1
t12 = 2
t_admix = 0.5

taus = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
Ns = [1e3, 1e4, 1e5]  # this is the number of states # No need for 1e6

for N in Ns:
    print("Starting N = %s" % N)
    for tau in taus:
        print("Starting tau = %s" % tau)

        data = []
        for _ in range(num_samples):
            # generate symbols and states
            t1, t2 = get_t1_t2(t01, t12, t_admix)
            model = setup_model(tau, t01, t12, t_admix)
            X = model.sample(int(N))  # symbols and states

            data.append(X)

        # save data
        with open("./data/2020-12-14/symbols-N%s-tau%s.pkl" % (N, tau), 'wb') as outfile:
            pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)

        # Generate Simulation Data: Genealogies

mutation_rate = 1e-8
recombination_rate = 1e-8
Ne = 1e6

t_mrca = 3

lengths = [1e4, 1e5, 1e6]
admix_props = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

# reset seed
np.random.seed(3)

for length in lengths:
    print("Starting length = %s" % length)

    for admix_prop in admix_props:
        print("Starting admix_prop = %s" % admix_prop)

        # make folder for a combination of length and admix_prop
        os.mkdir('./data/2020-12-14/genealogies/length%s-admix_prop%s' % (length, admix_prop))

        for i in range(num_samples):
            # simulate genealogy
            seed = np.random.randint(2 ** 32)
            dp = run_sim(length, mutation_rate, recombination_rate, Ne, t12, t01, t_admix, t_mrca, admix_prop,
                         random_seed=seed)

            # dump genealogy
            dp.dump('./data/2020-12-14/genealogies/length%s-admix_prop%s/sample%s' % (length, admix_prop, i))
