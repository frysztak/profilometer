import QtQuick.Controls 2.2
import QtCharts 2.2

Frame {
    width: parent.width
    spacing: 10
    height: 400
    rightPadding: 12
    property alias chartView: chart
    property alias axisX: xAxis
    property alias axisY: yAxis
    property alias profileSeries: profile
    property alias wavinessSeries: waviness
    property alias roughnessSeries: roughness

    ChartView {
        id: chart
        height: parent.height
        width: parent.width
        titleColor: "#404441"
        //title: qsTr("")
        visible: true
        antialiasing: true
        //legend.visible: true
        //legend.alignment: Qt.AlignBottom
        //legend.font.pointSize: 10

        ValueAxis {
            id: xAxis
            titleText: qsTr("X [mm]")
        }

        ValueAxis {
            id: yAxis
            titleText: qsTr("Y [μm]")
        }

        LineSeries {
            id: profile
            axisX: xAxis
            axisY: yAxis
            name: qsTr("Profile")
            useOpenGL: true
        }

        LineSeries {
            id: waviness
            axisX: xAxis
            axisY: yAxis
            name: qsTr("Waviness")
            useOpenGL: true
        }

        LineSeries {
            id: roughness
            axisX: xAxis
            axisY: yAxis
            name: qsTr("Roughness")
            useOpenGL: true
        }
    }
}
