import numpy as np
from scipy import signal


def getWeights(x, cutoff):
    alc = 0.469718639349826 * cutoff
    invAlc = 1 / alc

    weights = np.exp(-np.pi * (x * invAlc)**2) * invAlc
    weights *= (1 / np.sum(weights))
    return weights


def filterProfile(x, spacing, cutoff):
    Lc = 0.5  # Default truncating constant by ISO 16610-21
    lcuttr = Lc * cutoff  # Trucated cut-off wave length
    ni = len(x) - 1  # Original profile point interval number
    Ln = ni * spacing  # Original profile total lenght
    nicut = ni / Ln * cutoff  # Cut-off wave length in point interval number expesssed
    nicuttr = ni / Ln * lcuttr  # Truncated cut-off point interval number

    gaussxlim = int(np.rint(nicuttr))
    # Odd numbered symetrical weight function x ordinate
    gaussx = np.arange(-gaussxlim, gaussxlim + 1, dtype=np.float)
    weights = getWeights(gaussx, nicut)  # Weight funcion values
    filtered = signal.fftconvolve(x, weights, 'same')
    filtered[0:gaussxlim] = np.nan
    filtered[-gaussxlim:] = np.nan

    return (filtered, gaussxlim)
