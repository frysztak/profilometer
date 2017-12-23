import numpy as np
import peakutils


def calculateFFT(smoothedProfile, spacing):
    N = len(smoothedProfile)
    fft = np.abs(np.fft.rfft(smoothedProfile * np.hamming(N)) / N)
    fft = fft[4::]

    fftx = np.fft.rfftfreq(N, spacing)
    fftx = 1.0 / fftx[4::]

    fftMaximaIndices = peakutils.indexes(fft, thres=0.10, min_dist=5)
    fftMaxima = [(fftx[idx], fft[idx]) for idx in reversed(fftMaximaIndices)]
    fftRanges = (np.min(fftx), np.max(fftx), np.min(fft), np.max(fft))

    return (fft, fftx, fftMaxima, fftRanges)


def findGlobalMaxima(fftMaxima):
    heighestPeak = max(fftMaxima, key=lambda item: item[1])
    allPeaks = [peak[0] for peak in fftMaxima]
    return (heighestPeak[0], allPeaks)
