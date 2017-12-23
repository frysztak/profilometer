import QtQuick 2.0

Item {
    id: container
    width: 300
    height: 180

    function updateCurrentLine(currentLine) {
        var positionInPx = currentLine * rect.height
        var newY = rect.height - positionInPx

        Math.clip = function(number, min, max) {
          return Math.max(min, Math.min(number, max));
        }

        currentLineRect.y = Math.clip(newY, rect.border.width, rect.height - 2*rect.border.width)
    }

    Row {
        id: row
        x: 0
        y: 0

        Text {
            id: yAxisLabel
            text: qsTr("Y axis")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignLeft
            font.pointSize: 14
            verticalAlignment: Text.AlignTop
            //horizontalAlignment: Text.AlignLeft
            transformOrigin: Item.Center
            rotation: -90
        }

        Column {
            id: column
            //x: yAxisLabel.bottom
            width: 300

            Item {
                id: rectContainer
                width: 250
                height: 150

                Rectangle {
                    id: rect
                    height: parent.height
                    width: parent.width
                    border.color: "black"
                    border.width: 4
                }

                Rectangle {
                    id: currentLineRect
                    x: rect.border.width
                    y: rect.height - 2*rect.border.width
                    width: rect.width-2*rect.border.width
                    height: rect.border.width
                    color: "#e51111"
                }
            }

            Text {
                id: xAxisLabel
                text: qsTr("X axis")
                anchors.horizontalCenter: rectContainer.horizontalCenter
                font.pointSize: 14
            }
        }
    }
}
