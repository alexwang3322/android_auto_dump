import os
import xml.etree.ElementTree as ET

import time
import shutil   
import cv2

from window import LayoutChangeStatus, Window
from androidManifestParser import AndroidManifestParser
import status

traversalPath = open(status.TP, 'a+')

def produceSpaces(page, depth):
    prespace = " " * ((depth - 1) * 2)
    traversalPath.write(prespace + page.getPageName() + "\n")


class Application:
    def __init__(self, apkName='app-debug', packages=['com.example']):
        self.manifest = AndroidManifestParser(apkPath='data/apk/', apkName=apkName, packages=packages)
        self.manifest.get()
        self.window = Window(self.manifest) # self.manifest


    def nothing(self):
        pass


    def pageMerge(self, pre_page, new_page):
        pre_page.merge(new_page)
        produceSpaces(pre_page, pre_page.depth)


    def out(self, state, pre_page, new_page):        
        print("[backStack]", self.window.pageBackStack)
        print("[last_page]", pre_page)
        #print('[last_page] **finished elements**', pre_page.elementsFinshied)
        print("[new_page]", new_page)
        print('[result]', state, '\n\n')
        

    def startcallback(self, element, page):
        print("[" + element.getElementType() + "]", element, 'at', page.getPageName())
        #print("[with]", page.getElements())    
        return element.operate()


    def finishcallback(self, state, pre_page, new_page):        
        self.out(state, pre_page, new_page)
        if state == LayoutChangeStatus.NEW_LAYOUT:                     
            self.run(depth=pre_page.depth, page=new_page)            
        elif state == LayoutChangeStatus.LAYOUT_MERGE:
            self.pageMerge(pre_page, new_page)
        elif state == LayoutChangeStatus.PAGE_EXIT: 
            self.window.pageBackStack.pop()
        elif state == LayoutChangeStatus.APPLICATION_EXIT:            
            self.window.pageBackStack.pop()    
        elif state == LayoutChangeStatus.ERROR:
            self.nothing()    
        elif state == LayoutChangeStatus.PAGE_EMPTY_EXIT: 
            self.nothing() ## like a dialog disappear, we dont want to close our current activity
        else:
            self.nothing()
        

    def run(self, depth=0, page=None):        
        new = self.window.createPageWithAppend(depth, page)        
        
        callDepth = status.TRAVERSALPATH_STRIDE + depth
        new.depth = callDepth
        produceSpaces(new, callDepth)
        
        new.traversal(self.startcallback, self.finishcallback)
        

def ready(packages):
    traversalPath.truncate(0)    
    try: 
        for p in packages:
            path = p.replace(".", '/')
            shutil.rmtree(status.DUMP + path)        
    except:
        pass            


if __name__ == "__main__":
    
    #ready(packages=['com.taobao.trip'])
    #app1 = Application(apkName='portal-debug', packages=['com.taobao.trip'])
    
    ready(packages=['com.example'])
    app1 = Application()

    app1.run()
    print('[finish]', app1.window.pageBackStack)        