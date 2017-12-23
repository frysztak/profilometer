import QtQuick 2.2
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.2

SpinBox {
    id: spinbox
    editable: true
    font.pointSize: 10
    from: 0
    to: 100*scale
    property int decimals: 2
    property real realValue: value / scale
    property int scale: 100
    property string units: 'mm' //'μm'

    validator: DoubleValidator {
        bottom: Math.min(spinbox.from, spinbox.to)
        top:  Math.max(spinbox.from, spinbox.to)
    }
    textFromValue: function(value, locale) {
        //return Number(num).toLocaleString(locale, 'f', spinbox.decimals)
        var num = realValue.toFixed(decimals)
        return num + " " + units
    }
    valueFromText: function(text, locale) {
        return parseFloat(text) * scale
    }

    function setFromRealValue(realVal) {
        console.log('realval: ', realVal)
        value = realVal * scale
    }
}
