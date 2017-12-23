import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

Dialog {
    id: dialog
    visible: false
    height: 500
    width: 550
    modal: false
    //parent: ApplicationWindow.overlay
    //standardButtons: Dialog.Cancel
    title: qsTr("Project Wizard")

    signal projectWizardUpdateYoffsets()
    signal projectAccepted()

    ListView {
        id: listView
        width: parent.width
        model: datastore.newProjectMeasurements
        height: 300

        header:listViewHeader

        delegate: Column {
            id: delegate
            property int row: index

            Row {
                spacing: 5
                Text {
                    text: filename
                    font.pointSize: 10
                    y: 10
                    width: listView.headerItem.children[2].itemAt(0).width
                }
                Text {
                    id: spinBoxYoffset
                    font.pointSize: 10
                    y: 10
                    text: "%1 mm".arg(offsetY.toFixed(2))
                    width: listView.headerItem.children[2].itemAt(1).width
                }
            }
        }
        Rectangle {
            color: "silver"
            width: parent.width
            height: 1
        }
    }

    footer: RowLayout {
        Item {
            Layout.fillWidth: true
        }

        Button {
            id: okButton
            width: 150
            enabled: listView.headerItem.children[1].children[1].value !== 0 // spinBoxYstep
            text: qsTr("OK")
            onClicked: function() {
                dialog.accept()
                projectAccepted()
            }
        }

        Item {
            Layout.fillWidth: true
        }
    }

    Component {
        id: listViewHeader

        Column {
            spacing: 10
            z: 2

            RowLayout {
                spacing: 5
                Label {
                    font.pointSize: 12
                    text: qsTr('Project name: ')
                }
                Label {
                    id: projectNameLabel
                    font.pointSize: 12
                    text: datastore.newProjectName
                }
            }

            Row {
                spacing: 5
                Text {
                    text: qsTr("Y step: ")
                    font.pointSize: 12
                    anchors.verticalCenter: parent.verticalCenter
                }

                FloatSpinBox {
                    id: spinBoxYstep
                    onValueChanged: datastore.newProjectYstep = value/scale
                }

                Button {
                    id: updateButton
                    text: qsTr("Update")
                    onClicked: projectWizardUpdateYoffsets()
                }
            }

            Row {
                spacing: 5
                id: headerRow
                function itemAt(index) { return repeater.itemAt(index) }
                Repeater {
                    id: repeater
                    model: [qsTr("File name"), qsTr("Offset Y")]
                    Label {
                        text: modelData
                        font.bold: true
                        font.pointSize: 12
                        padding: 10
                        background: Rectangle { color: "silver" }
                        width: 150
                    }
                }
            }
        }
    }
}
