
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import tool
from status import TouchEvent 
import os, shutil 


class AndroidManifestParser:
    def __init__(self, apkPath, apkName, packages):
        self.apkPath = apkPath
        self.apkName = apkName
        self.manifestXml = "AndroidManifest.xml"
        self.df = None
        self.packages = packages
        self.cvs = self.apkPath + self.apkName + ".csv"


    def decomposeAPK(self): 
        path = self.apkPath + self.apkName       
        if not os.path.exists(path):
            apk = path + ".apk"  
            try: 
                shutil.rmtree(path)        
            except:
                pass            
            os.system("apktool d " + apk + " -o " + path)
        

    def parseManifest(self):
        manifestXMLFile = self.apkPath + self.apkName + "/" + self.manifestXml
        packages = self.packages
        activities = []
        root = ET.parse(manifestXMLFile).getroot()
        application = root.find('application')
        for activity in application.findall('activity'):
            name = activity.attrib['{http://schemas.android.com/apk/res/android}name']
            shouldAppend = False
            for p in packages:
                shouldAppend = shouldAppend or name.startswith(p)
            if shouldAppend or len(packages) == 0:
                activities.append(name)

        tags = [0] * len(activities)    
        pageName = [""] * len(activities)    
        self.manifest = {'activityName': activities, "pageName": pageName, "exitId": tags, "avaliable": tags}
        self.df = pd.DataFrame(self.manifest, columns=['activityName', 'pageName', 'exitId', 'avaliable'])


    def parsing(self):
        self.decomposeAPK()
        self.parseManifest()
        try:
            shutil.rmtree("./" + self.apkPath + self.apkName)
        except:
            pass


    def get(self, activityName=None, resource_id=None, avaliable=None):        
        if os.path.exists(self.cvs):
            self.df = pd.read_csv(self.cvs)
        else:            
            self.parsing()
            self.toExcel()


    def getAvaliable(self, activityName):
        name = str.split(activityName, "/")[-1]
        l = self.df.avaliable[self.df.activityName.str.contains(name)].tolist()        
        if l is None or len(l) == 0:
            return None            
        return l[0]


    def getExitId(self, activityName):
        name = str.split(activityName, "/")[-1]
        l = self.df.exitId[self.df.activityName.str.contains(name)].tolist()        
        if l is None or len(l) == 0:
            return None
        return l[0]
    

    def getExitIdByPageName(self, pageName):
        l = self.df.exitId[self.df.pageName.str.contains(pageName)].tolist()        
        if l is None or len(l) == 0:
            return None
        return l[0]


    def dump(self):
        return self.manifest


    def toExcel(self):        
        self.df.to_csv(self.apkPath + self.apkName + ".csv")


    def avaliable(self, activityName):
        index = self.manifest['activityName'].index('activityName')
        avaliable = self.manifest['avaliable'][index]
        return avaliable


    def contains(self, packageName):
        for a in self.packages:
            if packageName.startswith(a):
                return True
        return False



def testcase1():
    manifest = AndroidManifestParser("data/apk/", "app-debug", ['com.example'])
    manifest.parsing()    
    print(manifest.df)
    e = manifest.getExitId("com.example.ws3.testapp.parser.BActivity")
    print(e)    

def testcase2():    
    manifest = AndroidManifestParser("data/test", "", [])
    manifest.parseManifest()
    print(manifest.df)

if __name__ == "__main__":
    testcase2()
    