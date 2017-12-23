#!/usr/bin/env python3

import sys
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtWidgets import QApplication

from DataStore import DataStore
from Measurement import Measurement
from Model import Model

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(Measurement, 'App', 1, 0, 'Measurement')
    qmlRegisterType(DataStore,   'App', 1, 0, 'DataStore')
    qmlRegisterType(Model,       'App', 1, 0, 'Model')

    myCtx = DataStore()
    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()
    engine.rootContext().setContextProperty("datastore", myCtx)
    engine.load('ui/main.qml')
    win = engine.rootObjects()[0]
    win.show()

    win.newProjectFilesChosen.connect(myCtx.onNewProjectFilesChosen)
    win.projectFileChosen.connect(myCtx.onProjectFileChosen)
    win.projectWizardUpdateYoffsets.connect(
        myCtx.onProjectWizardUpdateYoffsets)
    win.projectAccepted.connect(myCtx.onProjectAccepted)
    win.currentLineChanged.connect(myCtx.updateCurrentMeasurement)
    myCtx.openProjectWizard.connect(win.onOpenWizard)

    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
