import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.1

ApplicationWindow {
    id: window
    title: datastore.projectName.length !== 0 ? "Profilometer -- %1".arg(datastore.projectName) : "Profilometer"

    width: 800; height: 700

    signal currentLineChanged(int offset)
    signal newProjectFilesChosen(var filepaths)
    signal projectFileChosen(var filepath)
    signal projectWizardUpdateYoffsets()
    signal projectAccepted()

    function onOpenWizard() {
        projectWizard.open()
    }

    Component.onCompleted: {
        projectWizard.projectWizardUpdateYoffsets.connect(projectWizardUpdateYoffsets)
        projectWizard.projectAccepted.connect(projectAccepted)
    }

    FileDialog {
        id: newProjectFileDialog
        nameFilters: ["PRF files (*.PRF)"]
        selectMultiple: true
        selectFolder: false
        selectExisting: true
        onAccepted: newProjectFilesChosen(fileUrls)
    }

    FileDialog {
        id: openProjectFileDialog
        nameFilters: ["JSON file (*.json)"]
        selectMultiple: false
        selectFolder: false
        selectExisting: true
        onAccepted: projectFileChosen(fileUrls)
    }

    Dialog {
        id: renameDialog
        title: qsTr("Rename project")
        modal: true
        visible: false
        standardButtons: Dialog.Ok | Dialog.Cancel

        contentItem:
            RowLayout {
            Label {
                text: qsTr("New project name: ")
            }
            TextField {
                id: projectNameField
                text: datastore.projectName
            }
        }

        onAccepted: datastore.projectName = projectNameField.text
        onRejected: projectNameField.text = datastore.projectName
    }

    ProjectWizard {
        id: projectWizard
        x: (window.width - width) / 2
        y: (window.height - height) / 2
    }

    header: ColumnLayout {
        Toolbar {}

        TabBar {
            id: tabBar
            TabButton {
                text: qsTr("Profile analysis")
                width: implicitWidth
                onToggled: datastore.model.isVisible = false
            }
            TabButton {
                text: qsTr("Fabric analysis")
                width: implicitWidth
                onToggled: datastore.model.isVisible = false
            }
            TabButton {
                text: qsTr("3D model")
                width: implicitWidth
                onToggled: datastore.model.isVisible = true
            }

            onCurrentIndexChanged: function() {
                if (currentIndex == 0 || currentIndex == 1) {
                    stack.currentIndex = 0
                    mainView.changeView(currentIndex)
                } else {
                    stack.currentIndex = 1
                }
            }
        }
    }

    StackLayout {
        id: stack
        anchors.fill: parent

        MainView { id: mainView }
        ModelView { projectOpened: datastore.projectName.length !== 0 }
    }

    footer: Label {
        leftPadding: 8
        text: datastore.statusBarMessage
        visible: !datastore.model.isVisible
    }
}
