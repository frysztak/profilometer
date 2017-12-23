import numpy as np


def split(data, chunkSize):
    chunks, nChunks = [], int(len(data) / chunkSize)

    for i in range(0, nChunks):
        startIdx = int(i * chunkSize)
        endIdx = int((i + 1) * chunkSize)
        chunks.append(data[startIdx:endIdx])

    return (chunks, nChunks)


def calculateRa(data, spacing, cutoff):
    nsamples = cutoff / spacing
    chunks, nChunks = split(data, nsamples)

    sum = 0.0
    for chunk in chunks:
        mean = np.average(chunk)
        sum += np.sum(np.absolute(chunk - mean)) / nsamples
    return sum / nChunks


def calculateRq(data, spacing, cutoff):
    nsamples = cutoff / spacing
    chunks, nChunks = split(data, nsamples)

    sum = 0.0
    for chunk in chunks:
        mean = np.average(chunk)
        sum += np.sqrt(np.sum((chunk - mean)**2) / nsamples)
    return sum / nChunks


def calculateRv(data):
    return np.min(data)


def calculateRp(data):
    return np.max(data)


def calculateRt(Rv, Rp):
    return np.abs(Rv) + np.abs(Rp)


def calculateRsk(data, Rq, spacing, cutoff):
    nsamples = cutoff / spacing
    chunks, nChunks = split(data, nsamples)

    sum = 0.0
    for chunk in chunks:
        mean = np.average(chunk)
        sum += np.sum((chunk - mean)**3) / (nsamples * Rq**3)
    return sum / nChunks


def calculateRku(data, Rq, spacing, cutoff):
    nsamples = cutoff / spacing
    chunks, nChunks = split(data, nsamples)

    sum = 0.0
    for chunk in chunks:
        mean = np.average(chunk)
        sum += np.sum((chunk - mean)**4) / (nsamples * Rq**4)
    return sum / nChunks
