import numpy as np
from scipy.interpolate import griddata
from PyQt5.QtDataVisualization import QSurfaceDataItem
from PyQt5.QtGui import QVector3D
from Measurement import Measurement


def fillProxy(proxy, data, scale, xoffset=0.0):
    dataArray = []

    for rowIdx, row in enumerate(data):
        newRow = []
        y = float(rowIdx) * scale
        for colIdx, value in enumerate(row):
            x = float(colIdx) * scale + xoffset
            newRow.append(QSurfaceDataItem(QVector3D(x, value, y)))
        dataArray.append(newRow)

    proxy.resetArray(dataArray)


def build3d(old_measurements, proxy, filePath, subsample, beginning, end):
    measurements = []

    for m in old_measurements:
        clonedMeas = Measurement(
            m._filename, m._fullpath, m._offsetX, m._offsetY)
        clonedMeas.readDataRange(beginning, end, subsample)
        measurements.append(clonedMeas)

    nsamples = max([m.nsamples for m in measurements])
    step = min([m.spacing for m in measurements])

    for meas in measurements:
        meas.pad(nsamples, step)

    cols, rows = nsamples, int(measurements[-1].offsetY / step)
    z = np.empty((rows, cols), dtype=np.float)
    z[:] = np.NAN

    for meas in measurements:
        row = int(meas.offsetY / step)
        row = min(row, rows - 1)
        z[row, :] = meas.profile

    x = np.arange(0, cols, 1, dtype=np.float)
    y = np.arange(0, rows, 1, dtype=np.float)
    xx, yy = np.meshgrid(x, y)

    missing = np.ma.masked_invalid(z)
    x1, y1 = xx[~missing.mask], yy[~missing.mask]
    newmissing = missing[~missing.mask]

    z = griddata((x1, y1), newmissing.ravel(),
                 (xx, yy), method='cubic')

    fillProxy(proxy, z, step, beginning)

    yRange = (measurements[0]._offsetY, measurements[-1]._offsetY)
    return (z, step, yRange)
