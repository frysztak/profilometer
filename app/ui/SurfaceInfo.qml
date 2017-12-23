import QtQuick 2.7
import QtQuick.Controls 2.2

Frame {
    topPadding: 8
    bottomPadding: 8
    spacing: 10

    property alias ra: raLabel.text
    property alias rq: rqLabel.text
    property alias rv: rvLabel.text
    property alias rp: rpLabel.text
    property alias rt: rtLabel.text
    property alias rsk: rskLabel.text
    property alias rku: rkuLabel.text

    property alias wa: waLabel.text
    property alias wq: wqLabel.text
    property alias wv: wvLabel.text
    property alias wp: wpLabel.text
    property alias wt: wtLabel.text
    property alias wsk: wskLabel.text
    property alias wku: wkuLabel.text

    Row {
        spacing: 20

        Column {
            Label {
                text: qsTr("Roughness parameters:")
                font.bold: true
                font.pixelSize: 18
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>a</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: raLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>q</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rqLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>v</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rvLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>p</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rpLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>t</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rtLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>sk</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rskLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("R<sub>ku</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: rkuLabel
                    font.pixelSize: 16
                }
            }
        }

        Column {
            Label {
                text: qsTr("Waviness parameters:")
                font.bold: true
                font.pixelSize: 18
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>a</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: waLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>q</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wqLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>v</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wvLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>p</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wpLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>t</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wtLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>sk</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wskLabel
                    font.pixelSize: 16
                }
            }

            Row {
                Label {
                    textFormat: Text.RichText
                    text: qsTr("W<sub>ku</sub>: ")
                    font.pixelSize: 16
                }
                Label {
                    id: wkuLabel
                    font.pixelSize: 16
                }
            }
        }
    }
}
