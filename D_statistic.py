
def compute_D_from_symbols(symbols):
    ABBA_counts = 0
    BABA_counts = 0
    for symbol in symbols:
        if symbol == 0 or symbol == 1:
            ABBA_counts += 1
        if symbol == 2:
            BABA_counts += 1
    return (ABBA_counts - BABA_counts) / (ABBA_counts + BABA_counts)

