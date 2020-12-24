import numpy as np


def get_transmat(tau):
    """
    Get the transition matrix of HMM.
    state0: non-introgressed
    state1: introgressed
    :param tau: introgression probability.
    :return: 2-by-2 transition matrix between the two states.
    """
    return np.array([[1 - tau, tau],
                    [1 - tau, tau]])


def get_emissionprobs(t01, t12, t_admix):
    """
    Get the emission probabilities.
    :param t01: time for MRCA of 0, 1.
    :param t12: time for MRCA of 0, 1, 2.
    :param t_admix: time for introgression.
    :return: emission probabilities.
    """
    t1, t2 = get_t1_t2(t01, t12, t_admix)
    emissionprob = np.zeros((2, 5))

    emissionprob[0] = [np.exp(-t1)/3, 0, np.exp(-t1)/3, 1 - np.exp(-t1), np.exp(-t1)/3]
    emissionprob[1] = [np.exp(-(t1+t2))/3, 1 - np.exp(-(t1 + t2)), np.exp(-(t1+t2))/3, 0, np.exp(-(t1+t2))/3]

    return emissionprob


def tree_to_symbol(tree, Ne, t12):
    """
    Convert a given tree to a symbol in {0, 1, 2, 3, 4}.
    0 = A (long BC)
    1 = A (short BC)
    2 = B(AC)
    3 = C (short AB)
    4 = C (long AB)
    :param tree: a tree
    :param N: effective population size
    :param t12: time for MRCA of pop0, pop1, pop2
    :return: the symbol that the tree represents
    """
    def branch_length(i):
        return tree.time(tree.parent(tree.parent(i)))
        # parent is the census node; so ``grandparent" is really the parent

    external_branch_lengths = [branch_length(0) / (2 * Ne),
                               branch_length(1) / (2 * Ne),
                               branch_length(2) / (2 * Ne)]

    if external_branch_lengths[1] == external_branch_lengths[2]:
        if external_branch_lengths[1] > t12:
            return 0
        else:
            return 1
    if external_branch_lengths[0] == external_branch_lengths[2]:
        assert external_branch_lengths[0] >= t12
        return 2
    if external_branch_lengths[0] == external_branch_lengths[1]:
        if external_branch_lengths[0] > t12:
            return 4
        else:
            return 3

    out = external_branch_lengths.index(max(external_branch_lengths))
    external_branch_lengths.sort()
    external_branch_length = external_branch_lengths[1]
    if out == 0:
        if external_branch_length > t12:
            return 0
        else:
            return 1
    if out == 1:
        return 2
    if out == 2:
        if external_branch_length > t12:
            return 4
        else:
            return 3


def treeseq_to_path(treeseq):
    """
    Convert the tree sequence to a path (hidden states in the HMM), representing introgressed regions.
    :param treeseq: a TreeSequence object.
    :return: the path represented by the tree sequence.
    """
    path = []
    for tree in treeseq.trees():
        census_node = tree.parent(1)
        path.append(treeseq.tables.nodes[census_node].population - 1)
    return path


def treeseq_to_symbols(treeseq, Ne, t12):
    """
    Convert the tree sequence to symbols (emissions).
    :param treeseq: a tree sequence object.
    :param N: effective population size
    :param t12:
    :return: the symbols represented by the tree sequence.
    """
    symbols = []
    for tree in treeseq.trees():
        symbols.append(tree_to_symbol(tree, Ne, t12))
    symbols = np.array(symbols).reshape(-1, 1)
    return symbols


def get_t1_t2(t01, t12, t_admix):
    """
    Convert t01, t12, t_admix into t1, t2.
    :param t01: time for MRCA of pop0, pop1.
    :param t12: time for MRCA of pop0, pop1, pop2.
    :param t_admix: time for introgression.
    :return: t1, t2.
    """
    t1 = t12 - t01
    t2 = t01 - t_admix
    return t1, t2

