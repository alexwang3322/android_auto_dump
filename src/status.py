import os

exitStatus = ['KEYCODE_BACK']


class LayoutChangeStatus:    
    NEW_LAYOUT = "NEW_LAYOUT" 
    LAYOUT_MERGE = "LAYOUT_MERGE"
    APPLICATION_EXIT = "APPLICATION_EXIT"
    PAGE_EXIT = "PAGE_EXIT"
    PAGE_EMPTY_EXIT = "PAGE_EMPTY_EXIT" # wiil do nothing exit
    PAGE_BACK = "PAGE_BACK"
    ERROR = "ERROR"
    NONE = "NOTHING" 
    


class ElementType:
    EXIT = "Exit"
    BUTTON = "Button"
    EDIT = "Edittext"
    LIST = "Listview"
    TEXT = "Text"


class TouchEvent:
    BACK = "KEYCODE_BACK"


TRAVERSALPATH_STRIDE=1

CLICKABLE_VIEWS = ['android.widget.LinearLayout', 
                'android.widget.RelativeLayout', 
                'android.widget.FrameLayout', 
                'android.widget.Button']


# the view id we don't want to use.
DO_NOT_USE = ['com.taobao.trip:id/fliggy_commonui_navigation_bar_right',
                'com.taobao.trip:id/btn_common_map_navigation_view',
                'com.taobao.trip:id/navigation_image']


# the view id we don't want to use in spec Activity
ACTIVITY_CONFIGS = {
    '.bus.busdetail.ui.BusDetailActivity': ['com.taobao.trip:id/bus_detail_station_list_tv',
    'com.taobao.trip:id/bus_detail_online_return_tv', 
    'com.taobao.trip:id/bus_detail_online_id_get_on_tv']
}


DO_EXIT_DIR_ACTIVITY = ['WeexActivity']


CWD = os.getcwd()
DATA = CWD + '/data/'
SRC = CWD + '/src/'
LOG = CWD + '/data/log/'
DUMP =  DATA + 'dump/'

SHELL = SRC + 'android.sh'

TP = LOG + 'traversalpath'
DA = LOG + 'dumpsysactivity'
WN = LOG + 'dumpswindows'
TXML = DUMP + 'temp.xml'