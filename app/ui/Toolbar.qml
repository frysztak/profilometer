import QtQuick 2.0
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3

ToolBar {
    anchors.fill: parent

    RowLayout {
        ToolButton {
            id: projectButton
            text: qsTr("Project...")
            onClicked: projectMenu.open()
        }
        Menu {
            id: projectMenu
            y: projectButton.height
            x: projectButton.x

            MenuItem {
                text: "New"
                onClicked: newProjectFileDialog.open()
            }
            MenuItem {
                text: "Open"
                onClicked: openProjectFileDialog.open()
            }
            MenuItem {
                text: "Rename"
                enabled: datastore.projectName.length !== 0
                onClicked: renameDialog.open()
            }
            MenuItem {
                text: "Save"
                enabled: datastore.projectName.length !== 0
                onClicked: datastore.saveProject()
            }
            MenuItem {
                text: "Exit"
                onClicked: Qt.quit()
            }
        }

        ToolButton {
            id: exportButton
            text: qsTr("Export...")
            onClicked: exportMenu.open()
        }

        Menu {
            id: exportMenu
            y: exportButton.height
            x: exportButton.x

            MenuItem {
                text: "Export current measurement"
                enabled: datastore.projectName.length !== 0
                onClicked: datastore.currentMeasurement.exportMeasurement()
            }
            MenuItem {
                text: "Export all measurements"
                enabled: datastore.projectName.length !== 0
                onClicked: datastore.exportMeasurements()
            }
            MenuSeparator {
                padding: 0
                topPadding: 6
                bottomPadding: 6
                contentItem: Rectangle {
                    implicitWidth: 200
                    implicitHeight: 1
                    color: "#1E000000"
                }
            }
            MenuItem {
                text: "Export model to image file"
                enabled: datastore.model.isCalculated
                onClicked: datastore.exportModelToImage()
            }
            MenuItem {
                text: "Export model to text file"
                enabled: datastore.model.isCalculated
                onClicked: datastore.exportModelToText()
            }
        }

        ToolButton {
            id: modelButton
            text: qsTr("3D model...")
            onClicked: modelMenu.open()
        }

        Menu {
            id: modelMenu
            y: modelButton.height
            x: modelButton.x

            MenuItem {
                text: "Clear"
                enabled: datastore.model.isCalculated
                onClicked: datastore.model.clear()
            }
        }

        Item {
            Layout.fillWidth: true
        }
    }
}
