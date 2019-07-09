import tool 
import cv2
import os
import time

'''

'''
class PageBase:    

    def __init__(self, window):
        self.window = window
        self.elementsFinshied = []
        self.elements = []        
        self.elementsBesideExit = []
        self.packageName, self.activityName = tool.activity()
        self.im = None
        self.pageName = None
        self.pagePath = None    

        self.elementWaitGapSecond = 2    
        self.depth = 0    
        self.isDrawed = False    
        
    
    def __repr__(self):
        return self.getPageName()

    def addFinishedElement(self, e):
        self.elementsFinshied.append(e)

    def refreshElements(self):                
        t = [e for e in self.elements if e not in set(self.elementsFinshied)]        
        self.elements = t

    def getElements(self):
        return self.elements

    def getElementSize(self):
        return len(self.elements)

    def appendElement(self, element):        
        self.elements.append(element)

    def getElementSize(self):
        return len(self.elements)

    def getPagePath(self):
        if self.pagePath is None:
            self.pagePath = tool.getPath(self.packageName + self.activityName)        
        return self.pagePath

    def getPageName(self):
        if self.pageName is None:                                  
            self.pageName = str.split(self.activityName, ".")[-1] + "_" + str(hash(str(self.elementsBesideExit)))
        return self.pageName
    
    def getPackageName(self):
        return self.packageName

    def getActivityName(self):
        return self.activityName

    def getSnapshotPath(self):
        return self.getPagePath() + self.getPageName() + ".png"            

    def initSnapshotImage(self):        
        if self.im is None:
            tool.takeSnapshot(self.getSnapshotPath())            
            self.im = cv2.imread(self.getSnapshotPath())        
        return self.im

    def drawElements(self):
        if not self.isDrawed:
            self.isDrawed = True
            self.initSnapshotImage() 
            for e in self.elements:            
                e.draw(self.im, e.index)
            cv2.imwrite(self.getSnapshotPath(), self.im)

    def dump(self):
        pageInfo = "{ActivityName:" + self.getActivityName() + " ,PackageName:" + self.getPackageName() + ", elements:{"
        for e in self.getElements():        
            pageInfo += " " + e.dump()
        pageInfo += "}}"            
        return pageInfo   

    # window
    def intersection(self, newPage):
        newElements = newPage.getElements()
        inters = set(newElements).intersection(set(self.elements))
        return inters

    # no use
    def difference(self, page):     
        diff = set(self.elementsBesideExit) - set(page.elementsBesideExit)
        return diff

def testDiff1():
    from element import Element
    page1 = PageBase(None)
    page1.activityName = "p1"
    e11 = Element(page1, "11", None)
    e12 = Element(page1, "12", None)
    e13 = Element(page1, "13", None)
    page1.elementsBesideExit.append(e11)
    page1.elementsBesideExit.append(e12)
    page1.elementsBesideExit.append(e13)
    
    page2 = PageBase(None)
    page2.activityName = "p2"
    e21 = Element(page2, "21", None)
    e22 = Element(page2, "22", None)
    e23 = Element(page2, "23", None)
    page2.elementsBesideExit.append(e21)
    page2.elementsBesideExit.append(e22)
    page2.elementsBesideExit.append(e23)

    
    diff = page1.difference(page2)
    print(diff)
    print(len(diff))
    print(diff == set(page1.elementsBesideExit))


    
if __name__ == '__main__':
    # test difference()
    testDiff1()
    