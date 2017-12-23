import re
import os
from PyQt5.QtCore import (QObject, QVariant, QUrl,
                          pyqtSignal, pyqtProperty, pyqtSlot)
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtChart import QAbstractSeries, QValueAxis, QLegend
from Measurement import Measurement
from Model import Model
import jsonpickle


class DataStore(QObject):
    def __init__(self, parent=None):
        super(DataStore, self).__init__(parent)
        self._measurements = []
        self._projectName = None
        self.projectFolderPath = None
        self._Ystep = 0.0

        self._currentMeasurement = None
        self._currentMeasurementIdx = 0
        self._measurementSelectionStep = 0.0
        self._measurementSelectionMax = 0.0

        self._newProjectName = ''
        self._newProjectMeasurements = []
        self._newProjectYstep = 0

        self._model = Model()

        self._statusBarMessage = ''

    @pyqtSlot('int')
    def updateCurrentMeasurement(self, offset):
        self._currentMeasurementIdx += offset
        self.currentMeasurement = self._measurements[self._currentMeasurementIdx]

    ### NEW PROJECT CREATION ###
    @pyqtSlot(QVariant)
    def onNewProjectFilesChosen(self, fileUrls):
        self.setMeasurements(fileUrls)
        self.openProjectWizard.emit()

    newProjectNameChanged = pyqtSignal()

    @pyqtProperty('QString', notify=newProjectNameChanged)
    def newProjectName(self):
        return self._newProjectName

    @newProjectName.setter
    def newProjectName(self, newName):
        if newName != self._newProjectName:
            self._newProjectName = newName
            self.newProjectNameChanged.emit()

    ##
    newProjectMeasurementsChanged = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=newProjectMeasurementsChanged)
    def newProjectMeasurements(self):
        return QQmlListProperty(Measurement, self, self._newProjectMeasurements)

    @newProjectMeasurements.setter
    def newProjectMeasurements(self, newProjectMeasurements):
        if newProjectMeasurements != self._newProjectMeasurements:
            self._newProjectMeasurements = newProjectMeasurements
            self.newProjectMeasurementsChanged.emit()

    def appendMeasurements(self, measurement):
        self._newProjectMeasurements.append(measurement)
        self.newProjectMeasurementsChanged.emit()

    ##
    newProjectYstepChanged = pyqtSignal()

    @pyqtProperty('double', notify=newProjectYstepChanged)
    def newProjectYstep(self):
        return self._newProjectYstep

    @newProjectYstep.setter
    def newProjectYstep(self, newVal):
        if newVal != self._newProjectYstep:
            self._newProjectYstep = newVal
            self.newProjectYstepChanged.emit()

    modelChanged = pyqtSignal()

    @pyqtProperty(Model, notify=modelChanged)
    def model(self):
        return self._model

    @model.setter
    def model(self, newVal):
        if newVal != self._model:
            self._model = newVal
            self.modelChanged.emit()

    ##
    def setMeasurements(self, fileUrls):
        if len(fileUrls) > 0:
            filename = fileUrls[0].fileName()
            matches = re.search('(.+)(?:[_ ]\d+\.PRF)', filename)
            projectName = matches.group(1)
            self.newProjectName = projectName
            self.projectFolderPath = fileUrls[0].toString(
                QUrl.PreferLocalFile | QUrl.RemoveFilename)

        for fileUrl in fileUrls:
            filename = fileUrl.fileName()
            fullpath = fileUrl.toLocalFile()
            meas = Measurement(filename, fullpath, 0.0, 0.0)
            self.appendMeasurements(meas)

    ##
    openProjectWizard = pyqtSignal()

    @pyqtSlot()
    def onProjectWizardUpdateYoffsets(self):
        for n, meas in enumerate(self.newProjectMeasurements):
            meas.offsetY = n * self.newProjectYstep
        self.measurementSelectionStep = self.newProjectYstep
        self.measurementSelectionMax = (
            len(self.newProjectMeasurements) - 1) * self.newProjectYstep

    ##
    @pyqtSlot()
    def onProjectAccepted(self):
        self.measurements = self._newProjectMeasurements
        self.newProjectMeasurements = []

        self.projectName = self.newProjectName
        self.newProjectName = ''

        self.updateCurrentMeasurement(0)
        self.projectNameChanged.emit()

    ### PROPERTIES ###
    measurementsChanged = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=measurementsChanged)
    def measurements(self):
        return QQmlListProperty(Measurement, self, self._measurements)

    @measurements.setter
    def measurements(self, measurements):
        if measurements != self._measurements:
            self._measurements = measurements
            self.measurementsChanged.emit()

    YstepChanged = pyqtSignal()

    @pyqtProperty('double', notify=YstepChanged)
    def Ystep(self):
        return self._Ystep

    @Ystep.setter
    def Ystep(self, Ystep):
        if Ystep != self._Ystep:
            self._Ystep = Ystep
            self.YstepChanged.emit()

    projectNameChanged = pyqtSignal()

    @pyqtProperty('QString', notify=projectNameChanged)
    def projectName(self):
        return self._projectName

    @projectName.setter
    def projectName(self, newName):
        if newName != self._projectName:
            self._projectName = newName
            self.projectNameChanged.emit()

    measurementSelectionStepChanged = pyqtSignal()

    @pyqtProperty('double', notify=measurementSelectionStepChanged)
    def measurementSelectionStep(self):
        return self._measurementSelectionStep

    @measurementSelectionStep.setter
    def measurementSelectionStep(self, newVal):
        if newVal != self._measurementSelectionStep:
            self._measurementSelectionStep = newVal
            self.measurementSelectionStepChanged.emit()

    measurementSelectionMaxChanged = pyqtSignal()

    @pyqtProperty('double', notify=measurementSelectionMaxChanged)
    def measurementSelectionMax(self):
        return self._measurementSelectionMax

    @measurementSelectionMax.setter
    def measurementSelectionMax(self, newVal):
        if newVal != self._measurementSelectionMax:
            self._measurementSelectionMax = newVal
            self.measurementSelectionMaxChanged.emit()

    ##
    currentMeasurementChanged = pyqtSignal()

    @pyqtProperty(Measurement, notify=currentMeasurementChanged)
    def currentMeasurement(self):
        return self._currentMeasurement

    @currentMeasurement.setter
    def currentMeasurement(self, newVal):
        if newVal != self._currentMeasurement:
            self._currentMeasurement = newVal
            self.currentMeasurementChanged.emit()

    ### UPDATE GUI ###
    @pyqtSlot(QAbstractSeries, QAbstractSeries, QAbstractSeries)
    def updateProfileSeries(self, profileSeries, wavinessSeries, roughnessSeries):
        profile, waviness, roughness = self.currentMeasurement.getProfiles()
        profileSeries.replace(profile)
        wavinessSeries.replace(waviness)
        roughnessSeries.replace(roughness)

    @pyqtSlot(QAbstractSeries, QAbstractSeries, QAbstractSeries, QAbstractSeries, QValueAxis, QValueAxis)
    def updateFabricSeries(self, profileSeries, smoothedProfileSeries, fftSeries, maximaSeries, fftX, fftY):
        profile, smoothedProfile, fft, fftMaxima, fftRanges = self.currentMeasurement.getFabricSeries()
        profileSeries.replace(profile)
        smoothedProfileSeries.replace(smoothedProfile)
        fftSeries.replace(fft)
        maximaSeries.replace(fftMaxima)

        fftX.setRange(fftRanges[0], fftRanges[1])
        fftY.setRange(fftRanges[2], fftRanges[3])

    @pyqtSlot(QValueAxis, QValueAxis)
    def updateProfileAxes(self, x, y):
        maxX = self.currentMeasurement.lengthInMM()
        minY, maxY = self.currentMeasurement.valuesRange()
        x.setMax(maxX)
        y.setRange(minY, maxY)

    @pyqtSlot(QLegend)
    def connectChartLegendSignals(self, legend):
        for marker in legend.markers():
            marker.disconnect()
            marker.clicked.connect(self.onMarkerClicked)

    @pyqtSlot()
    def onMarkerClicked(self):
        marker = self.sender()
        series = marker.series()
        series.setVisible(not series.isVisible())
        marker.setVisible(True)

        alpha = 1.0 if series.isVisible() else 0.5

        def setAlpha(brush):
            color = brush.color()
            color.setAlphaF(alpha)
            brush.setColor(color)
            return brush

        marker.setLabelBrush(setAlpha(marker.labelBrush()))
        marker.setBrush(setAlpha(marker.brush()))
        marker.setPen(setAlpha(marker.pen()))

    ### SERIALIZATION / DESERIALIZATION ###
    def __getstate__(self):
        return {'projectName': self._projectName,
                'measurementSelectionStep': self._measurementSelectionStep,
                'measurements': self._measurements,
                'projectFolderPath': self.projectFolderPath,
                'model': self.model}

    @pyqtSlot()
    def saveProject(self):
        jsonpickle.set_encoder_options('json', indent=4)
        filePath = os.path.join(self.projectFolderPath,
                                self.projectName + '.json')
        with open(filePath, 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=False))
            self.statusBarMessage = 'Saved project as {:s}.json'.format(
                self.projectName)

    resetMeasurementSpinbox = pyqtSignal()

    @pyqtSlot(QVariant)
    def onProjectFileChosen(self, fileUrls):
        filePath = fileUrls[0].toLocalFile()
        with open(filePath) as f:
            dict = jsonpickle.decode(f.read())
            self.projectName = dict['projectName']
            self.measurementSelectionStep = dict['measurementSelectionStep']
            self.projectFolderPath = dict['projectFolderPath']
            self.model.subsamplingFactor = dict['model']['subsamplingFactor']
            self.model.beginning = dict['model']['beginning']
            self.model.end = dict['model']['end']
            self._measurements = []
            for m in dict['measurements']:
                filename = m['filename']
                fullpath = os.path.join(self.projectFolderPath, filename)
                self._measurements.append(Measurement(
                    filename, fullpath, m['offsetX'], m['offsetY'], m['cutoff']))

            self._currentMeasurementIdx = 0
            self.measurementsChanged.emit()
            self.measurementSelectionMax = (
                len(self.measurements) - 1) * self.measurementSelectionStep
            self.updateCurrentMeasurement(0)
            self.projectNameChanged.emit()
            self.resetMeasurementSpinbox.emit()

            self._model.clear()
            self.statusBarMessage = 'Opened {:s}'.format(
                fileUrls[0].fileName())

    @pyqtSlot()
    def build3dModel(self):
        filepath = os.path.join(self.projectFolderPath,
                                self.projectName + '.png')
        self._model.build(self._measurements, filepath, self.statusBarMessage)

    @pyqtSlot()
    def exportModelToImage(self):
        self.statusBarMessage = 'Exporting model...'
        filename = '{:s}_3D.png'.format(self._projectName)
        path = os.path.join(self.projectFolderPath, filename)
        self._model.exportToImage(path)
        self.statusBarMessage = 'Exported model to {:s}'.format(filename)

    @pyqtSlot()
    def exportModelToText(self):
        self.statusBarMessage = 'Exporting model...'
        filename = '{:s}_3D.txt'.format(self._projectName)
        path = os.path.join(self.projectFolderPath, filename)
        self._model.exportToText(path)
        self.statusBarMessage = 'Exported model to {:s}'.format(filename)

    ### EXPORT ###
    @pyqtSlot()
    def exportMeasurements(self):
        self.statusBarMessage = 'Exporting measurements...'
        for m in self._measurements:
            m.exportMeasurement()
        self.statusBarMessage = 'Exported measurements'

    ### STATUS BAR ###
    statusBarMessageChanged = pyqtSignal()

    @pyqtProperty(str, notify=statusBarMessageChanged)
    def statusBarMessage(self):
        return self._statusBarMessage

    @statusBarMessage.setter
    def statusBarMessage(self, newVal):
        if newVal != self._statusBarMessage:
            self._statusBarMessage = newVal
            self.statusBarMessageChanged.emit()
