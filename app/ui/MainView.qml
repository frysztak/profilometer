import QtQuick 2.2
import QtQuick.Layouts 1.3

Item {
    anchors.fill: parent

    function changeView(idx)
    {
        if (idx == 0) {
            // profile view
            profilePlots.visible = true
            fabricPlots.visible = false
            controlPanel.visible = true
            fabricInfo.visible = false
            surfaceInfo.visible = true
        } else if (idx == 1) {
            // fabric view
            profilePlots.visible = false
            fabricPlots.visible = true
            controlPanel.visible = false
            fabricInfo.visible = true
            surfaceInfo.visible = false
        }
    }

    ColumnLayout {
        id: column
        anchors.fill: parent
        spacing: 0

        Component.onCompleted: {
            controlPanel.spinBoxValueChanged.connect(onControlPanelSpinboxValueChanged)
            datastore.connectChartLegendSignals(profilePlots.chartView.legend)
            datastore.connectChartLegendSignals(fabricPlots.chartView.legend)
            datastore.currentMeasurementChanged.connect(onCurrentMeasurementChanged)
        }

        function onCurrentMeasurementChanged()
        {
            datastore.updateProfileSeries(profilePlots.profileSeries, profilePlots.wavinessSeries, profilePlots.roughnessSeries)
            datastore.updateProfileAxes(profilePlots.axisX, profilePlots.axisY)

            datastore.updateFabricSeries(fabricPlots.profileSeries, fabricPlots.smoothedProfileSeries, fabricPlots.fftSeries, fabricPlots.maximaSeries,
                                      fabricPlots.axisX2, fabricPlots.axisY2)
            datastore.updateProfileAxes(fabricPlots.axisX, fabricPlots.axisY)

            controlPanel.spinbox.value = controlPanel.spinbox.scale * datastore.currentMeasurement.cutoff
        }

        function onControlPanelSpinboxValueChanged(val)
        {
            datastore.currentMeasurement.cutoff = val
            datastore.updateProfileSeries(profilePlots.profileSeries, profilePlots.wavinessSeries, profilePlots.roughnessSeries)
        }

        Row {
            spacing: 8
            Layout.margins: 8
            Layout.bottomMargin: 0

            SampleOverview {}
            ControlPanel {
                id: controlPanel
                projectOpened: datastore.projectName.length !== 0
            }

            FabricInfo {
                id: fabricInfo
                visible: false
                fftGlobalMaximum: datastore.currentMeasurement !== null ? datastore.currentMeasurement.fftGlobalMaximum : "-"
                fftLocalMaxima:   datastore.currentMeasurement !== null ? datastore.currentMeasurement.fftLocalMaxima : "-"
            }

            SurfaceInfo {
                id: surfaceInfo
                Layout.margins: 8
                Layout.fillHeight: true

                ra: datastore.currentMeasurement !== null ? datastore.currentMeasurement.ra : "-"
                rq: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rq : "-"
                rv: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rv : "-"
                rp: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rp : "-"
                rt: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rt : "-"
                rsk: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rsk : "-"
                rku: datastore.currentMeasurement !== null ? datastore.currentMeasurement.rku : "-"

                wa: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wa : "-"
                wq: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wq : "-"
                wv: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wv : "-"
                wp: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wp : "-"
                wt: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wt : "-"
                wsk: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wsk : "-"
                wku: datastore.currentMeasurement !== null ? datastore.currentMeasurement.wku : "-"

            }
        }

        Plots {
            id: profilePlots
            Layout.margins: 8
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        FabricPlots {
            id: fabricPlots
            visible: false
            Layout.margins: 8
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}
