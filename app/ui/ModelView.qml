import QtQuick 2.2
import QtQuick.Controls 2.2
import QtDataVisualization 1.0

Item {
    id: surfaceView
    anchors.fill: parent
    anchors.margins: surfacePlot.visible ? 0 : 8

    property bool projectOpened
    signal build3dModel

    Component.onCompleted: {
        datastore.model.renderModelToFile.connect(function(path) {
            surfacePlot.grabToImage(function(result) {
                result.saveToFile(path);
            })
        });
    }

    Frame {
        topPadding: 20
        bottomPadding: 20
        spacing: 10
        visible: !datastore.isModelCalculated

        Column {
            spacing: 10
            Row {
                spacing: 10
                Label {
                    id: subsampleLabel
                    text: qsTr("Subsample: ")
                    font.pixelSize: 18
                }
                SpinBox {
                    id: subsampleSpinBox
                    anchors.verticalCenter: subsampleLabel.verticalCenter
                    from: 1
                    to: 128
                    enabled: projectOpened
                    value: datastore.model.subsamplingFactor
                    onValueChanged: datastore.model.subsamplingFactor = value
                }
            }

            Row {
                spacing: 10
                Label {
                    id: beginningLabel
                    text: qsTr("X-axis beginning: ")
                    font.pixelSize: 18
                }
                FloatSpinBox {
                    id: beginningSpinBox
                    anchors.verticalCenter: beginningLabel.verticalCenter
                    from: 0
                    enabled: projectOpened
                    onValueChanged: datastore.model.beginning = value/scale
                }
            }

            Row {
                spacing: 10
                Label {
                    id: endLabel
                    text: qsTr("X-axis end: ")
                    font.pixelSize: 18
                }
                FloatSpinBox {
                    id: endSpinBox
                    anchors.verticalCenter: endLabel.verticalCenter
                    from: 0
                    enabled: projectOpened
                    onValueChanged: datastore.model.end = value/scale
                }
            }

            Row {
                spacing: 10
                Label {
                    id: scaleFactorLabel
                    text: qsTr("Z-axis scaling factor: ")
                    font.pixelSize: 18
                }
                FloatSpinBox {
                    id: scaleFactorSpinBox
                    anchors.verticalCenter: scaleFactorLabel.verticalCenter
                    from: 10
                    scale: 10
                    units: ''
                    decimals: 1
                    enabled: projectOpened
                    onValueChanged: datastore.model.zAxisScalingFactor = value/scale
                }
            }

            Button {
                id: show3dModelButton
                text: qsTr("Build 3D model")
                enabled: projectOpened && (beginningSpinBox.value != endSpinBox.value) && (beginningSpinBox.value != 0 || endSpinBox.value != 0)
                onClicked: datastore.build3dModel()
            }
        }
    }

    ColorGradient {
        id: surfaceGradient
        ColorGradientStop { position: 0.00; color: "darkGreen" }
        ColorGradientStop { position: 0.50; color: "yellow" }
        ColorGradientStop { position: 0.80; color: "red" }
        ColorGradientStop { position: 1.00; color: "darkRed" }
    }

    Surface3D {
        id: surfacePlot
        width: surfaceView.width
        height: surfaceView.height
        visible: datastore.model.isCalculated && datastore.model.isVisible

        theme: Theme3D {
            type: Theme3D.ThemeStoneMoss
            font.family: "STCaiyun"
            font.pointSize: 35
            colorStyle: Theme3D.ColorStyleRangeGradient
            baseGradients: [surfaceGradient]
        }

        shadowQuality: AbstractGraph3D.ShadowQualityNone
        selectionMode: AbstractGraph3D.SelectionSlice | AbstractGraph3D.SelectionRow
        scene.activeCamera.cameraPreset: Camera3D.CameraPresetIsometricLeft
        //axisY.autoAdjustRange: true
        axisY.max: datastore.model.zAxisMax
        axisY.min: datastore.model.zAxisMin
        axisX.autoAdjustRange: true
        axisZ.autoAdjustRange: true
        axisX.segmentCount: 10
        axisX.subSegmentCount: 2
        axisX.labelFormat: "%0.2f mm"
        axisZ.segmentCount: 10
        axisZ.subSegmentCount: 2
        axisZ.labelFormat: "%0.2f mm"
        axisY.segmentCount: 5
        axisY.subSegmentCount: 2
        axisY.labelFormat: "%0.2f μm"
        //axisY.title: "Z"
        axisX.title: "X"
        axisZ.title: "Y"
        axisY.titleVisible: true
        axisX.titleVisible: true
        axisZ.titleVisible: true

        Surface3DSeries {
            id: modelSeries
            flatShadingEnabled: false
            drawMode: Surface3DSeries.DrawSurface
            dataProxy: datastore.model.proxy
        }
    }
}

