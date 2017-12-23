import QtQuick 2.7
import QtQuick.Controls 2.2

Frame {
    bottomPadding: 33
    spacing: 10

    property alias fftGlobalMaximum: fftGlobalMaximum.text
    property alias fftLocalMaxima: fftLocalMaxima.text

    Column {
        Row {
            Label {
                text: qsTr("FFT global maximum: ")
                font.pixelSize: 18
            }

            Label {
                id: fftGlobalMaximum
                font.bold: true
                font.pixelSize: 18
            }
        }

        Row {
            Label {
                text: qsTr("FFT local maxima: ")
                font.pixelSize: 18
            }

            Label {
                id: fftLocalMaxima
                font.bold: true
                font.pixelSize: 18
            }
        }
    }
}
