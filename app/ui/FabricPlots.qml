import QtQuick.Controls 2.2
import QtCharts 2.2

Frame {
    width: parent.width
    spacing: 10
    height: 400
    rightPadding: 12
    property alias chartView: chart

    property alias axisX:  xAxis
    property alias axisY:  yAxis
    property alias profileSeries: profile
    property alias smoothedProfileSeries: smoothedProfile

    property alias axisX2: xAxis2
    property alias axisY2:  yAxis2
    property alias fftSeries: fft
    property alias maximaSeries: maxima

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
            titleText: qsTr("Profile: X [mm]")
        }

        ValueAxis {
            id: yAxis
            titleText: qsTr("Profile: Y [μm]")
        }

        ValueAxis {
            id: xAxis2
            titleText: qsTr("FFT: X [mm]")
        }

        ValueAxis {
            id: yAxis2
            titleText: qsTr("FFT: Y [μm]")
        }

        LineSeries {
            id: profile
            axisX: xAxis
            axisY: yAxis
            name: qsTr("Profile")
            useOpenGL: true
        }

        LineSeries {
            id: smoothedProfile
            axisX: xAxis
            axisY: yAxis
            name: qsTr("Smoothed profile")
            useOpenGL: true
        }

        LineSeries {
            id: fft
            axisXTop: xAxis2
            axisYRight: yAxis2
            name: qsTr("FFT")
            useOpenGL: true
        }

        ScatterSeries {
            id: maxima
            axisXTop: xAxis2
            axisYRight: yAxis2
            name: qsTr("FFT maxima")
            useOpenGL: false

            markerShape: ScatterSeries.MarkerShapeCircle
            markerSize: 12
        }
    }
}
