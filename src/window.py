from page import Page
from pout import out
import tool
import status
from collections import deque
from status import LayoutChangeStatus


class Window:
    def __init__(self, manifest):
        self.manifest = manifest
        self.exitStatus = ['KEYCODE_BACK']
        self.pageBackStack = deque()
        self.prePage = None
        self.newPage = None

    def check(self, page):
        if self.manifest is None:
            return True
        if self.manifest.contains(page.getPackageName()):
            return True                
        return False 

    def append(self, page):           
        if not self.check(page):
            raise Exception("*****package not right*****", page.getPackageName(), self.manifest.packages)
        self.pageBackStack.append(page)        

    def createPage(self):            
        page = Page(self)            
        page.parsing()
        return page

    def createPageWithAppend(self, depth=0, page=None):
        if page is None:
            page = self.createPage()

        if self.prePage is None:
            self.prePage = page
        else:
            self.prePage = self.newPage
            self.newPage = page   
                
        self.append(page)                     
        page.depth = depth
        return page


    def sameActivityCheck(self, prePage, newPage):
        # a empty page should exit directly
        if newPage.elementsBesideExit == []:
            newPage.exit() 
            return LayoutChangeStatus.PAGE_EXIT, prePage, newPage
                    
        diff = newPage.difference(prePage)             
        if len(diff) == 0: # nothing change
            return LayoutChangeStatus.NONE, prePage, newPage                            
        elif diff == set(newPage.elementsBesideExit): # page defintly not same    
            if len(self.pageBackStack) >= 2:
                # check it is circle calling, like this situation:
                # eque([BusHomeActivity_7609395336725850600, BusHomeActivity_7186982384285961855, BusHomeActivity_7609395336725850600, BusHomeActivity_7186982384285961855])
                lastPageInStack = self.pageBackStack[-2]
                if lastPageInStack.getPageName() == newPage.getPageName():
                    return LayoutChangeStatus.PAGE_EMPTY_EXIT, prePage, newPage            
            return LayoutChangeStatus.NEW_LAYOUT, prePage, newPage  
        else: # page partly same               
            return LayoutChangeStatus.LAYOUT_MERGE, prePage, newPage                                       


    def diffActivityCheck(self, prePage, newPage):
        lastPage = self.pageBackStack[-1]
        if lastPage.getPageName() == newPage.getPageName():
            newPage.exit() # a empty page should exit directly
            return LayoutChangeStatus.PAGE_EXIT, prePage, newPage
        else: 
            # page name not same    
            return LayoutChangeStatus.NEW_LAYOUT, prePage, newPage  

    '''
    if new page is a dialog in the activity
    '''
    def checkChange(self, prePage): 
        newPage = self.createPage()
        if not self.manifest.contains(newPage.getPackageName()): 
            if len(self.pageBackStack) == 0:
                return LayoutChangeStatus.APPLICATION_EXIT, None, None
            else:
                return LayoutChangeStatus.ERROR, prePage, None
            
        if prePage.getActivityName() == newPage.getActivityName():        
            return self.sameActivityCheck(prePage, newPage)
        else:
            return self.diffActivityCheck(prePage, newPage)

    
    def getManifest(self):        
        return self.manifest

    def dump(self):
        return getPage(self).dump()        

    def size(self):       
        return len(self.pageBackStack)
