import xml.etree.ElementTree as ET
import tool 
from element import Element
from pout import out
from base import PageBase
import cv2
import os
from collections import deque
from element import ElementType
from status import TouchEvent
import status
import time
import shutil

'''
page parsing
BFS -> ElementQueue

page traversal 
ElementQueue: E1, E2, E3
eq.poll().operation()

'''

class Page(PageBase):
    def __init__(self, window):
        super(Page, self).__init__(window)   
                
                           
    '''
    1. parse viewtree ojbect into elements by a temp viewtree xml file
    2. also add exit element into the tail of elements
    3. move the temp viewtree xml file to its expected folder if the viewtree not exist
    '''
    def parsing(self):    
        
        # dumping into temp                    
        tool.dumpLayoutXml(status.DUMP, status.TXML)                        
        
        # parsing
        root = ET.parse(status.TXML).getroot().find("node")
        elementsQueue = deque([root])        

        # init exit id
        exitManifestId = None
        avaliable = None
        self.exitResourceElement = None
        
    
        if self.window and self.window.getManifest():                    
            mani = self.window.getManifest()
            # if it is a dialog page
            if tool.isDialogWindow(self.activityName):
                exitManifestId = TouchEvent.BACK
            else:
                exitManifestId = str(mani.getExitId(self.activityName)) 
            avaliable = str(mani.getAvaliable(self.activityName))                       

        activityConfig = status.ACTIVITY_CONFIGS.get(self.getActivityName(), None)        
        
        # BFS
        while(len(elementsQueue) != 0) and (avaliable == '1' or avaliable == '1.0'):
            child = elementsQueue.popleft()            
             
            clickable = child.attrib['clickable']
            resource_id = child.attrib['resource-id']     
            bounds = child.attrib['bounds']
            className = child.attrib['class']
                         
            if resource_id in status.DO_NOT_USE:
                continue

            if activityConfig and resource_id in activityConfig:
                continue                

            if child in elementsQueue:
                continue
            
            # put values into fields
            nodes = None
            e = Element(self, resource_id, bounds)            
            e.setIndex(self.getElementSize())
            e.setClassName(className)

            if clickable == "true" and resource_id != "":   
                if resource_id.endswith(exitManifestId):                                        
                    self.exitResourceElement = e
                    self.exitResourceElement.setType(ElementType.EXIT)
                else:         
                    self.elementsBesideExit.append(e)            
                    self.appendElement(e)
                          
            nodes = child.findall('node')                    
            elementsQueue.extend(nodes)                      

        # add exit method to this page    
        if not self.exitResourceElement:
            self.exitResourceElement = Element(self, exitManifestId, None)
            self.exitResourceElement.setType(ElementType.EXIT)
        self.exitResourceElement.setIndex(self.getElementSize())                                            
        self.appendElement(self.exitResourceElement)

        # move xml file 
        pageXml = self.getPagePath() + self.getPageName() + ".xml"                    
        if not os.path.exists(pageXml):   
            if not os.path.exists(self.getPagePath()):
                os.makedirs(self.getPagePath())         
            shutil.copyfile(status.TXML, pageXml)              
        
        # all avaliable values put into elements already



    def traversal(self, startcallback=None, finishcallback=None, test=False):                                                
        state = None
        newPage = None
        prePage = None

        self.drawElements()
        #self.refreshElements()

        for e in self.getElements():     
            if startcallback:
                state = startcallback(e, self)                        

            self.addFinishedElement(e)            
            time.sleep(self.elementWaitGapSecond)

            if state is None and self.window:
                state, prePage, newPage = self.window.checkChange(self)                

            if finishcallback:
                finishcallback(state, self, newPage)
                time.sleep(self.elementWaitGapSecond)                
            

    def exit(self):
        self.exitResourceElement.operate()

    
    # window
    def merge(self, newPage):
        diff = newPage.difference(self)
        # put exitId into last of queue
        self.addElements(diff)
        '''
        try:
            os.remove(self.getPagePath() + self.getPageName() + ".xml")
            os.remove(self.getPagePath() + self.getPageName() + ".png")
        except:
            pass
        '''            
        # put new page into 
        newPage.drawElements()
        self.pageName = newPage.pageName
        self.im = newPage.im
        

    def addElements(self, elements):        
        exitId = self.elements.pop()
        size = self.getElementSize()         
        for e in elements:
            e.index += size 
            self.appendElement(e)    
        
        exitId.index = self.getElementSize()
        self.appendElement(exitId)
    

def startcallback(element):
    print("[click]", element)    
    return element.operate()


def finishcallback(state, pre_page, new_page):
    print('[finished]', state, pre_page, new_page)        


def testPage():
    from androidManifestParser import AndroidManifestParser
    from window import Window
    apk = 'portal-debug' 
    apk = 'app-debug'
    packs = ['com.taobao.trip'] 
    packs = ['com.example']
    manifest = AndroidManifestParser(apkPath='data/apk/', apkName=apk, packages=packs)
    
    manifest.get()
    window = Window(manifest)
    p = window.createPageWithAppend() 
    print('[elements]', p.elements) # test parseing
    print('[pagename]', p.getPageName())

    p.drawElements()

#    p.traversal(startcallback, finishcallback)
#    print('[elementsFinshied]', p.elementsFinshied) # test traversal


if __name__ == "__main__":
    testPage()
    #testIntersection()
    #testMerge()
    #testDiff()