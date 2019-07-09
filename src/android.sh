
function dump() {
    adb shell uiautomator dump         
    adb pull /sdcard/window_dump.xml $1 >> data/log/sys
}

function snapshot() {
    adb exec-out screencap -p > $1 #data/window_dump.png
}

function exitActivity() {
    adb shell am start -W -n $1/$2
}

function click() {
    adb shell input tap $1 $2
}

function swipe() {
    adb shell input swipe x1 y1 x2 y2
}

function destroyWeex() {
    adb shell am start -W -n com.taobao.trip/.weex.WeexActivity
}

function windows() {
    adb shell dumpsys window displays | grep "windows=" | head -1 > data/log/dumpswindows
}

function activityName() {
    adb shell dumpsys window windows | grep -E 'mCurrentFocus' | awk -F "\/" '{split($2, a, "}")}; {print a[1]};' 
}

$1 $2 $3
