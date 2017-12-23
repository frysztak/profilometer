from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot
from PyQt5.QtDataVisualization import QSurface3DSeries, QSurfaceDataProxy
import numpy as np
import build3d


class Model(QObject):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)

        self._isCalculated = False
        self._isVisible = False
        self._subsamplingFactor = 4
        self._beginning = 0.0  # in mm
        self._end = 0.0  # in mm
        self._modelStep = 0.0  # in mm
        self._YRange = (0.0, 0.0)  # in mm
        self._model = []
        self._proxy = QSurfaceDataProxy()
        self._modelSeries = QSurface3DSeries(self._proxy)
        self._zAxisMin = 0.0  # in um
        self._zAxisMax = 1.0  # in um
        self._zAxisScalingFactor = 1.0

    subsamplingFactorChanged = pyqtSignal()

    @pyqtProperty(int, notify=subsamplingFactorChanged)
    def subsamplingFactor(self):
        return self._subsamplingFactor

    @subsamplingFactor.setter
    def subsamplingFactor(self, newVal):
        if newVal != self._subsamplingFactor:
            self._subsamplingFactor = newVal
            self.subsamplingFactorChanged.emit()

    isCalculatedChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isCalculatedChanged)
    def isCalculated(self):
        return self._isCalculated

    @isCalculated.setter
    def isCalculated(self, newVal):
        if newVal != self._isCalculated:
            self._isCalculated = newVal
            self.isCalculatedChanged.emit()

    isVisibleChanged = pyqtSignal()

    @pyqtProperty(bool, notify=isVisibleChanged)
    def isVisible(self):
        return self._isVisible

    @isVisible.setter
    def isVisible(self, newVal):
        if newVal != self._isVisible:
            self._isVisible = newVal
            self.isVisibleChanged.emit()

    beginningChanged = pyqtSignal()

    @pyqtProperty(float, notify=beginningChanged)
    def beginning(self):
        return self._beginning

    @beginning.setter
    def beginning(self, newVal):
        if newVal != self._beginning:
            self._beginning = newVal
            self.beginningChanged.emit()

    endChanged = pyqtSignal()

    @pyqtProperty(float, notify=endChanged)
    def end(self):
        return self._end

    @end.setter
    def end(self, newVal):
        if newVal != self._end:
            self._end = newVal
            self.endChanged.emit()

    @pyqtProperty(QSurfaceDataProxy, constant=True)
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, newVal):
        if newVal != self._proxy:
            self._proxy = newVal

    zAxisMinChanged = pyqtSignal()

    @pyqtProperty(float, notify=zAxisMinChanged)
    def zAxisMin(self):
        return self._zAxisMin

    @zAxisMin.setter
    def zAxisMin(self, newVal):
        if newVal != self._zAxisMin:
            self._zAxisMin = newVal
            self.zAxisMinChanged.emit()

    zAxisMaxChanged = pyqtSignal()

    @pyqtProperty(float, notify=zAxisMaxChanged)
    def zAxisMax(self):
        return self._zAxisMax

    @zAxisMax.setter
    def zAxisMax(self, newVal):
        if newVal != self._zAxisMax:
            self._zAxisMax = newVal
            self.zAxisMaxChanged.emit()

    zAxisScalingFactorChanged = pyqtSignal()

    @pyqtProperty(float, notify=zAxisScalingFactorChanged)
    def zAxisScalingFactor(self):
        return self._zAxisScalingFactor

    @zAxisScalingFactor.setter
    def zAxisScalingFactor(self, newVal):
        if newVal != self._zAxisScalingFactor:
            self._zAxisScalingFactor = newVal
            self.zAxisScalingFactorChanged.emit()

    @pyqtSlot()
    def build(self, measurements, filePath, statusBarMessage):
        statusBarMessage = 'Building 3D model...'

        self._model, self._modelStep, self._YRange = build3d.build3d(
            measurements, self._proxy, filePath, self.subsamplingFactor, self.beginning, self.end)

        self.zAxisMin = self.zAxisScalingFactor * np.nanmin(self._model)
        self.zAxisMax = self.zAxisScalingFactor * np.nanmax(self._model)

        self.isCalculated = True
        statusBarMessage = 'Built 3D model'

    @pyqtSlot()
    def clear(self):
        self._proxy.resetArray([])
        self._model = []
        self.isCalculated = False

    renderModelToFile = pyqtSignal(str)

    @pyqtSlot()
    def exportToImage(self, filepath):
        self.renderModelToFile.emit(filepath)

    @pyqtSlot()
    def exportToText(self, filepath):
        x = np.linspace(self._beginning, self._end, num=self._model.shape[1])
        y = np.linspace(
            self._YRange[0],
            self._YRange[1],
            num=self._model.shape[0])

        with open(filepath, 'w') as f:
            f.write('#   X [mm]   |    Y [mm]   |    Z [um]\n')
            for idx, val in np.ndenumerate(self._model):
                yIdx, xIdx = idx
                f.write(
                    '{:^ 13.6e} {:^ 13.6e} {:^ 13.6e}\n'.format(
                        x[xIdx], y[yIdx], val))

    def __getstate__(self):
        return {'subsamplingFactor': self._subsamplingFactor,
                'beginning': self._beginning,
                'end': self._end}
