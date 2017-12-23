from PyQt5.QtCore import QObject, QPointF, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt5.QtGui import QPolygonF

import numpy as np
import scipy
from prfreader import PRFreader
import iso16610_21
import surfaceparams
import fabricparams


class Measurement(QObject):
    offsetXchanged = pyqtSignal()
    offsetYchanged = pyqtSignal()
    cutOffChanged = pyqtSignal()

    def __init__(self, filename='', fullpath='', offsetX=0.0,
                 offsetY=0.0, cutoff=0.08, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = []
        self._filename = filename
        self._fullpath = fullpath
        self._offsetX = offsetX
        self._offsetY = offsetY
        self._cutoff = cutoff
        self.roughness = self.waviness = []
        self._ra = self._rq = self._rv = self._rp = self._rt = self._rku = self._rsk = 0.0
        self._wa = self._wq = self._wv = self._wp = self._wt = self._wku = self._wsk = 0.0
        self._fftGlobalMaximum = 0.0
        self._fftLocalMaxima = []

    @pyqtProperty('QString', constant=True)
    def filename(self):
        return self._filename

    @pyqtProperty('double', notify=offsetXchanged)
    def offsetX(self):
        return self._offsetX

    @offsetX.setter
    def offsetX(self, offsetX):
        if offsetX != self._offsetX:
            self._offsetX = offsetX
            self.offsetXchanged.emit()

    @pyqtProperty('float', notify=offsetYchanged)
    def offsetY(self):
        return self._offsetY

    @offsetY.setter
    def offsetY(self, offsetY):
        if offsetY != self._offsetY:
            self._offsetY = offsetY
            self.offsetYchanged.emit()

    @pyqtProperty('double', notify=cutOffChanged)
    def cutoff(self):
        return self._cutoff

    @cutoff.setter
    def cutoff(self, newVal):
        if newVal != self._cutoff:
            self._cutoff = newVal
            self.cutOffChanged.emit()

    ### ROUGHNESS PARAMETERS ###
    raChanged = pyqtSignal()

    @pyqtProperty('QString', notify=raChanged)
    def ra(self):
        return '{:.3f} μm'.format(self._ra)

    @ra.setter
    def ra(self, newVal):
        if newVal != self._ra:
            self._ra = newVal
            self.raChanged.emit()

    rqChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rqChanged)
    def rq(self):
        return '{:.3f} μm'.format(self._rq)

    @rq.setter
    def rq(self, newVal):
        if newVal != self._rq:
            self._rq = newVal
            self.rqChanged.emit()

    rvChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rvChanged)
    def rv(self):
        return '{:.3f} μm'.format(self._rv)

    @rv.setter
    def rv(self, newVal):
        if newVal != self._rv:
            self._rv = newVal
            self.rvChanged.emit()

    rpChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rpChanged)
    def rp(self):
        return '{:.3f} μm'.format(self._rp)

    @rp.setter
    def rp(self, newVal):
        if newVal != self._rp:
            self._rp = newVal
            self.rpChanged.emit()

    rtChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rtChanged)
    def rt(self):
        return '{:.3f} μm'.format(self._rt)

    @rt.setter
    def rt(self, newVal):
        if newVal != self._rt:
            self._rt = newVal
            self.rtChanged.emit()

    rskChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rskChanged)
    def rsk(self):
        return '{:.3f}'.format(self._rsk)

    @rsk.setter
    def rsk(self, newVal):
        if newVal != self._rsk:
            self._rsk = newVal
            self.rskChanged.emit()

    rkuChanged = pyqtSignal()

    @pyqtProperty('QString', notify=rkuChanged)
    def rku(self):
        return '{:.3f}'.format(self._rku)

    @rku.setter
    def rku(self, newVal):
        if newVal != self._rku:
            self._rku = newVal
            self.rkuChanged.emit()

    ### WAVINESS PARAMETERS ###
    waChanged = pyqtSignal()

    @pyqtProperty('QString', notify=waChanged)
    def wa(self):
        return '{:.3f} μm'.format(self._wa)

    @wa.setter
    def wa(self, newVal):
        if newVal != self._wa:
            self._wa = newVal
            self.waChanged.emit()

    wqChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wqChanged)
    def wq(self):
        return '{:.3f} μm'.format(self._wq)

    @wq.setter
    def wq(self, newVal):
        if newVal != self._wq:
            self._wq = newVal
            self.wqChanged.emit()

    wvChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wvChanged)
    def wv(self):
        return '{:.3f} μm'.format(self._wv)

    @wv.setter
    def wv(self, newVal):
        if newVal != self._wv:
            self._wv = newVal
            self.wvChanged.emit()

    wpChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wpChanged)
    def wp(self):
        return '{:.3f} μm'.format(self._wp)

    @wp.setter
    def wp(self, newVal):
        if newVal != self._wp:
            self._wp = newVal
            self.wpChanged.emit()

    wtChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wtChanged)
    def wt(self):
        return '{:.3f} μm'.format(self._wt)

    @wt.setter
    def wt(self, newVal):
        if newVal != self._wt:
            self._wt = newVal
            self.wtChanged.emit()

    wskChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wskChanged)
    def wsk(self):
        return '{:.3f}'.format(self._wsk)

    @wsk.setter
    def wsk(self, newVal):
        if newVal != self._wsk:
            self._wsk = newVal
            self.wskChanged.emit()

    wkuChanged = pyqtSignal()

    @pyqtProperty('QString', notify=wkuChanged)
    def wku(self):
        return '{:.3f}'.format(self._wku)

    @wku.setter
    def wku(self, newVal):
        if newVal != self._wku:
            self._wku = newVal
            self.wkuChanged.emit()

    ### FABRIC PARAMRETERS ###
    fftGlobalMaximumChanged = pyqtSignal()

    @pyqtProperty('QString', notify=fftGlobalMaximumChanged)
    def fftGlobalMaximum(self):
        return '{:.3f} μm'.format(1000.0 * self._fftGlobalMaximum)

    @fftGlobalMaximum.setter
    def fftGlobalMaximum(self, newVal):
        if newVal != self._fftGlobalMaximum:
            self._fftGlobalMaximum = newVal
            self.fftGlobalMaximumChanged.emit()

    fftLocalMaximaChanged = pyqtSignal()

    @pyqtProperty('QString', notify=fftLocalMaximaChanged)
    def fftLocalMaxima(self):
        str = sep = ''
        for peak in self._fftLocalMaxima:
            str += '{:s}{:.3f} μm'.format(sep, 1000.0 * peak)
            sep = ', '
        return str

    @fftLocalMaxima.setter
    def fftLocalMaxima(self, newVal):
        if newVal != self._fftLocalMaxima:
            self._fftLocalMaxima = newVal
            self.fftLocalMaximaChanged.emit()

    def readData(self, subsample=1):
        (_spacing, _data) = PRFreader.read(self._fullpath)
        self.spacing = _spacing * subsample
        self.profile = 1e3 * _data  # scale to microns
        if subsample != 1:
            self.profile = scipy.signal.decimate(
                self.profile, subsample, zero_phase=True)
        self.nsamples = len(self.profile)

    def readDataRange(self, beginning, end, subsample):
        (_spacing, _data) = PRFreader.read(self._fullpath)

        beginningIdx = int(beginning / _spacing)
        endIdx = int(end / _spacing)
        self.profile = 1e3 * _data[beginningIdx:endIdx]

        if subsample != 1:
            self.profile = scipy.signal.decimate(
                self.profile, subsample, zero_phase=True)
        self.nsamples = len(self.profile)
        self.spacing = _spacing * subsample

    def pad(self, length, step):
        startIdx = int(self.offsetX / step)
        if startIdx is not 0:
            self.shift(startIdx)

        right = length - self.nsamples
        if right is not 0:
            self.profile = np.pad(self.profile, (0, right),
                                  'constant', constant_values=(np.NAN))

    # https://stackoverflow.com/a/42642326
    def shift(self, num, fill_value=np.nan):
        result = np.empty_like(self.profile)
        if num > 0:
            result[:num] = fill_value
            result[num:] = self.profile[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = self.profile[-num:]
        else:
            result = arr
        self.profile = result

    def get_polyline(self, profile, xdata, offset=0.0):
        """Convert series data to QPolygon(F) polyline

        This code is derived from PythonQwt's function named
        `qwt.plot_curve.series_to_polyline`"""

        if (offset != 0.0):
            xdata = xdata[offset:-offset:1]
            profile = profile[offset:-offset:1]

        size = len(profile)
        polyline = QPolygonF(size)
        pointer = polyline.data()
        dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
        pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)

        memory = np.frombuffer(pointer, dtype)
        memory[:(size - 1) * 2 + 1:2] = xdata
        memory[1:(size - 1) * 2 + 2:2] = profile
        return polyline

    def getProfiles(self):
        if len(self.profile) == 0:
            self.readData()

        self.waviness, offset = iso16610_21.filterProfile(
            self.profile, self.spacing, self.cutoff)
        self.roughness = self.profile - self.waviness
        x = np.linspace(0.0, self.lengthInMM(), self.nsamples)

        roughness = self.roughness[offset:-offset]
        waviness = self.waviness[offset:-offset]
        self.ra = surfaceparams.calculateRa(
            roughness, self.spacing, self.cutoff)
        self.rq = surfaceparams.calculateRq(
            roughness, self.spacing, self.cutoff)
        self.rv = surfaceparams.calculateRv(roughness)
        self.rp = surfaceparams.calculateRp(roughness)
        self.rt = surfaceparams.calculateRt(self._rv, self._rp)
        self.rsk = surfaceparams.calculateRsk(
            roughness, self._rq, self.spacing, self.cutoff)
        self.rku = surfaceparams.calculateRku(
            roughness, self._rq, self.spacing, self.cutoff)

        self.wa = surfaceparams.calculateRa(
            waviness, self.spacing, self.cutoff)
        self.wq = surfaceparams.calculateRq(
            waviness, self.spacing, self.cutoff)
        self.wv = surfaceparams.calculateRv(waviness)
        self.wp = surfaceparams.calculateRp(waviness)
        self.wt = surfaceparams.calculateRt(self._wv, self._wp)
        self.wsk = surfaceparams.calculateRsk(
            waviness, self._wq, self.spacing, self.cutoff)
        self.wku = surfaceparams.calculateRku(
            waviness, self._wq, self.spacing, self.cutoff)

        return (self.get_polyline(self.profile, x),
                self.get_polyline(self.waviness, x, offset),
                self.get_polyline(self.roughness, x, offset))

    def getFabricSeries(self):
        if len(self.profile) == 0:
            self.readData()

        smoothedProfile, offset = iso16610_21.filterProfile(
            self.profile, self.spacing, 0.02)
        x = np.linspace(0.0, self.lengthInMM(), self.nsamples)

        fft, fftx, fftMaxima, fftRanges = fabricparams.calculateFFT(
            smoothedProfile[offset:-offset], self.spacing)
        self.fftGlobalMaximum, self.fftLocalMaxima = fabricparams.findGlobalMaxima(
            fftMaxima)

        fftMaxima = [QPointF(point[0], point[1]) for point in fftMaxima]

        return (self.get_polyline(self.profile, x),
                self.get_polyline(smoothedProfile, x, offset),
                self.get_polyline(fft, fftx),
                fftMaxima, fftRanges)

    def lengthInMM(self):
        return self.nsamples * self.spacing

    def valuesRange(self):
        return (min(self.profile), max(self.profile))

    def __getstate__(self):
        return {'filename': self._filename,
                'offsetX': self._offsetX,
                'offsetY': self._offsetY,
                'cutoff': self._cutoff}

    ### EXPORT ###
    @pyqtSlot()
    def exportMeasurement(self):
        if len(self.profile) == 0:
            self.readData()
        if len(self.roughness) == 0:
            self.waviness, offset = iso16610_21.filterProfile(
                self.profile, self.spacing, self.cutoff)
            self.roughness = self.profile - self.waviness

        path = self._fullpath.replace('.PRF', '.txt')
        x = np.linspace(0.0, self.lengthInMM(), self.nsamples)

        with open(path, 'w') as f:
            f.write('# Cut-off: {:f} mm\n'.format(self._cutoff))
            f.write('# Ra  = {:^ 8.3f} um, Wa  = {:^ 8.3f} um\n'.format(
                self._ra, self._wa))
            f.write('# Rq  = {:^ 8.3f} um, Wq  = {:^ 8.3f} um\n'.format(
                self._rq, self._wq))
            f.write('# Rv  = {:^ 8.3f} um, Wv  = {:^ 8.3f} um\n'.format(
                self._rv, self._wv))
            f.write('# Rp  = {:^ 8.3f} um, Wp  = {:^ 8.3f} um\n'.format(
                self._rp, self._wp))
            f.write('# Rt  = {:^ 8.3f} um, Wt  = {:^ 8.3f} um\n'.format(
                self._rt, self._wt))
            f.write('# Rsk = {:^ 8.3f},    Wsk = {:^ 8.3f}\n'.format(
                self._rsk, self._wsk))
            f.write('# Rku = {:^ 8.3f},    Wku = {:^ 8.3f}\n'.format(
                self._rku, self._wku))
            f.write('\n')

            f.write('#   X [mm]   |    Y [um]   |    R [um]   |    W [um]\n')
            for x, y, r, w in zip(
                    x, self.profile, self.roughness, self.waviness):
                f.write(
                    '{:^ 13.6e} {:^ 13.6e} {:^ 13.6e} {:^ 13.6e}\n'.format(x, y, r, w))
