import xml.etree.ElementTree as ET

import tool as tool
import draw
from draw import DrawNode
import time
from status import exitStatus, ElementType, LayoutChangeStatus



class Element(DrawNode):
    def __init__(self, page, resource_id, bounds):
        super(Element, self).__init__(resource_id, bounds)
        self.page = page
        self.activityName = page.activityName
        self.resource_id = resource_id
        self.elementType = None
        self.index = -1

    def setIndex(self, index):
        self.index = index        

    def setClassName(self, className):
        self.className = className
        if self.className == "android.widget.EditText":
            self.elementType = ElementType.EDIT
        else:
            self.elementType = ElementType.BUTTON    


    def setType(self, eleType):
        self.elementType = eleType

    def click(self):
        x, y = self.getPoint()
        tool.click(x, y)  

    def text(self, msg="123456"):
        self.click()
        tool.text(msg)
        tool.sh_exec("adb shell input keyevent KEYCODE_BACK")
							
    def getElementType(self):
        return self.elementType

    def exit(self):
        if self.resource_id in exitStatus:
            tool.sh_exec("adb shell input keyevent " + self.resource_id)
        else:
            self.click()

    def operate(self): 
        state = None 
        if self.getElementType() == ElementType.EXIT:
            self.exit()    
            if len(self.page.window.pageBackStack) == 1:
                state = LayoutChangeStatus.APPLICATION_EXIT
            else:                
                state = LayoutChangeStatus.PAGE_EXIT            
        elif self.getElementType() == ElementType.EDIT:
            self.text()
        else:
            self.click()       
        return state

    def __eq__(self, other):
        if self.resource_id != "":
            return self.resource_id == other.resource_id        
        else:
            return self.index == other.index and self.className == other.className            

    def __hash__(self):
        if self.resource_id != "":
            return hash(self.resource_id)
        else:
            return hash(str(self.index) + self.className)            
    
    def __repr__(self):
        if self.resource_id != "":
            return "{i:" + str(self.index) + ", id:" + self.resource_id + ", type:" + str(self.elementType) + "}"
        else:
            return "{i:" + str(self.index) + ", id:" +self.className + ", type:" + self.elementType + "}"                        

    def dump(self):
        return "(" + self.resource_id + ")"
        #return "(" + self.resource_id + " " + str(self.getBound()) + ")"




