import QtQuick 2.0
import QtQuick.Controls 2.2

Frame {
    topPadding: 20
    rightPadding: 2
    leftPadding: 0
    bottomPadding: 33
    spacing: 10

    Row {
        id: row
        spacing: 5
        //anchors.fill: parent

        DUT {
            id: dut;
            height: 150;
            width: 300;
        }

        FloatSpinBox {
            id: floatSpinBox
            anchors.verticalCenter: dut.verticalCenter
            enabled: datastore.projectName.length !== 0
            to: floatSpinBox.scale * datastore.measurementSelectionMax
            stepSize: floatSpinBox.scale * datastore.measurementSelectionStep
            height: 55
            transformOrigin: Item.Center
            rotation: -90

            property int previousValue: 0

            Component.onCompleted: {
                down.indicator.children[0].rotation = -90
                contentItem.rotation = 90

                datastore.resetMeasurementSpinbox.connect(function() {
                    floatSpinBox.value = 0
                })
            }

            onValueChanged: function() {
                Math.clip = function(number, min, max) {
                    return Math.max(min, Math.min(number, max));
                }
                currentLineChanged(Math.clip(value - previousValue, -1, 1))
                dut.updateCurrentLine((value/scale) / datastore.measurementSelectionMax)
                previousValue = value
            }
        }
    }
}
