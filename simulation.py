import msprime

max_chrom = 1


def run_sim(length, mutation_rate, recombination_rate, Ne, t12, t01, t_admix, t_mrca, admix_prop, random_seed=None):
    # Set up the population sizes

    population_configurations = [
        msprime.PopulationConfiguration(sample_size=1, initial_size=Ne),
        msprime.PopulationConfiguration(sample_size=1, initial_size=Ne),
        msprime.PopulationConfiguration(sample_size=1, initial_size=Ne),
        msprime.PopulationConfiguration(sample_size=1, initial_size=Ne)]
       
    # Now we set up the migration matrix, if you want continuous gene flow
    migration_matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]]
    
    #Times are given in generations
    T12 = 2 * t12 * Ne
    T01 = 2 * t01 * Ne
    T_admix = 2 * t_admix * Ne
    T_mrca = 2 * t_mrca * Ne
    
    demographic_events = [
    # One-way flow from 1 into 2
        msprime.MassMigration(
            time=T_admix, source=1, destination=2, proportion=admix_prop),
    # census after mass migration
        msprime.CensusEvent(time=T_admix + 1), 
    # 0 splits from 1, i.e. 0 and 1 merge
        msprime.MassMigration(
            time=T01, source=0, destination=1, proportion=1.0),
    # 1 splits from 2, i.e. 1 and 2 merge
        msprime.MassMigration(
            time=T12, source=1, destination=2, proportion=1.0),
    # 2 and 3 merge:
        msprime.MassMigration(
            time=T_mrca, source=2, destination=3, proportion=1.0)
    ]            

    dp = msprime.simulate(
        Ne=N,
        population_configurations=population_configurations,
        migration_matrix=migration_matrix,
        demographic_events=demographic_events,
        mutation_rate=mutation_rate,
        length=length,
        recombination_rate=recombination_rate,
        random_seed=random_seed)

    return dp
