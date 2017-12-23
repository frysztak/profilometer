import QtQuick 2.7
import QtQuick.Controls 2.2

Column {
    property alias spinbox: cutOffSpinBox
    property bool projectOpened
    signal spinBoxValueChanged(real val)

    spacing: 10

    Frame {
        topPadding: 20

        Row {
            spacing: 10
            Label {
                id: cutOffLabel
                text: qsTr("Cut-off: ")
                font.pixelSize: 18
            }
            FloatSpinBox {
                id: cutOffSpinBox
                anchors.verticalCenter: cutOffLabel.verticalCenter
                from: 1
                enabled: projectOpened
                onValueChanged: spinBoxValueChanged(value/scale)
            }
        }
    }
}
